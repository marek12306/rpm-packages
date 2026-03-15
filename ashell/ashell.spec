Name:           ashell
Version:        0.6.9
Release:        %autorelease
Summary:        Wayland status bar for Hyprland and Niri

License:        MIT
URL:            https://malpenzibo.github.io/ashell
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
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
cargo fetch --locked
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
rm -rf %{buildroot}
%cargo_install

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/ashell

%changelog
%autochangelog
