%define major 2
%define minor 9
Name:           cpprest
Version:        2.9.1
Release:        4%{?dist}
Summary:        C++ REST library
License:        MIT and BSD and zlib
# main: MIT (license.txt)
# Websocket++: New BSD (no advertising, 3 clause) (ThirdPartyNotices.txt)
# base64/base64.hpp: Zlib (ThirdPartyNotices.txt)
# sha1/sha1.hpp: New BSD (no advertising, 3 clause) (ThirdPartyNotices.txt)
# common/md5.hpp: zlib (ThirdPartyNotices.txt)
# utf8_validation.hpp: MIT (ThirdPartyNotices.txt)
Url:            https://github.com/Microsoft/cpprestsdk
Source0:        https://github.com/Microsoft/cpprestsdk/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  boost-devel >= 1.55
BuildRequires:  cmake >= 2.6
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel >= 1.0
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
%setup -q -n cpprestsdk-%{version}
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
%cmake -DCMAKE_BUILD_TYPE=Release
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_includedir}
cp -r Release/include/* %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_libdir}
cp Release/Binaries/libcpprest.so.%{major}.%{minor} %{buildroot}%{_libdir}/
ln -sf libcpprest.so.%{major}.%{minor} %{buildroot}%{_libdir}/libcpprest.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc CONTRIBUTORS.txt license.txt ThirdPartyNotices.txt
%{_libdir}/libcpprest.so.%{major}.%{minor}

%files devel
%doc CONTRIBUTORS.txt license.txt
%{_includedir}/%{name}
%{_includedir}/pplx
%{_libdir}/libcpprest.so


%changelog
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
