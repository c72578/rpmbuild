%global srcname wxWidgets
%global wxgtkname wxGTK3
%global wxbasename wxBase3
#RHEL 6 does not have gtk3
#RHEL prior to 6 is unsupported by this package
%if 0%{?el6}
%global gtkver 2
%else
%global gtkver 3
%endif

#For git snapshots, set to 0 to use release instead:
%global usesnapshot 0
%if 0%{?usesnapshot}
%global commit0 3fa996453f47f06141e8049fde203e08742aeaa0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#What doc version to use with the snapshot (usually last release):
%global builddocs 1
%endif

Name:           %{wxgtkname}
Version:        3.0.3
Release:        1%{?dist}
Summary:        GTK port of the wxWidgets GUI library
License:        wxWidgets
Group:          System Environment/Libraries
URL:            http://www.wxwidgets.org/

%if 0%{?usesnapshot}
Source0:        https://github.com/%{srcname}/%{srcname}/archive/%{commit0}.tar.gz#/%{srcname}-%{shortcommit0}.tar.gz
%else
Source0:        https://github.com/%{srcname}/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.bz2
%endif
%if ! 0%{?builddocs}
Source1:        https://github.com/%{srcname}/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}-docs-html.tar.bz2
%endif
Source10:       wx-config
# https://bugzilla.redhat.com/show_bug.cgi?id=1225148
# remove abort when ABI check fails
# Backport from wxGTK
Patch0:         %{name}-%{version}-abicheck.patch
# Temporary patch to port to webkit2gtk
%if 0%{?fedora} > 26
Patch1:         %{name}-%{version}-webkit2.patch
%endif

BuildRequires:  gtk%{gtkver}-devel
#Note webkitgtk (GTK2) does not appear to be supported
%if %{gtkver} == 3
%if 0%{?fedora} < 27
BuildRequires:  webkitgtk3-devel
%else
BuildRequires:  webkitgtk4-devel
%endif
%endif
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  expat-devel
BuildRequires:  SDL2-devel
BuildRequires:  libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  GConf2-devel
BuildRequires:  gettext
BuildRequires:  cppunit-devel
BuildRequires:  libmspack-devel
BuildRequires:  doxygen

Provides:       %{srcname} = %{version}-%{release}
Provides:       bundled(scintilla) = 3.2.1
Requires:       %{wxbasename}%{?_isa} = %{version}-%{release}

%description
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        devel
Group:          Development/Libraries
Summary:        Development files for the wxGTK3 library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-gl = %{version}-%{release}
Requires:       %{name}-media = %{version}-%{release}
%if 0%{?fedora} > 25
Requires:       %{name}-webview = %{version}-%{release}
%endif
Requires:       %{wxbasename} = %{version}-%{release}
Requires:       gtk%{gtkver}-devel
Requires:       libGLU-devel
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:       %{srcname}-devel = %{version}-%{release}

%description devel
This package include files needed to link with the wxGTK3 library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        gl
Summary:        OpenGL add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gl
OpenGL (a 3D graphics API) add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        media
Summary:        Multimedia add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description media
Multimedia add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%if 0%{?fedora} > 25
%package        webview
Summary:        WebView add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description webview
WebView add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.
%endif


%package -n     %{wxbasename}
Summary:        Non-GUI support classes from the wxWidgets library
Group:          System Environment/Libraries

%description -n %{wxbasename}
Every wxWidgets application must link against this library. It contains
mandatory classes that any wxWidgets code depends on (like wxString) and
portability classes that abstract differences between platforms. wxBase can
be used to develop console mode applications -- it does not require any GUI
libraries or the X Window System.


%package        docs
Group:          Development/Libraries
Summary:        Documentation for the wxGTK3 library
Requires:       %{name} = %{version}-%{release}
Provides:       %{srcname}-docs = %{version}-%{release}
BuildArch:      noarch

%description docs
This package provides documentation for the %{srcname} library.


%package        xmldocs
Group:          Development/Libraries
Summary:        XML Documentation for the wxGTK3 library
Requires:       %{name} = %{version}-%{release}
Provides:       %{srcname}-xmldocs = %{version}-%{release}
BuildArch:      noarch

%description xmldocs
This package provides XML documentation for the %{srcname} library.


