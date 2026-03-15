Name:           soteria
Version:        0.3.0
Release:        %autorelease
Summary:        Polkit authentication agent written in GTK

License:        Apache-2.0
URL:            https://github.com/imvaskel/soteria
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/marek12306/rpm-packages/releases/download/vendor-%{name}-%{version}/%{name}-%{version}-vendor.tar.xz

BuildRequires:  rust >= 1.85
BuildRequires:  cargo
BuildRequires:  gtk4-devel
BuildRequires:  polkit-devel
BuildRequires:  gettext

%if 0%{?suse_version}
BuildRequires:  cargo-packaging
%else
BuildRequires:  cargo-rpm-macros
%endif

%description
Soteria is a Polkit authentication agent written in GTK designed to be used with any desktop environment.

%prep
%autosetup -p1 -a1
%if 0%{?suse_version}
mkdir -p .cargo
cat > .cargo/config.toml <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
%else
%cargo_prep -v vendor
%endif

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

# Building translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    msgfmt $file -o po/${lang}.mo
done

%install
rm -rf %{buildroot}

%cargo_install

# Install translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    install -D -m 0644 po/${lang}.mo %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/soteria.mo
done

%find_lang soteria

%files -f soteria.lang
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/soteria

%changelog
%autochangelog

