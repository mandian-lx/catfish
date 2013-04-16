Summary:	A handy file search tool
Name:		catfish
Version:	0.3.2
Release:	7
Group:		File tools
License:	GPLv2+
Url:		http://software.twotoasts.de/?page=%{name}
Source0:	http://software.twotoasts.de/media/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		%{name}-0.3-fix-separator-position.patch
Patch1:		%{name}.desktop.patch
BuildArch:	noarch

BuildRequires:	gettext
BuildRequires:	desktop-file-utils
%py_requires -d
Requires:	python-dbus
Requires:	findutils
Requires:	mlocate
Requires:	pygtk2.0-libglade
Requires:	pyxdg

%description
A handy file searching tool for linux. Basically it is a
frontend for different search engines (daemons) which
provides a unified interface. The interface is intentionally
lightweight and simple, using only GTK+ 2. You can configure
it to your needs by using several command line options.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
sed -i.misc \
	-e '/svg/s|install|install -m 644|' \
	-e '/glade/s|install| install -m 644|' \
	-e 's|install |install -p |' \
	-e 's|pyc|py|' \
	-e 's|^\([ \t]*\)ln |\1: ln |' \
	-e 's|cp -rf|cp -prf|' \
	Makefile.in

sed -i.byte -e 's|pyc|py|' %{name}.in

sed -i.engine -e 's|Nautilus|Thunar|' %{name}.py

# --libdir= option doesn't work here.
./configure --prefix=%{_prefix}

%install
%makeinstall_std

desktop-file-install \
	--remove-category="Utility" \
	--add-category='System' \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/doc/

ln -sf ../icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_datadir}/%{name}/
ln -sf ../locale/ %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

