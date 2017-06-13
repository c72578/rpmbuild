
Name:    websocketpp
Summary: C++ WebSocket Protocol Library
Version: 0.7.0
Release: 7%{?dist}

License: BSD
Url:     http://www.zaphoyd.com/websocketpp
Source0: https://github.com/zaphoyd/websocketpp/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: websocketpp.pc
BuildArch: noarch

# put cmake files in share/cmake instead of lib/cmake
Patch1: websocketpp-0.7.0-cmake_noarch.patch

# make compatible with openssl-1.1.x
# https://github.com/zaphoyd/websocketpp/issues/599
Patch2: websocketpp-0.7.0-openssl11.patch

# Fix build and test failures with zlib 1.2.11. Fixes test_permessage_deflate
# https://github.com/zaphoyd/websocketpp/issues/653
# Upstream patches, backported to websocketpp-0.7.0
# https://github.com/zaphoyd/websocketpp/commit/9ddb300d874a30db35e3ad58f188944bef0bf31b
Patch3: websocketpp-0.7.0-zlib-permessage-deflate.patch
# https://github.com/zaphoyd/websocketpp/commit/4cab5e5c0c5f19fcee7d37b4a38b156d63a150d4
Patch4: websocketpp-0.7.0-minor-adjustments-to-recent-extension-negotiation.patch

# Disable the following tests, which fail occasionally: test_transport, test_transport_asio_timers
Patch5: websocketpp-0.7.0-disable-test_transport-test_transport_asio_timers.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
# needed for tests mostly
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

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
%cmake .. \
  -DBUILD_TESTS:BOOL=ON

make %{?_smp_mflags}
popd


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
rm -rfv %{buildroot}%{_includedir}/test_connection/


%check
make test -C %{_target_platform}


%files devel
%doc changelog.md readme.md roadmap.md
%license COPYING
%{_includedir}/websocketpp/
%dir %{_datadir}/cmake/
%{_datadir}/cmake/websocketpp/


%changelog
* Tue Jun 13 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.7.0-7
- Add patches to fix zlib test failure (test_permessage_deflate)
- Disable tests test_transport, test_transport_asio_timers

* Fri May 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-6
- explicitly use openssl-devel (instead of generic 'pkgconfig(openssl)'

* Mon May 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-5
- adjust openssl patch
- BR: openssl-devel zlib-devel (for tests mostly)

* Wed May 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-4
- tls.hpp, SSL_R_SHORT_READ undefined in openssl-1.1 (#1449163)
- enable tests

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
