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

%description
A ready to go Wayland status bar for Hyprland and Niri.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
rm -rf %{buildroot}
install -D -m 0755 target/release/ashell %{buildroot}%{_bindir}/ashell

%files
%license LICENSE
%doc README.md
%{_bindir}/ashell

%changelog
%autochangelog
