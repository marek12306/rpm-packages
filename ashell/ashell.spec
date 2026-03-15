Name:           ashell
Version:        0.7.0
Release:        2%{?dist}
Summary:        Wayland status bar for Hyprland and Niri

License:        MIT
URL:            https://malpenzibo.github.io/ashell
Source0:        https://github.com/malpenzibo/ashell/archive/refs/tags/%{version}.tar.gz
Source1:        https://github.com/marek12306/rpm-packages/releases/download/vendor-%{name}-%{version}/%{name}-%{version}-vendor.tar.xz

BuildRequires:  rust >= 1.89
BuildRequires:  cargo
BuildRequires:  clang

BuildRequires:  wayland-protocols-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  wayland-devel
BuildRequires:  dbus-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel

%if 0%{?suse_version}
BuildRequires:  cargo-packaging
%else
BuildRequires:  cargo-rpm-macros
%endif

%description
A ready to go Wayland status bar for Hyprland and Niri.

%prep
%autosetup -p1 -a1
mkdir -p .cargo
cat >> .cargo/config.toml << EOF

[profile.rpm]
inherits = "release"
EOF

%build
cargo fetch --locked
%cargo_build

%if 0%{?fedora} || 0%{?rhel}
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%endif

%install
rm -rf %{buildroot}
if [ -f target/rpm/ashell ]; then
    install -p -m 0755 target/rpm/ashell %{buildroot}%{_bindir}/ashell
elif [ -f target/release/ashell ]; then
    install -p -m 0755 target/release/ashell %{buildroot}%{_bindir}/ashell
else
    echo "Error: Built binary not found"
    exit 1
fi

%files
%license LICENSE
%if 0%{?fedora} || 0%{?rhel}
%license LICENSE.dependencies
%endif
%doc README.md
%{_bindir}/ashell

%changelog
%if 0%{?fedora} || 0%{?rhel}
%autochangelog
%else
* %(LC_ALL=C date +"%a %b %d %Y") marek12306 <marek12306@gmail.com> - %{version}-%{release}
- Automated build for version %{version}
%endif
