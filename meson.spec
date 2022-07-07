Summary: A software build system
Name: meson
Version:	0.63.0
Release:	1
URL: http://mesonbuild.com/
License: Apache-2.0
Group: Development/Tools
Source0: https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
Patch0: meson-0.42.1-macros.patch
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
install -D -m 0644 data/macros.%{name} %{buildroot}%{_rpmmacrodir}/macros.%{name}

%files
%{_bindir}/*
%dir %{python3_sitelib}/mesonbuild
%{python3_sitelib}/mesonbuild/*
%{python3_sitelib}/%{name}-*.egg-info
%doc %{_mandir}/*/*
%{_rpmmacrodir}/macros.%{name}
%{_datadir}/polkit-1/actions/*.policy
