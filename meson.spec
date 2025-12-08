%undefine _debugsource_packages

# Keep this in sync with the list of cross tools we build
# in other packages (binutils, gcc, ...)
%global targets aarch64-linux armv7hnl-linux i686-linux x86_64-linux x32-linux riscv32-linux riscv64-linux aarch64-linuxmusl armv7hnl-linuxmusl i686-linuxmusl x86_64-linuxmusl x32-linuxmusl riscv32-linuxmusl riscv64-linuxmusl aarch64-linuxuclibc armv7hnl-linuxuclibc i686-linuxuclibc x86_64-linuxuclibc x32-linuxuclibc riscv32-linuxuclibc riscv64-linuxuclibc aarch64-android armv7l-android armv8l-android x86_64-android i686-mingw32 x86_64-mingw32 ppc64le-linux ppc64le-linuxmusl ppc64le-linuxuclibc ppc64-linux ppc64-linuxmusl ppc64-linuxuclibc loongarch64-linux loongarch64-linuxmusl loongarch64-linuxuclibc
%global long_targets %(
	for i in %{targets}; do
		CPU=$(echo $i |cut -d- -f1)
		OS=$(echo $i |cut -d- -f2)
		echo -n "$(rpm --target=${CPU}-${OS} -E %%{_target_platform}) "
	done
)

Summary: A software build system
Name: meson
Version: 1.9.2
Release: 2
URL: https://mesonbuild.com/
License: Apache-2.0
Group: Development/Tools
Source0: https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
Source1: macros.buildsys.meson
Patch0: meson-0.42.1-macros.patch
Patch1: meson-0.54.2-add-meson32-macro.patch
Patch2: meson-1.0.1-crosscompile-macros.patch
BuildRequires: python >= 3.0
BuildRequires: python%{pyver}dist(pip)
BuildArch: noarch
Requires: ninja
Requires: python >= 3.0
Requires: python%{pyver}dist(pip)

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
install -D -m 0644 %{S:1} %{buildroot}%{_rpmmacrodir}/macros.buildsys.%{name}

# Create toolchain files for supported and semi-supported
# crosscompilers...
mkdir -p %{buildroot}%{_datadir}/meson/toolchains
for i in %{long_targets}; do
	CPU=$(echo ${i}|cut -d- -f1)
	ARCH=$CPU
	OS=$(echo ${i}|cut -d- -f3)
	ENDIAN=little
	EXTRAS_binaries=""
	EXTRAS_host_machine=""
	case $ARCH in
	arm*)
		ARCH=arm
		;;
	i?86|pentium?|athlon)
		ARCH=x86
		;;
	znver*|x86_64*)
		ARCH=x86_64
		;;
	ppc|ppc64|mips*)
		ENDIAN=big
		ARCH=ppc64
		;;
	ppc64le*)
		ARCH=ppc64
		;;
	esac
	LIB=lib64
	if echo $ARCH |grep -qE '(arm|32|i.86)'; then
		LIB=lib
	fi
	if echo $OS |grep mingw; then
		EXTRAS_binaries="exe_wrapper = 'wine'
"
		OS=windows
	fi

	# ipc_rmid_deferred_release is to make cairo happy
	cat >%{buildroot}%{_datadir}/meson/toolchains/${i}.cross <<EOF
[binaries]
c = [ 'clang', '-target', '$i', '--sysroot', '%{_prefix}/$i' ]
cpp = [ 'clang++', '-target', '$i', '--sysroot', '%{_prefix}/$i' ]
ar = 'llvm-ar'
ranlib = 'llvm-ranlib'
strip = 'llvm-strip'
pkgconfig = '%{_bindir}/pkg-config'
$EXTRAS_binaries
[host_machine]
system = '$OS'
cpu_family = '$ARCH'
cpu = '$CPU'
endian = '$ENDIAN'
$EXTRAS_host_machine
[properties]
sys_root = '%{_prefix}/$i'
pkg_config_libdir = '%{_prefix}/$i%{_prefix}/$LIB/pkgconfig'
ipc_rmid_deferred_release = true
EOF
	cat >%{buildroot}%{_datadir}/meson/toolchains/${i}-gcc.cross <<EOF
[binaries]
c = '%{_bindir}/$i-gcc'
cpp = '%{_bindir}/$i-g++'
ar = '%{_bindir}/$i-ar'
ranlib = '%{_bindir}/$i-ranlib'
strip = '%{_bindir}/$i-strip'
pkgconfig = '%{_bindir}/pkg-config'
$EXTRAS_binaries
[host_machine]
system = '$OS'
cpu_family = '$ARCH'
cpu = '$CPU'
endian = '$ENDIAN'
$EXTRAS_host_machine
[properties]
sys_root = '%{_prefix}/$i'
pkg_config_libdir = '%{_prefix}/$i%{_prefix}/$LIB/pkgconfig'
ipc_rmid_deferred_release = true
EOF
done

%files
%{_bindir}/*
%dir %{python3_sitelib}/mesonbuild
%{python3_sitelib}/mesonbuild/*
%{python3_sitelib}/%{name}-*.dist-info
%doc %{_mandir}/*/*
%{_rpmmacrodir}/macros.%{name}
%{_rpmmacrodir}/macros.buildsys.%{name}
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/meson
