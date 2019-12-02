Summary: A fast build system
Name: meson
Version: 0.52.1
Release: 1
URL: http://mesonbuild.com/
License: Apache 2
Group: Development/Tools
Source0: https://github.com/mesonbuild/meson/archive/%{name}-%{version}.tar.gz
Patch0: meson-0.42.1-macros.patch
BuildRequires: python >= 3.0
BuildRequires: python3egg(setuptools)
BuildArch: noarch
Requires: ninja
Requires: python >= 3.0
Requires: python3egg(setuptools)
Requires: glibc

%description
Meson is an open source build system meant to be both extremely fast, and,
even more importantly, as user friendly as possible.

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

# install meson rpm macro helper
install -D -m 0644 data/macros.%{name} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

%files
%{_bindir}/*
%{_prefix}/lib/python*/site-packages/meson*
%{_mandir}/*/*
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_datadir}/polkit-1/actions/*.policy
