Name:           poedit
Version:        2.0.4
Release:        0.1%{?dist}
Summary:        GUI editor for GNU gettext .po files
Summary(de):    Grafischer Editor für GNU Gettext-Dateien

Group:          Development/Tools
License:        MIT
URL:            http://www.poedit.net/
Source0:        https://github.com/vslavik/%{name}/releases/download/v%{version}-oss/%{name}-%{version}.tar.gz
Source1:        http://pkgs.fedoraproject.org/cgit/rpms/%{name}.git/plain/%{name}.1.de.po

BuildRequires:  wxGTK3-devel >= 3.0.3
BuildRequires:  gtkspell3-devel
BuildRequires:  libappstream-glib
BuildRequires:  lucene++-devel
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  po4a
BuildRequires:  libsecret-devel
BuildRequires:  openssl-devel
BuildRequires:  cpprest-devel
# cld2 is not available for ppc64 s390x
%ifnarch ppc64 s390x
BuildRequires:  cld2-devel
%endif
# Use json.hpp from Fedora and not the version bundled with Poedit
BuildRequires:  json-devel


Requires:       gettext


%description
This program is a GUI frontend to GNU Gettext utilities and a catalogs 
editor/source code parser. It helps with translating applications into 
other languages.

%description -l de
Dieses Programm stellt eine grafische Benutzeroberfläche für die
Dienstprogramme aus GNU Gettext bereit, sowie einen Katalogeditor und einen
Quellcode-Parser. Es hilft beim Übersetzen von Anwendungen in andere Sprachen.

%prep
%autosetup
# Make sure docs are utf-8
for FILE in `find docs/en -name '*.hhp'`; do
    iconv -f iso-8859-15 -t utf-8 $FILE > $FILE.tmp && \
    touch -r $FILE $FILE.tmp && \
    mv -f $FILE.tmp $FILE
done


%build
%ifarch ppc64 s390x
# cld2 is not available for ppc64 s390x
%configure --with-wx-config=/usr/bin/wx-config-3.0 --with-cpprest
%else
%configure --with-wx-config=/usr/bin/wx-config-3.0 --with-cpprest --with-cld2
%endif
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

# Remove a few unnecessary locations where the makefile may install
# copies of icons and .desktop files
rm -rf \
    %{buildroot}%{_datadir}/applnk \
    %{buildroot}%{_datadir}/mimelnk \
    %{buildroot}%{_datadir}/gnome \
    %{buildroot}%{_datadir}/mime-info

# Install the desktop file
desktop-file-install \
    --delete-original \
    --add-category=GTK \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/poedit.desktop

# Generate and install localized man pages
mkdir -p man/de
po4a-translate -M utf-8 -f man \
               --option groff_code=verbatim \
               -m docs/%{name}.1 -p %{SOURCE1} \
               -l man/de/%{name}.1

mkdir -p %{buildroot}%{_mandir}/de/man1
install -p -m 644 man/de/%{name}.1 %{buildroot}%{_mandir}/de/man1

appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml ||:

%{find_lang} poedit --with-man


