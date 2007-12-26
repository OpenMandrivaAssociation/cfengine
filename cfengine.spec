%define	name	cfengine
%define version 2.2.3
%define release %mkrel 2

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Cfengine helps administer remote BSD and System-5-like systems
License:	GPL
Group:		Monitoring
URL:		http://www.cfengine.org
Source0:	ftp://ftp.iu.hio.no/pub/cfengine/%{name}-%{version}.tar.gz
Source1:	%{name}.vim
Source4:	cfengine.init
Source5:	cfengine.sysconfig
Source7:	%{name}.bash-completion
Patch0:		%{name}-2.2.3-autotools-fix.patch
Patch1:		cfengine-fpic.diff
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel
BuildRequires:	db4-devel
BuildRequires:	tetex-dvips
BuildRequires:	texinfo
BuildRequires:	tetex-latex
Requires(pre):	rpm-helper
Requires(preun):rpm-helper
Obsoletes:      %{name}-base < 2.2.3
Obsoletes:      %{name}-cfagent < 2.2.3
Obsoletes:      %{name}-cfservd < 2.2.3
Obsoletes:      %{name}-cfexecd < 2.2.3
Obsoletes:      %{name}-cfenvd < 2.2.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Cfengine, the configuration engine, is a very high level language for
simplifying the task of administrating and configuring large numbers
of workstations. Cfengine uses the idea of classes and a primitive
form of intelligence to define and automate the configuration of large
systems in the most economical way possible.

%package -n	%{libname}
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

chmod 644 inputs/*

%build
autoreconf
%serverbuild
%configure2_5x --with-workdir=%{_localstatedir}/%{name} --enable-shared
%make
cd doc
%make

%install
rm -rf %{buildroot}
%makeinstall
pushd doc
%makeinstall
popd

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_localstatedir}/%{name}
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/cfengine
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/cfengine

# everything installed there is doc, actually
rm -rf %{buildroot}%{_datadir}/%{name}

%define info_files cfengine-Tutorial cfengine-Reference

# install vim syntax file
install -d -m 755 %{buildroot}%{_datadir}/vim/syntax
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/vim/syntax

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%post
for f in %{info_files}; do
    %_install_info $f
done
if [ $1 = 1 ]; then
    [ -f "%{_localstatedir}/%{name}/ppkeys/localhost.priv" ] || cfkey >/dev/null 2>&1
fi
%_post_service %{name}

%preun
for f in %{info_files}; do
    %_remove_install_info $f
done
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/*.{ps,pdf,html} inputs/*.example
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/cfengine
%{_sysconfdir}/bash_completion.d/%{name}
%{_initrddir}/%{name}
%{_localstatedir}/%{name}
%{_sbindir}/*
%{_infodir}/*
%{_mandir}/man8/*
%{_datadir}/vim/syntax/%{name}.vim

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
