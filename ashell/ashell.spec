Name:           ashell
Version:        0.7.0
Release:        %autorelease
Summary:        Wayland status bar for Hyprland and Niri

License:        MIT
URL:            https://malpenzibo.github.io/ashell
Source0:        https://github.com/MalpenZibo/ashell/archive/refs/tags/%{version}.tar.gz

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
%autosetup -n %{name}-%{version}

%build
cargo fetch --locked
%cargo_build

%install
rm -rf %{buildroot}
%cargo_install

%files
%license LICENSE
%doc README.md
%{_bindir}/ashell

%changelog
%autochangelog
