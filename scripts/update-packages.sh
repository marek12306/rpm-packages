#!/bin/bash
set -e

for PKG_DIR in */; do
    # Remove trailing slash
    PKG_DIR=${PKG_DIR%/}
    if [ "$PKG_DIR" = "scripts" ]; then continue; fi

    UPSTREAM_FILE="${PKG_DIR}/upstream.txt"
    SPEC_FILE=$(ls ${PKG_DIR}/*.spec 2>/dev/null | head -n 1)

    if [ ! -f "$UPSTREAM_FILE" ] || [ -z "$SPEC_FILE" ]; then
        continue
    fi

    # Strip text
    UPSTREAM_REPO=$(cat "$UPSTREAM_FILE" | tr -d '[:space:]')
    echo "Checking ${PKG_DIR}..."

    LATEST_TAG=$(curl -s "https://api.github.com/repos/${UPSTREAM_REPO}/releases/latest" | jq -r .tag_name)
    if [ "$LATEST_TAG" = "null" ] || [ -z "$LATEST_TAG" ]; then
        echo "  [!] Couldn't check upstream version"
        continue
    fi

    # Remove initial v from version tag
    UPSTREAM_VERSION=${LATEST_TAG#v}
    CURRENT_VERSION=$(grep -i "^Version:" "${SPEC_FILE}" | awk '{print $2}')

    echo "  Current version: ${CURRENT_VERSION} -> New version ${UPSTREAM_VERSION}"

    if [ "$UPSTREAM_VERSION" != "$CURRENT_VERSION" ]; then
	BRANCH_NAME="update-${PKG_DIR}-${UPSTREAM_VERSION}"

	if git ls-remote --heads origin "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
            echo "  [-] Pull request already exists, skipping."
            continue
        fi

	echo "  [+] Updating ${SPEC_FILE}..."
	git checkout -b "$BRANCH_NAME"
        
	# Update version in spec file
        sed -i "s/^Version:.*/Version:        ${UPSTREAM_VERSION}/i" "${SPEC_FILE}"

	# Download latest release notes
	RELEASE_NOTES=$(curl -s "https://api.github.com/repos/${UPSTREAM_REPO}/releases/latest" | jq -r .body | tr -d '\r')
	COMMIT_MSG_FILE="/tmp/commit_msg_${PKG_DIR}.txt"
	echo "Update ${PKG_DIR} to version ${UPSTREAM_VERSION}" > "$COMMIT_MSG_FILE"
        echo "" >> "$COMMIT_MSG_FILE" 

	if [ "$RELEASE_NOTES" != "null" ] && [ -n "$RELEASE_NOTES" ]; then
            echo "Upstream release notes:" >> "$COMMIT_MSG_FILE"
            echo "$RELEASE_NOTES" >> "$COMMIT_MSG_FILE"
        else
            echo "- Auto update to upstream version ${UPSTREAM_VERSION}" >> "$COMMIT_MSG_FILE"
        fi
        
        git add "${SPEC_FILE}"
        git commit -F "$COMMIT_MSG_FILE"
	git push origin "$BRANCH_NAME"

	echo "  [+] Creating pull request..."
        gh pr create \
            --title "Update ${PKG_DIR} to version ${UPSTREAM_VERSION}" \
            --body-file "$COMMIT_MSG_FILE" \
            --base "$DEFAULT_BRANCH" \
            --head "$BRANCH_NAME"

	git checkout main
	rm -f "$COMMIT_MSG_FILE"
        echo "  [OK] Commited changes to ${PKG_DIR}."
    else
        echo "  [-] Package is up to date"
    fi
done
