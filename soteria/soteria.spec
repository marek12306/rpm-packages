Name:           soteria
Version:        0.3.0
Release:        %autorelease
Summary:        Polkit authentication agent written in GTK

License:        Apache-2.0
URL:            https://github.com/imvaskel/soteria
Source0:        https://github.com/imvaskel/soteria/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust >= 1.85
BuildRequires:  cargo
BuildRequires:  gtk4-devel
BuildRequires:  polkit-devel
BuildRequires:  gettext

%description
Soteria is a Polkit authentication agent written in GTK designed to be used with any desktop environment.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

# Building translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    msgfmt $file -o po/${lang}.mo
done

%install
rm -rf %{buildroot}

install -D -m 0755 target/release/soteria %{buildroot}%{_bindir}/soteria

# Install translation files
for file in po/*.po; do
    lang=$(basename $file .po)
    install -D -m 0644 po/${lang}.mo %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/soteria.mo
done

%find_lang soteria

%files -f soteria.lang
%license LICENSE
%doc README.md
%{_bindir}/soteria

%changelog
%autochangelog

