Summary:	A handy file search tool
Name:		catfish
Version:	0.6.4
Release:	4
Group:		File tools
License:	GPLv2+
Url:		http://twotoasts.de/index.php/catfish
Source0:	https://launchpad.net/catfish-search/0.6/%{version}/+download/catfish-%{version}.tar.bz2
BuildArch:	noarch
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
Requires:	pygtk2.0-libglade
Requires:	python-pyxdg
Requires:	python-dbus
Requires:	mlocate
Requires:	findutils

%description
A handy file searching tool for linux. Basically it is a
frontend for different search engines (daemons) which
provides a unified interface. The interface is intentionally
lightweight and simple, using only GTK+ 2. You can configure
it to your needs by using several command line options.

%prep
%setup -q

%build
sed -i.misc \
	-e '/svg/s|install|install -m 644|' \
	-e '/glade/s|install| install -m 644|' \
	-e 's|install |install -p |' \
	-e 's|pyc|py|' \
	-e 's|^\([ \t]*\)ln |\1: ln |' \
	-e 's|cp -rf|cp -prf|' \
	Makefile.in.in

# --libdir= option doesn't work here.
./configure --prefix=%{_prefix}

%install
%makeinstall_std


desktop-file-install \
	--remove-category="Utility" \
	--add-category='System' \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/doc/

ln -sf ../pixmaps/%{name}.svg %{buildroot}%{_datadir}/%{name}/
ln -sf ../locale/ %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
