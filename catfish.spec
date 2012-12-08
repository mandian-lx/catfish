Summary:	A handy file search tool
Name:		catfish
Version:	0.3.2
Release:	%mkrel 6
Group:		File tools
License:	GPLv2+
URL:		http://software.twotoasts.de/?page=%{name}
Source0:	http://software.twotoasts.de/media/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		%{name}-0.3-fix-separator-position.patch
Patch1:		%{name}.desktop.patch
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
%py_requires -d
Requires:	pygtk2.0-libglade
Requires:	pyxdg
Requires:	dbus-python
Requires:	mlocate
Requires:	findutils
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
rm -rf %{buildroot}

%makeinstall_std

desktop-file-install \
	--remove-category="Utility" \
	--add-category='System' \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/doc/

ln -sf ../icons/hicolor/scalable/apps/%{name}.svg %{buildroot}%{_datadir}/%{name}/
ln -sf ../locale/ %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg


%changelog
* Fri Apr 13 2012 Franck Bui <franck.bui@mandriva.com> 0.3.2-6mdv2012.0
+ Revision: 790629
- strip trailing whitespace and bump release
- fix broken /usr/share/catfish/catfish.svg symlink

  + Sergey Zhemoitel <serg@mandriva.org>
    - patch russian comment in .desktop

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 0.3.2-5mdv2011.0
+ Revision: 590788
- rebuild for py2.7

* Wed Jun 09 2010 Funda Wang <fwang@mandriva.org> 0.3.2-4mdv2010.1
+ Revision: 547339
- add system category (bug#58189)

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.3.2-3mdv2010.0
+ Revision: 436946
- rebuild

* Thu Jan 01 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3.2-2mdv2009.1
+ Revision: 323191
- rebuild for new python

* Sat Nov 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3.2-1mdv2009.1
+ Revision: 300964
- fix file list
- update to new version 0.3.2

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.3-8mdv2009.0
+ Revision: 243437
- rebuild

* Wed Mar 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-6mdv2008.1
+ Revision: 187121
- drop suggests on beagle
- default file manager is Thunar

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-5mdv2008.1
+ Revision: 133604
- suggests beagle
- tune up desktop file

* Tue Dec 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-4mdv2008.1
+ Revision: 131980
- add patch 0, fixes separator position
- do not package COPYING file

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix missing space after final stop

* Wed Oct 31 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-3mdv2008.1
+ Revision: 104108
- fix requires (i hope this will be last time ;)

* Wed Oct 31 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-2mdv2008.1
+ Revision: 104053
- fix requires

* Wed Oct 31 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3-1mdv2008.1
+ Revision: 104023
- fix requires
- change requires fro strigi to beagle, as it is more apopriate ;)
- import catfish