%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f poedit.lang
%doc NEWS README AUTHORS docs/*.txt
%license COPYING
%{_bindir}/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/poedit
%{_datadir}/pixmaps/*
%{_mandir}/man?/*


%changelog
* Fri Oct 13 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.0.4-0.1
- New upstream version
- Configure without cld2 for ppc64 s390x (instead of ExcludeArch)

* Mon Aug 28 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 2.0.3-3
- Add ExcludeArch: ppc64 s390x (no cld2 there)
- Use cld2-devel for language detection
- Add BuildRequires:  gcc-c++

* Wed Jul 26 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 2.0.3-1
- New upstream version
- Use cpprest-devel for Crowdin support

* Sat Jun 03 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 2.0.2-5
- Thanks to Wolfgang Stöggl <c72578@yahoo.de> for the following changes:
- Add upstream fix to enable opening of .po files again in Poedit 2.0.2
- Fix DrawRoundedRectangle assert with wxGTK 3.0
- Add dependency on json-devel (use json.hpp from Fedora and not the version
  bundled with Poedit
- Fixed spurious assert in wxGTK wxDataViewCtrl::EditItem()
- Compile with CLD2 language detection from copr c72578/cld2
- Compile with Crowdin integration using cpprest from copr c72578/cpprest
- Remove outdated BuildRequires

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon May 15 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 2.0.2-1
- New upstream version

* Fri May 12 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 2.0.1-1
- New upstream version

* Sun Feb 19 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.12-1
- New upstream version

* Sun Oct 30 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.11-1
- New upstream version

* Tue Oct 18 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.10-1
- New upstream version
- Add libappstream-glib to BuildRequires 
- Appdata file is now maintained upstream
- Use a better URL for the po file

* Fri Sep 02 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.9-1
- New upstream version
- Added latest features to the appdata file:
  translation hints, keywords, donations

* Wed Jun 01 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.8-1
- New upstream version

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.8.7.1-2
- rebuild for ICU 57.1

* Sat Feb 27 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.7.1-1
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Jonathan Wakely <jwakely@redhat.com> - 1.8.6-3
- Rebuilt for Boost 1.60

* Fri Jan 01 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.6-2
- Fixed appdata file

* Fri Jan 01 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.6-1
- New upstream version

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.8.5-2
- rebuild for ICU 56.1

* Sat Sep 26 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.5-1
- New upstream version

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.8.4-3
- Rebuilt for Boost 1.59

* Tue Aug 04 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.4-1
- New upstream version
- Updated screenshot for appdata

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.8.2-2
- rebuild for Boost 1.58

* Tue Jul 07 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.2-1
- New upstream version

* Thu May 28 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8.1-1
- New upstream version

* Thu May 21 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.8-1
- New upstream version

* Mon May 04 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.6-1
- New upstream version

* Thu Apr 02 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.5-2
- Rebuilt for latest versions of wxGTK3 and lucene++

* Fri Mar 13 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.5-1
- New upstream version
- Add screenshot URL to appdata file, thanks to Wolfgang Stöggl
- Updated German man page

* Thu Mar 05 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.4-1
- New upstream version

* Thu Jan 15 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.3-4
- Tweak appdata file and add German summary and description
- Spec file cleanup

* Wed Jan 14 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.3-3
- Add an appdata file
- Some spec file cleanup

* Wed Jan 14 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.3-2
- Disable non-working menu entries (backported from upstream's Git)
- Add an appdata file
- Some spec file cleanup

* Sat Jan 10 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.3-1
- New upstream version

* Thu Jan 08 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.1-3
- Remove the redundant zip from BuildRequires
- Fix directory ownership in %%{_datadir}/icons/hicolor/

* Fri Jan 02 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 1.7.1-2
- New upstream version
- Use the %%license macro
- Install German man page

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.5.4-9
- Rebuild for boost 1.55.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.5.4-7
- Rebuild for boost 1.54.0

* Wed Mar  6 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-6
- Remove vendor prefix from desktop files in F19+ https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.4-4
- Make sure translation memory gets built (#870724)

* Mon Oct 22 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.4-3
- Really fix file conflict, affects all sizes (#866058)

* Mon Oct 15 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.4-2
- Fix file conflict (#866058)

* Thu Oct 11 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.6.1-6
- Don't ship docs twice (#827472)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.4.6.1-4
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 1.4.6.1-2
- rebuilt against wxGTK-2.8.11-2

* Sat Apr 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.6.1-1
- Update to 1.4.6.1 (#579235)
- New BuildRequires boost-devel
- Update icon cache scriptlets

* Fri Feb 05 2010 Haïkel Guémar <karlthered@gmail.com> - 1.4.5-1
* Updated to 1.4.5

* Fri Jan 29 2010 Haïkel Guémar <karlthered@gmail.com> - 1.4.4-1
* Updated to 1.4.4

* Fri Sep 18 2009 Haïkel Guémar <karlthered@gmail.com> - 1.4.3-1
* Updated to 1.4.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Bill Nottingham <notting@redhat.com> - 1.4.2-4
- rebuild per bug #492193, releng ticket 1432

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.4.2-2
- We still need desktop-file-utils, just not the post/postun scriptlets

* Sat Dec 27 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.4.2-1
- Upstream 1.4.2
- Do not depend on desktop-file-utils (#463047)
- Fix source location

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.9-2
- Autorebuild for GCC 4.3

* Sun Dec 23 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.9-1
- Upstream 1.3.9
- Make sure all docs are utf-8

* Fri Aug 17 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.7-1
- Upstream 1.3.7
- Require gettext (#253228)

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.6-1.2
- Rebuild for new wx in devel

* Fri Nov 10 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.6-1.1
- Rebuild for newer db4 in devel

* Mon Oct 30 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.6-1
- Upstream 1.3.6

* Sun Oct 29 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.5-1
- Upstream 1.3.5

* Sun Sep 03 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.4-2.1
- FC6 rebuild

* Wed May 24 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.4-2
- Remove any potential places where makefile may create copies of 
  .desktop files and icons.

* Tue May 23 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.3.4-1
- Initial packaging