%prep
%if 0%{?usesnapshot}
%autosetup -n %{srcname}-%{commit0} %{!?builddocs:-a 1} -p1
%else
%autosetup -n %{srcname}-%{version} -a 1 -p1
%endif

# Run autogen since we're patching configure.in
./autogen.sh

# patch some installed files to avoid conflicts with 2.8.*
sed -i -e 's|aclocal)|aclocal/wxwin3.m4)|' Makefile.in
sed -i -e 's|wxstd.mo|wxstd3.mo|' Makefile.in
sed -i -e 's|wxmsw.mo|wxmsw3.mo|' Makefile.in

# fix plugin dir for 64-bit
sed -i -e 's|/usr/lib\b|%{_libdir}|' wx-config.in configure
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

# Trick configure into using pkg-config for cppunit-config
sed -i -e 's|$CPPUNIT_CONFIG --version|$CPPUNIT_CONFIG --modversion|' configure


%build
# likely still dereferences type-punned pointers
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
# fix unused-direct-shlib-dependency error:
export LDFLAGS="-Wl,--as-needed"
# Trick configure into using pkg-config for cppunit-config
export CPPUNIT_CONFIG="/usr/bin/pkg-config cppunit"
# Trick configure into building with SDL2
export SDL_CONFIG=/usr/bin/sdl2-config

%if 0%{?usesnapshot}
#For snapshots, mo files need to be generated
pushd locale
make allmo
popd
%endif

%configure \
  --with-gtk=%{gtkver} \
  --with-opengl \
  --with-sdl \
  --with-gnomeprint \
  --with-libmspack \
  --enable-intl \
  --enable-no_deps \
  --disable-rpath \
  --enable-ipv6

%make_build

#Docs
%if 0%{?builddocs}
WX_SKIP_DOXYGEN_VERSION_CHECK=1 docs/doxygen/regen.sh html
mv docs/doxygen/out/html .
%else
# wxWidgets-3.0.2
# wxWidgets-3.0.3-docs-html
mv %{srcname}-%{version}-docs-html html
%endif

pushd docs/doxygen
WX_SKIP_DOXYGEN_VERSION_CHECK=1 ./regen.sh xml
popd

%install
%makeinstall

# install our multilib-aware wrapper
##Remove installed
rm %{buildroot}%{_bindir}/wx-config
##Install new and symlink
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/%{name}/wx-config
ln -s ../..%{_libexecdir}/%{name}/wx-config %{buildroot}%{_bindir}/wx-config-3.0
touch %{buildroot}%{_bindir}/wx-config
##If gtk2
%if %{gtkver} == 2
sed -i -e 's|gtk3|gtk2|' %{buildroot}%{_libexecdir}/%{name}/wx-config
%endif

#Alternatives setup with wxrc
mv %{buildroot}%{_bindir}/wxrc* %{buildroot}%{_libexecdir}/%{name}
ln -s ../..%{_libexecdir}/%{name}/wxrc-3.0 %{buildroot}%{_bindir}/wxrc-3.0
touch %{buildroot}%{_bindir}/wxrc

