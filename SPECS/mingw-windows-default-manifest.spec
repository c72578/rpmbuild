%?mingw_package_header

Name:           mingw-windows-default-manifest
Version:        6.4
Release:        0.2%{?dist}
Summary:        MinGW Default Windows application manifest

# The source code is FSFAP (see COPYING) except install-sh which is MIT/X11
License:        FSFAP and MIT

# https://cygwin.com/git/?p=cygwin-apps/windows-default-manifest.git;a=summary
URL:            https://cygwin.com/

# How to generate the tarball used in the rpm:
# wget https://cygwin.com/pub/cygwin/x86/release/windows-default-manifest/windows-default-manifest-6.4-1-src.tar.xz
# extract windows-default-manifest-6.4.tar.bz2
# tar -xvf windows-default-manifest-6.4-1-src.tar.xz windows-default-manifest-6.4-1.src/windows-default-manifest-6.4.tar.bz2 --strip=1
Source0:        windows-default-manifest-6.4.tar.bz2

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils


%description
The Default Windows application manifest is linked to applications by
default to claim compatibility with the latest Windows versions.
The package version number reflects the latest Windows kernel version
supported by this manifest.

This package contains the MinGW Windows cross compiled default Windows
application manifest.

# Win32
%package -n mingw32-windows-default-manifest
Summary:        MinGW Default Windows application manifest

%description -n mingw32-windows-default-manifest
The Default Windows application manifest is linked to applications by
default to claim compatibility with the latest Windows versions.
The package version number reflects the latest Windows kernel version
supported by this manifest.

This package contains the MinGW Windows cross compiled default Windows
application manifest.

# Win64
%package -n mingw64-windows-default-manifest
Summary:        MinGW Default Windows application manifest

%description -n mingw64-windows-default-manifest
The Default Windows application manifest is linked to applications by
default to claim compatibility with the latest Windows versions.
The package version number reflects the latest Windows kernel version
supported by this manifest.

This package contains the MinGW Windows cross compiled default Windows
application manifest.


%prep
%setup -q -n windows-default-manifest


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# Win32
%files -n mingw32-windows-default-manifest
%doc README
%license COPYING

%{mingw32_libdir}/default-manifest.o

# Win64
%files -n mingw64-windows-default-manifest
%doc README
%license COPYING
%{mingw64_libdir}/default-manifest.o

%changelog
* Fri Mar 23 2018 Wolfgang Stöggl <c72578@yahoo.de> - 6.4-0.2
- Add license details for MIT/X11

* Wed Mar 21 2018 Wolfgang Stöggl <c72578@yahoo.de> - 6.4-0.1
- Initial Fedora RPM release
