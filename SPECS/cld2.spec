%global githubproj CLD2Owners
%global githubrepo cld2

#For git snapshots, set to 0 to use release instead:
%global usesnapshot 1
%if 0%{?usesnapshot}
    %global commitdate0 20150821
    %global commit0 b56fa78a2fe44ac2851bae5bf4f4693a0644da7b
    %global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%endif

Name:           cld2
# When upstream has never chosen a version, you MUST use Version: 0.
Version:        0
Release:        0.8%{?usesnapshot:.%{commitdate0}git%{shortcommit0}}%{?dist}
Summary:        A library to detect the natural language of text
License:        ASL 2.0
URL:            https://github.com/CLD2Owners/cld2/
Source0:        https://github.com/%{githubproj}/%{githubrepo}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
# CMakeLists.txt originally from https://code.google.com/p/cld2/issues/detail?id=29
# Updated version 0.0.197 from Debian at https://sources.debian.net/src/cld2/0.0.0-git20150806-5/CMakeLists.txt/
# There is no CMakeLists.txt yet at https://github.com/CLD2Owners/cld2/
# Stored CMakeLists.txt 0.0.198 at own github repo for now
Source1:        https://raw.githubusercontent.com/c72578/rpmbuild/master/SOURCES/CMakeLists.txt
BuildRequires:  cmake >= 2.8

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
    %autosetup
%endif
cp %{SOURCE1} .

%build
mkdir build
cd build
# https://fedoraproject.org/wiki/Common_Rpmlint_issues#unused-direct-shlib-dependency
# Add Wl,--as-needed to CXX_FLAGS
# Fix build with gcc-6, build with -std=c++98. See Github, CLD2 issue #47
# https://github.com/CLD2Owners/cld2/issues/47
export CXXFLAGS="%{optflags} -std=c++98 -Wl,--as-needed"
%cmake .. -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir}
make %{?_smp_mflags}

%install
cd build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%check
cd build
# Tests from: internal/compile_and_test_all.sh
echo "this is some english text" | ./compact_lang_det_test_chrome_2
echo "this is some english text" | ./compact_lang_det_test_chrome_16
./cld2_unittest_chrome_2 > /dev/null
./cld2_unittest_avoid_chrome_2 > /dev/null
echo "this is some english text" | ./compact_lang_det_test_full
./cld2_unittest_full > /dev/null
./cld2_unittest_full_avoid > /dev/null
./cld2_dynamic_data_tool --dump cld2_data.bin
./cld2_dynamic_data_tool --verify cld2_data.bin
echo "this is some english text" | ./compact_lang_det_dynamic_test_chrome --data-file cld2_data.bin
./cld2_dynamic_unittest --data-file cld2_data.bin > /dev/null

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_libdir}/libcld2.so.*
%{_libdir}/libcld2_dynamic.so.*
%{_libdir}/libcld2_full.so.*

%files devel
%doc docs/*
%{_includedir}/%{name}
%{_libdir}/libcld2.so
%{_libdir}/libcld2_dynamic.so
%{_libdir}/libcld2_full.so

%changelog
* Thu Aug 10 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0-0.8.20150821gitb56fa78
- Modifications according to package review (#1441728)
- Removed license file from devel package

* Sun Jun 04 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0-0.7.20150821gitb56fa78
- Change version of package from 0.0.0 to 0
- Added date of git commit to <snapinfo>

* Fri Jun 02 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.6.gitb56fa78
- Removed BR: gcc-c++
- Added check section and tests

* Wed May 24 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.5.gitb56fa78
- Use license macro for LICENSE
- Add doc README.md

* Fri May 05 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.4.gitb56fa78
- Simplify cmake, use cmake macro

* Wed May 03 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.3.gitb56fa78
- Fix unused-direct-shlib-dependency reported by rpmlint (installed packages)
- Update CMakeLists.txt to version 0.0.198, to avoid
  shared-lib-without-dependency-information of libcld2_full

* Wed May 03 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.2.gitb56fa78
- Modifications to spec file
- Remove sub-package libcld2. Names for rpms are cld2 and cld2-devel now
- Updated version of CMakeLists.txt

* Wed Apr 12 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0-0.1.gitb56fa78
- Update to newer git snapshot

* Tue Apr 11 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.0.0~svn195-1
- Initial Fedora packaging.