# move bakefiles to avoid conflicts with 2.8.*
mkdir %{buildroot}%{_datadir}/bakefile/presets/wx3
mv %{buildroot}%{_datadir}/bakefile/presets/*.* %{buildroot}%{_datadir}/bakefile/presets/wx3

%find_lang wxstd3
%find_lang wxmsw3
cat wxmsw3.lang >> wxstd3.lang

%check
pushd tests
make %{?_smp_mflags} test
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gl -p /sbin/ldconfig
%postun gl -p /sbin/ldconfig

%post media -p /sbin/ldconfig
%postun media -p /sbin/ldconfig

%if 0%{?fedora} > 25
%post webview -p /sbin/ldconfig
%postun webview -p /sbin/ldconfig
%endif

%post -n %{wxbasename} -p /sbin/ldconfig
%postun -n %{wxbasename} -p /sbin/ldconfig

%post devel
if [ -f %{_bindir}/wx-config ] && [ ! -h %{_bindir}/wx-config ] ; then
  rm %{_bindir}/wx-config
fi
%{_sbindir}/update-alternatives --install %{_bindir}/wx-config \
  wx-config %{_libexecdir}/%{name}/wx-config 3
%{_sbindir}/update-alternatives --install %{_bindir}/wxrc \
  wxrc %{_libexecdir}/%{name}/wxrc 3

%postun devel
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove wx-config %{_libexecdir}/%{name}/wx-config
  %{_sbindir}/update-alternatives --remove wxrc %{_libexecdir}/%{name}/wxrc
fi

%files -f wxstd3.lang
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_gtk%{gtkver}u_adv-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_aui-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_core-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_html-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_propgrid-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_qa-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_ribbon-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_richtext-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_stc-*.so.*
%if %{gtkver} == 3
%if 0%{?fedora} < 26
%{_libdir}/libwx_gtk%{gtkver}u_webview-*.so.*
%endif
%endif
%{_libdir}/libwx_gtk%{gtkver}u_xrc-*.so.*

%files devel
%ghost %{_bindir}/wx-config
%ghost %{_bindir}/wxrc
%{_bindir}/wxrc-3.0
%{_bindir}/wx-config-3.0
%{_includedir}/wx-3.0
%{_libdir}/libwx_*.so
%{_libdir}/wx
%{_datadir}/aclocal/wxwin3.m4
%{_datadir}/bakefile/presets/wx3
#Exclude some python bitecode
%exclude %{_datadir}/bakefile/presets/wx3/*.pyc
%exclude %{_datadir}/bakefile/presets/wx3/*.pyo
%{_libexecdir}/%{name}

%files gl
%{_libdir}/libwx_gtk%{gtkver}u_gl-*.so.*

%files media
%{_libdir}/libwx_gtk%{gtkver}u_media-*.so.*

%if 0%{?fedora} > 25
%files webview
%{_libdir}/libwx_gtk%{gtkver}u_webview-*.so.*
%endif

%files -n %{wxbasename}
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.*
%{_libdir}/libwx_baseu_xml-*.so.*

%files docs
%doc html

%files xmldocs
%doc docs/doxygen/out/xml/*

%changelog
* Tue May 02 2017 Wolfgang Stöggl <c72578@yahoo.de> - 3.0.3-1
- Update to 3.0.3

* Fri Apr 28 2017 Wolfgang Stöggl <c72578@yahoo.de> - 3.0.3-0.9.git3fa9964
- Update to newer git snapshot

* Mon Apr 17 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.8.gite4293e9
- Rebuild against SDL2

* Wed Mar 08 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.7.gite4293e9
- Update to newer git snapshot
- Remove GStreamer patch as it has been incorporated upstream

* Sun Mar 05 2017 Scott Talbert <swt@techie.net> - 3.0.3-0.6.gitf90b768
- Add temporary patch for webkit2 port in rawhide, re-enable webview subpackage

* Thu Mar 02 2017 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.3-0.5.gitf90b768
- Disable webview subpackage in rawhide for now

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-0.4.gitf90b768
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Scott Talbert <swt@techie.net> - 3.0.3-0.3.gitf90b768
- Switch to use GStreamer 1.0 (#1402628)

* Wed Dec 28 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.3-0.2.gitf90b768
- Update to newer git snapshot

* Sat Dec 10 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.3-0.1.git9518d52
- Update to git snapshot

* Mon Nov 21 2016 Scott Talbert <swt@techie.net> - 3.0.2-30
- Fix poedit regression in -29 - add paint clipping region patch (#1396747)
- Add patch to change ~wxPGChoicesData from private to protected

* Mon Nov 14 2016 Scott Talbert <swt@techie.net> - 3.0.2-29
- Fix some sizing problems with GTK3 (#1392102)
- Fix non-default window background color with GTK+ >= 3.20 (#1393847)

* Mon Oct 10 2016 Scott Talbert <swt@techie.net> - 3.0.2-28
- Fix rename issues in Filezilla with overlay scrollbars disabled (#1381765)

* Sat Oct 08 2016 Scott Talbert <swt@techie.net> - 3.0.2-27
- Add a -webview subpackage in F26+

* Tue Oct 04 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-26
- Memory leak in last patch, add patch to fix it
- Change last patch to 3.0 branch for consistency

* Tue Oct 04 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-25
- Add patch to fix bug 1381767
- Clean up spec file with autosetup

* Sat Sep 24 2016 Scott Talbert <swt@techie.net> - 3.0.2-24
- Add patch to fix crash in wxGCDC::DrawEllipticArc()

* Mon Sep 19 2016 Scott Talbert <swt@techie.net> - 3.0.2-23
- Fix alternatives implementation

* Mon Sep 19 2016 Scott Talbert <swt@techie.net> - 3.0.2-22
- Add patch to fix runtime link error due to previous patches

* Tue Sep 13 2016 Scott Talbert <swt@techie.net> - 3.0.2-21
- Add patch to resolve wxGetKeyState() crash on Wayland (#1266743)
- Add patch to fix wxFontEnumerator stop function
- Add patch to fix wxNativeFontInfo::InitFromFont()

* Sun Aug 28 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-20
- Fix alternatives with wxGTK (#1077718)

* Mon Apr  4 2016 Tom Callaway <tcallawa@redhat.com> - 3.0.2-19
- Add patch to resolve window sizing issue with gtk 3.19+

* Sun Mar 20 2016 Scott Talbert <swt@techie.net> - 3.0.2-18
- Add patch for wxEVT_MEDIA_XXX event types (for Phoenix)

* Wed Feb 24 2016 Scott Talbert <swt@techie.net> - 3.0.2-17
- Add patch to resolve issue with wxStaticText growing, fixes RH#1282142
- Add patches to resolve issues under Wayland with window sizing, RH#1294229

* Tue Feb 23 2016 Scott Talbert <swt@techie.net> - 3.0.2-16
- Add -xmldocs subpackage containing XML documentation (needed for Phoenix)

* Tue Feb 23 2016 Scott Talbert <swt@techie.net> - 3.0.2-15
- Add GCC6 patches for STC and strings tests
- Adapt cppunit to use pkg-config (cppunit-config has been removed in F24)
- Fixes FTBFS in F24 Rawhide, RH#1308244

* Mon Feb 22 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-14
- Should actually fix RH#1294712

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 31 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-12
- Remove python artifacts in bakefile dir, causes multilib devel conflict RH#1294712
- Fix package devel not owning created wx3 backfile preset dir
- Add support for MIPS to wx-config RH#1294895
- Wayland Patch

* Thu Nov 5 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-11
- Added patch to fix checkbox and radio button issues for f21 onwards

* Sun Nov 1 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-10
- Removed depreciated/retired libgnomeprintui22

* Sat Aug 22 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-9
- Include spinbutton patch from upstream

* Mon Jun 22 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-8
- Include some upstream patches to fix crashes and warnings

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.2-6
- Don't abort on ABI check, backport from wxGTK

* Mon May 04 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 3.0.2-5
- Indicate that this package bundles scintilla 3.2.1.

* Thu Feb 26 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-4
- Bump to rebuild, fix bug #1210239

* Thu Feb 26 2015 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-3
- Bump to rebuild for gcc 5.0 to fix some issues

* Tue Nov 04 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-2
- Moving things around again, hopefully fixing RH#1124402
- Adding symlinks to avoid breaking things

* Tue Nov 04 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.2-1
- Update to 3.0.2

* Mon Nov 03 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.0.1-5
- Add aarch64 and ppc64le to list of 64-bit architectures

* Tue Sep 30 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.1-4
- Add conflict with wxgtk-devel again, temporary fix until it can be resolved

* Tue Sep 30 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.1-3
- Avoid gtk warnings, fixes RH#1147995
- Moving wxrc and wx-config to libexec instead of renaming
- Misc changes and spec error fixes, fixes RH#1124402

* Sat Jul 5 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.1-1
- Bump to 3.0.1 RH#1076617

* Tue Mar 18 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-6
- Removed disable-catch_segvs, see RH#1076617

* Mon Mar 17 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-5
- Renable combat28 - without it causes bugs RH#1076617 and a few others

* Wed Feb 19 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-4
- Fixed GTK3 bug with wx-config
- Fixed a unused-direct-shlib-dependency error

* Mon Feb 17 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-3
- Added patch to avoid build fail on gtk 3.10+
- Reverted patching to make devel package compatible with wxGTK-devel
- Added combatibility for RHEL 6+
- Changed all mention of GTK3 and GTK2 to GTK for consistency

* Mon Feb 10 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-2
- Changed to build against gtk3
- Add webkit to build requires
- Removed patching to make devel package compatible with wxGTK-devel
- Disable 2.8.* combatibility (redundant functionality)

* Sat Jan 4 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 3.0.0-1
- Initial build of wxwidgets version 3, mostly based on wxGTK spec
