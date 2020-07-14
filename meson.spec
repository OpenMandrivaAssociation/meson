Summary: A software build system
Name: meson
Version: 0.55.0
Release: 1
URL: http://mesonbuild.com/
License: Apache 2
Group: Development/Tools
Source0: https://github.com/mesonbuild/meson/archive/%{name}-%{version}.tar.gz
Patch0: meson-0.55.0-macros.patch
Patch1: meson-0.54.2-add-meson32-macro.patch
BuildRequires: python >= 3.0
BuildRequires: python3dist(setuptools)
BuildArch: noarch
Requires: ninja
Requires: python >= 3.0
Requires: python3dist(setuptools)

%description
Meson is an open source build system meant to be fast and
user friendly.

%prep
%autosetup -p1

%build
%py_build

%install
%py_install

# install meson rpm macro helper
install -D -m 0644 data/macros.%{name} %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.%{name}

%files
%{_bindir}/*
%{_prefix}/lib/python*/site-packages/meson*
%{_mandir}/*/*
%{_prefix}/lib/rpm/macros.d/macros.%{name}
%{_datadir}/polkit-1/actions/*.policy
