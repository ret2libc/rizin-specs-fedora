Name:           rizin
Summary:        UNIX-like reverse engineering framework and command-line tool-set
Version:        0.1.2
URL:            https://rizin.re/
VCS:            https://github.com/rizinorg/rizin

%global         gituser         rizinorg
%global         gitname         rizin
%global         rel             1

Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/v%{version}/%{name}-src-%{version}.tar.xz

License:        LGPLv3+ and GPLv2+ and BSD and MIT and ASL 2.0 and MPLv2.0 and zlib
# Rizin as a package is targeting to be licensed/compiled as LGPLv3+
# however during build for Fedora the GPL code is not omitted so effectively it
# is GPLv2+.
#
# Some code has originally different license:
# librz/asm/arch/ - GPLv2+, MIT, GPLv3
# librz/bin/format/pe/dotnet - Apache License Version 2.0
# librz/util/qrcode.c - MIT
# shlr/java - Apache 2.0
# shlr/sdb/src - MIT
# shlr/lz4 - 3 clause BSD (system installed shared lz4 is used instead)
# shlr/spp - MIT
# shlr/tcc - LGPLv2+
# shlr/udis86 - 2 clause BSD
# shlr/spp - MIT

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  file-devel
BuildRequires:  xxhash-devel
BuildRequires:  pkgconfig

BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(capstone) >= 3.0.4
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(openssl)

Requires:       %{name}-common = %{version}-%{release}

# Package contains several bundled libraries that are used in Fedora builds

# ./shlr/spp/README.md
# SPP stands for Simple Pre-Processor, a templating language.
# https://github.com/rizinorg/spp
Provides:       bundled(spp) = 1.2.0

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/rizinorg/sdb
Provides:       bundled(sdb) = 01e4bd15397394ed592eb436e9bf70f5ad585c5b

# ./shlr/sdb/src/json/README
# https://github.com/quartzjer/js0n
# JSON support for sdb
Provides:       bundled(js0n)

# librz/util/regex/README
# Modified OpenBSD regex to be portable
# cvs -qd anoncvs@anoncvs.ca.openbsd.org:/cvs get -P src/lib/libc/regex
# version from 2010/11/21 00:02:30, version of files ranges from v1.11 to v1.20
Provides:       bundled(openbsdregex) = 1.11

# ./shlr/tcc/README.md
# This is a stripped down version of tcc without the code generators and heavily modified.
Provides:       bundled(tcc) = 0.9.26

# ./librz/asm/arch/tricore/README.md
# Based on code from https://www.hightec-rt.com/en/downloads/sources/14-sources-for-tricore-v3-3-7-9-binutils-1.html
# part of binutils to read machine code for Tricore architecture
# ./librz/asm/arch/ppc/gnu/
# part of binutils to read machine code for ppc architecture
# ./librz/asm/arch/arm/gnu/
Provides:       bundled(binutils) = 2.13

# ./librz/asm/arch/avr/README
# * This code has been ripped from vavrdisasm 1.6
Provides:       bundled(vavrdisasm) = 1.6


%description
Rizin is a free and open-source Reverse Engineering framework, providing a
complete binary analysis experience with features like Disassembler,
Hexadecimal editor, Emulation, Binary inspection, Debugger, and more.

Rizin is a fork of radare2 with a focus on usability, working features and code
cleanliness.


%package devel
Summary:        Development files for the rizin package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       file-devel
Requires:       openssl-devel

%description devel
Development files for the rizin package. See rizin package for more
information.


%package common
Summary:        Arch-independent SDB files for the rizin package
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description common
Arch-independent SDB files used by rizin package. See rizin package for more
information


%prep
# Build from git release version
%setup -n %{gitname}-%{version}

%build
# Whereever possible use the system-wide libraries instead of bundles
%meson \
    -Duse_sys_magic=true \
    -Duse_sys_zip=true \
    -Duse_sys_zlib=true \
    -Duse_sys_lz4=true \
    -Duse_sys_xxhash=true \
    -Duse_sys_openssl=true \
    -Duse_libuv=true \
    -Duse_sys_capstone=true \
%ifarch s390x
    -Ddebugger=false \
%endif
    -Denable_tests=false \
    -Denable_rz_test=false \
    -Dlocal=disabled
%meson_build

%install
%meson_install
%ldconfig_scriptlets


%check
# Do not run the unit testsuite yet - it pulls another big repository
# https://github.com/rizinorg/rizin-testbins from github



%files
%doc CONTRIBUTING.md DEVELOPERS.md README.md SECURITY.md BUILDING.md
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/librz_*.so.%{version}*
%{_datadir}/%{name}/%{version}/fortunes/fortunes.*
%{_mandir}/man1/rizin.1.*
%{_mandir}/man1/rz*.1.*
%{_mandir}/man7/rz-esil.7.*


%files devel
%{_includedir}/librz
%{_libdir}/librz*.so
%{_libdir}/pkgconfig/*.pc


%files common
%{_datadir}/%{name}/%{version}/cons
%{_datadir}/%{name}/%{version}/fcnsign
%{_datadir}/%{name}/%{version}/flag
%{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/hud
%{_datadir}/%{name}/%{version}/magic
%{_datadir}/%{name}/%{version}/opcodes
%{_datadir}/%{name}/%{version}/syscall
%dir %{_datadir}/%{name}
%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/%{name}/%{version}


%changelog
* Tue Mar 30 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.1.2-1
- Initial SPEC file
