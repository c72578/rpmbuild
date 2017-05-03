%global githubproj CLD2Owners
%global githubrepo cld2

#For git snapshots, set to 0 to use release instead:
%global usesnapshot 1
%if 0%{?usesnapshot}
    %global commit0 b56fa78a2fe44ac2851bae5bf4f4693a0644da7b
    %global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%endif

Name:           cld2
Version:        0.0.0
Release:        0.2%{?usesnapshot:.git%{shortcommit0}}%{?dist}
Summary:        A library to detect the natural language of text
License:        ASL 2.0
URL:            https://github.com/CLD2Owners/cld2/
Source0:        https://github.com/%{githubproj}/%{githubrepo}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
# CMakeLists.txt originally from https://code.google.com/p/cld2/issues/detail?id=29
# Updated version 0.0.197 from Debian at https://sources.debian.net/src/cld2/0.0.0-git20150806-5/CMakeLists.txt/
# There is no CMakeLists.txt yet at https://github.com/CLD2Owners/cld2/
# Stored CMakeLists.txt 0.0.198 at github repo for now
Source1:        https://raw.githubusercontent.com/c72578/rpmbuild/master/SOURCES/CMakeLists.txt
BuildRequires:  cmake >= 2.8
BuildRequires:  gcc-c++

%description
A library that detects over 80 languages in UTF-8 text, based largely
on groups of four letters. Also tables for 160+ language versions.

%package devel
Summary:        Development files for cld2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
A library that detects over 80 languages in UTF-8 text, based largely
on groups of four letters. Also tables for 160+ language versions.

This sub-package contains the headers for cld2.

%prep
%if 0%{?usesnapshot}
    %autosetup -n %name-%{commit0}
%else
    %setup -q
%endif
cp %{SOURCE1} .

%build
mkdir build
cd build
# Fix build with gcc-6, build with -std=c++98. See Github, CLD2 issue #47
# https://github.com/CLD2Owners/cld2/issues/47
cmake .. \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DCMAKE_BUILD_TYPE=release \
    -DCMAKE_SKIP_RPATH:BOOL=ON \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
    -DCMAKE_C_FLAGS:STRING="%{optflags}" \
    -DCMAKE_CXX_FLAGS:STRING="%{optflags} -std=c++98"
make %{?_smp_mflags}

%install
cd build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/libcld2.so.*
%{_libdir}/libcld2_dynamic.so.*
%{_libdir}/libcld2_full.so.*

%files devel
%doc LICENSE docs/*
%{_includedir}/%{name}
%{_libdir}/libcld2.so
%{_libdir}/libcld2_dynamic.so
%{_libdir}/libcld2_full.so

%changelog
* Wed May 03 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.2.gitb56fa78
- Modifications to spec file
- Remove sub-package libcld2. Names for rpms are cld2 and cld2-devel now
- Updated version of CMakeLists.txt

* Wed Apr 12 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.1.gitb56fa78
- Update to newer git snapshot

* Tue Apr 11 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0~svn195-1
- Initial Fedora packaging.
- Adapted from Opensuse cld2-0.0.0~svn195-2.3.src.rpm
  http://download.opensuse.org/repositories/openSUSE:/Factory/standard/src/cld2-0.0.0~svn195-2.3.src.rpm

* Tue Jun 21 2016 astieger@suse.com
- fix build with gcc6 in Factory, build with -std=c++98 boo#985158

* Wed May 27 2015 astieger@suse.com
- initial version
