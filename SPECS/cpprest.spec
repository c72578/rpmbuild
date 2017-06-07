%define major 2
%define minor 9
Name:           cpprest
Version:        2.9.1
Release:        12%{?dist}
Summary:        C++ REST library
License:        MIT
Url:            https://github.com/Microsoft/cpprestsdk
Source0:        https://github.com/Microsoft/cpprestsdk/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Patch1 https://github.com/Microsoft/cpprestsdk/pull/285
# Fix build issue with openssl-1.1
Patch1:         cpprest-2.9.1-openssl-1.1.patch
# Disable outside/failing tests
# https://github.com/Microsoft/cpprestsdk/issues/27
Patch2:         cpprest-2.9.1-disable-outside-tests.patch
BuildRequires:  boost-devel >= 1.55
BuildRequires:  cmake >= 2.6
BuildRequires:  openssl-devel >= 1.0
# BuildRequires:  pkgconfig(openssl) >= 1.0
# Current websockettpp versions: 0.4 (F24), 0.7 (>= F25), 0.5.1 (embedded in cpprestsdk 2.9.1)
BuildRequires:  websocketpp-devel >= 0.4
# PR submitted upstream: Change end-of-line encoding of two files to Unix (LF)
# https://github.com/Microsoft/cpprestsdk/pull/429
BuildRequires:  dos2unix

%description
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Also known as Casablanca.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Development files.

%prep
%autosetup -n cpprestsdk-%{version} -p1
# Convert ThirdPartyNotices.txt to utf-8
iconv -f iso-8859-15 -t utf-8 ThirdPartyNotices.txt > ThirdPartyNotices.txt.tmp
touch -r ThirdPartyNotices.txt ThirdPartyNotices.txt.tmp
mv -f ThirdPartyNotices.txt.tmp ThirdPartyNotices.txt
# Change end-of-line encoding to Unix (LF)
dos2unix -k Release/src/http/oauth/oauth1.cpp
dos2unix -k Release/libs/websocketpp/websocketpp/sha1/sha1.hpp
# Remove spurious-executable-perm
chmod -x Release/include/cpprest/oauth1.h
chmod -x Release/libs/websocketpp/websocketpp/sha1/sha1.hpp
chmod -x Release/src/http/oauth/oauth1.cpp

%build
cd Release
# https://fedoraproject.org/wiki/Common_Rpmlint_issues#unused-direct-shlib-dependency
# -Wl,--as-needed
mkdir build.release
cd build.release
export CXXFLAGS="%{optflags} -Wl,--as-needed"
# Set CMAKE_INCLUDE_PATH where websocketpp is installed in Fedora
%cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INCLUDE_PATH=/usr/share/cmake/websocketpp/
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_includedir}
cp -r Release/include/* %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_libdir}
cp Release/build.release/Binaries/libcpprest.so.%{major}.%{minor} %{buildroot}%{_libdir}/
ln -sf libcpprest.so.%{major}.%{minor} %{buildroot}%{_libdir}/libcpprest.so

%check
cd Release/build.release/Binaries
./test_runner *_test.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc CONTRIBUTORS.txt
%license license.txt
%{_libdir}/libcpprest.so.%{major}.%{minor}

%files devel
%doc CONTRIBUTORS.txt
%license license.txt
%{_includedir}/%{name}
%{_includedir}/pplx
%{_libdir}/libcpprest.so


%changelog

* Wed Jun 07 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-12
- Removed BR: gcc-c++
- Added check section and tests
- Add patch to disable outside/failing tests

* Mon May 29 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-11
- Explicitly require openssl-devel instead of pkgconfig(openssl), so we
  build against OpenSSL 1.1 on F26 and rawhide and not compat-openssl10.

* Wed May 24 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-10
- Apply cpprest-2.9.1-openssl-1.1.patch anyway, remove the condition
  fedora > 25, which is not needed

* Tue May 23 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-9
- Rebuild using websocketpp-0.7.0-5.fc26 for F26 and rawhide
- Rename patch file including version of cpprest
- Set license to MIT. This is the license of C++ REST SDK (license.txt).
  Websocket++ is a separate Fedora package (websocketpp-devel) and its 
  license is handled there.
- Use BuildRequires: pkgconfig(openssl) instead of openssl-devel

* Thu May 18 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-8
- Rebuild for testing websocketpp-0.7.0-4.fc26

* Tue May 09 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-7
- Add requirement websocketpp-devel.
  Build against the Fedora websocketpp package and not the embedded version of cpprest.
- Add -DCMAKE_INCLUDE_PATH=/usr/share/cmake/websocketpp/ so that websocketpp is found
- Add patch cpprest-Fix-build-issue-with-openssl-1.1-From-Kurt-Roeckx

* Fri May 05 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-6
- Use directory build.release for cmake

* Sun Apr 30 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-5
- Fix unused-direct-shlib-dependency reported by rpmlint (installed packages)

* Sat Apr 29 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-4
- Updated spec file
- Remove spurious-executable-perm earlier in spec file (after setup)
- Change end-of-line encoding of two files to Unix (LF)

* Fri Apr 28 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-3
- Updated spec file
- Changed Source0 filename from v2.9.1.tar.gz to cpprest-2.9.1.tar.gz
- Convert ThirdPartyNotices.txt to utf-8

* Tue Apr 25 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-2
- Updated spec file according to package review feedback from:
  https://bugzilla.redhat.com/show_bug.cgi?id=1440704#c3

* Wed Apr 05 2017 Wolfgang Stöggl <c72578@yahoo.de> - 2.9.1-1
- Initial packaging
