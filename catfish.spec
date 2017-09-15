%define url_ver %(echo %{version} | cut -d. -f1,2)

Summary:	A handy file search tool
Name:		catfish
Version:	1.4.2
Release:	1
Group:		File tools
License:	GPLv2+
Url:		http://twotoasts.de/index.php/catfish
Source0:	https://launchpad.net/catfish-search/%{url_ver}/%{version}/+download/catfish-%{version}.tar.bz2
BuildArch:	noarch

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(pexpect)
BuildRequires:	python3egg(pygobject)
BuildRequires:	python3egg(python-distutils-extra)
BuildRequires:	python3egg(setuptools)
BuildRequires:	zeitgeist

Requires:	findutils
Requires:	gksu
Requires:	pygtk2.0-libglade
Requires:	python-pyxdg
Requires:	python-dbus
Requires:	python-gi
Requires:	python-gi-cairo
Requires:	python-pexpect
Requires:	mlocate
Requires:	typelib(Gdk)
Requires:	typelib(GLib)
Requires:	typelib(GObject)
Requires:	typelib(GdkPixbuf)
Requires:	typelib(Gtk)
Requires:	typelib(Pango)
Recommends:	zeitgeist

%description
A handy file searching tool for linux. Basically it is a
frontend for different search engines (daemons) which
provides a unified interface. The interface is intentionally
lightweight and simple, using only GTK+ 3. You can configure
it to your needs by using several command line options.

%files -f %{name}.lang -f FILELIST
%doc AUTHORS ChangeLog README
%{py_puresitedir}/%{name}-%{version}-*.egg-info
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/appdata
%dir %{_datadir}/%{name}/media
%dir %{_datadir}/%{name}/ui
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/%{name}.1*

#----------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --root=%{buildroot} --record=FILELIST

# remove *.pyc files, README, man and locales from FILELIST
sed -i -e '/\\*.pyc$/d' FILELIST
sed -i -e '/\\*README$/d' FILELIST
sed -i -e '/\\*%{name}.1/d' FILELIST
sed -i -e '/\\*.mo/d' FILELIST

# fix .desktop
desktop-file-edit \
	--remove-category='Utility' \
	--add-category='System' \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# fix icon path
install -dm 0755 %{buildroot}%{_datadir}/%{name}/media/
ln -sf ../../icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_datadir}/%{name}/media/

# locales
%find_lang %{name} --all-name

