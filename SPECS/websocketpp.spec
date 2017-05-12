
Name:    websocketpp
Summary: C++ WebSocket Protocol Library
Version: 0.7.0
Release: 4%{?dist}

License: BSD
Url:     http://www.zaphoyd.com/websocketpp
Source0: https://github.com/zaphoyd/websocketpp/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: websocketpp.pc
BuildArch: noarch

# put cmake files in share/cmake instead of lib/cmake
Patch1: websocketpp-0.7.0-cmake_noarch.patch

%if 0%{?fedora} > 25
# This patch fixes compilation errors in F26 etc., which contain openssl >= 1.1
# SSL_R_SHORT_READ undefined in openssl-1.1
# See also https://github.com/zaphoyd/websocketpp/issues/599
# Commit: https://github.com/LocutusOfBorg/websocketpp/commit/1dd07113f2a7489444a8990a95be42e035f8e9df
Patch2: %{name}-Fix-issue-599.patch
%endif

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  pkgconfig

%description
WebSocket++ is an open source (BSD license) header only C++ library
that impliments RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.

%package devel
Summary:  C++ WebSocket Protocol Library
Requires: boost-devel
%description devel
WebSocket++ is an open source (BSD license) header only C++ library
that impliments RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.


%prep
%autosetup -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake ..

make %{?_smp_mflags}
popd


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files devel
%doc COPYING changelog.md readme.md roadmap.md
%{_includedir}/websocketpp/
%dir %{_datadir}/cmake/
%{_datadir}/cmake/websocketpp/


%changelog
* Fri May 12 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.7.0-4
- Added websocketpp-Fix-issue-599.patch
  Fixes compilation errors in F26 etc., which contain openssl >= 1.1
  SSL_R_SHORT_READ undefined in openssl-1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-2
- Rebuilt for Boost 1.63

* Thu Sep 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-1
- websocketpp-0.7.0 (#1375610)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.4.0-8
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.4.0-7
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.4.0-5
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.4.0-3
- Rebuild for boost 1.57.0

* Thu Nov 13 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- use (upstreamable) cmake_noarch.patch instead of manually moving files around

* Wed Nov 05 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- first try

* Mon Mar 17 2014 prusnak@opensuse.org
- created package (based on a Fedora package by Thomas Sailer)
