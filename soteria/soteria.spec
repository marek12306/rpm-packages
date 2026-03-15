Name:           soteria
Version:        0.3.1
Release:        2%{?dist}
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
mkdir -p .cargo
cat >> .cargo/config.toml << EOF

[profile.rpm]
inherits = "release"
EOF

%build
%cargo_build

%if 0%{?fedora} || 0%{?rhel}
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%endif

# Building translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    msgfmt $file -o po/${lang}.mo
done

%install
rm -rf %{buildroot}
%cargo_install
if [ -d .cargo/bin ]; then
    mkdir -p %{buildroot}%{_bindir}
    install -p -m 0755 .cargo/bin/* -t %{buildroot}%{_bindir}/
fi

# Install translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    install -D -m 0644 po/${lang}.mo %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/soteria.mo
done

%find_lang soteria

%files -f soteria.lang
%license LICENSE
%if 0%{?fedora} || 0%{?rhel}
%license LICENSE.dependencies
%endif
%doc README.md
%{_bindir}/soteria

%changelog
%if 0%{?fedora} || 0%{?rhel}
%autochangelog
%else
* %(LC_ALL=C date +"%a %b %d %Y") marek12306 <marek12306@gmail.com> - %{version}-%{release}
- Automated build for version %{version}
%endif

