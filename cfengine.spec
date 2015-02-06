%define _fortify_cflags %{nil}

%define major 1
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname -d %{name}

Name:		cfengine
Version:	3.3.0
Release:	3
Summary:	Cfengine helps administer remote BSD and System-5-like systems
License:	GPL
Group:		Monitoring
URL:		http://www.cfengine.org
Source0:	http://www.cfengine.org/tarballs/%{name}-%{version}.tar.gz
Source4:	cfengine-serverd.init
Source5:	cfengine-execd.init
Source6:	cfengine-monitord.init
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel
BuildRequires:	db-devel
BuildRequires:	graphviz-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig(tokyocabinet)
Requires(pre):	rpm-helper
Requires(preun):rpm-helper
%rename cfengine3

%description
Cfengine, the configuration engine, is a very high level language for
simplifying the task of administrating and configuring large numbers
of workstations. Cfengine uses the idea of classes and a primitive
form of intelligence to define and automate the configuration of large
systems in the most economical way possible.

%package base
Summary:	Cfengine base files
Group:		Monitoring
Requires:	lsb-release
%rename cfengine3-base

%description base
This package contain the cfengine base files needed by all subpackages.

%package agent
Summary:	Cfengine agent
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
%rename cfengine3-agent

%description agent
This package contain the cfengine agent.

%package serverd
Summary:	Cfengine server daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):rpm-helper
Requires(preun):rpm-helper
%rename cfengine3-serverd

%description serverd
This package contain the cfengine server daemon.

%package execd
Summary:	Cfengine agent execution wrapper
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):rpm-helper
%rename cfengine3-execd

%description execd
This package contain the cfengine agent execution wrapper.

%package monitord
Summary:	Cfengine anomaly detection daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(preun):rpm-helper
%rename cfengine3-monitord

%description monitord
This package contain the cfengine anomaly detection daemon.

%package -n	%{libname}
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries
%define old_libname %mklibname %{name}3_ %{major}
%rename %{old_libname}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
%define old_develname %mklibname -d %{name}3
%rename %{old_develname}

%description -n	%{develname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q -n %{name}-%{version}

%build
%serverbuild
%configure2_5x --with-workdir=%{_localstatedir}/lib/%{name} --enable-shared
%make

%install
%makeinstall_std projlibdir=%{_libdir}

install -d -m 755 %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/bin
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/lastseen
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/modules
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/outputs
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{name}/ppkeys
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/randseed
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/reports
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{name}/rpc_in
install -d -m 700 %{buildroot}%{_localstatedir}/lib/%{name}/rpc_out
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/rpc_state

#mv %{buildroot}%{_docdir}/%{name}/inputs \
#    %{buildroot}%{_sysconfdir}/%{name}

pushd %{buildroot}%{_localstatedir}/lib/%{name}
ln -sf ../../..%{_sysconfdir}/%{name} inputs
popd
pushd %{buildroot}%{_localstatedir}/lib/%{name}/bin
#ln -sf ../../../../%{_sbindir}/cf-promises .
for i in ../../../../%{_sbindir}/cf-*
do
ln -sf ../../../../%{_sbindir}/$i .
done
popd

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/cfengine-serverd
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/cfengine-execd
install -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/cfengine-monitord

# mv %{buildroot}%{_docdir}/%{name} %{buildroot}%{_docdir}/%{name}

# compatibility purpose
pushd %{buildroot}%{_localstatedir}/lib/%{name}
ln -sf %{_localstatedir}/lib/%{name} ../../%{name}
popd

%post base
if [ $1 = 1 ]; then
    [ -f "%{_localstatedir}/lib/%{name}/ppkeys/localhost.priv" ] || cf-key >/dev/null 2>&1
fi

%post execd
%_post_service cfengine-execd

%preun execd
%_preun_service cfengine-execd

%post monitord
%_post_service cfengine-monitord

%preun monitord
%_preun_service cfengine-monitord

%post serverd
%_post_service cfengine-serverd

%preun serverd
%_preun_service cfengine-serverd

%files base
%doc %{_docdir}/README
%doc %{_docdir}/ChangeLog
%doc %{_docdir}/example_config
%doc %{_docdir}/examples
%{_bindir}/cf-key
%{_bindir}/cf-promises
%{_datadir}/CoreBase
%{_localstatedir}/lib/%{name}
%{_localstatedir}/%{name}
# %config(noreplace) %{_sysconfdir}/%{name}
%{_mandir}/man8/cf-key.8*
%{_mandir}/man8/cf-promises.8*

%files agent
%{_bindir}/cf-agent
%{_bindir}/cf-know
%{_bindir}/cf-report
%{_bindir}/cf-runagent
%{_mandir}/man8/cf-agent.8*
%{_mandir}/man8/cf-know.8*
%{_mandir}/man8/cf-report.8*
%{_mandir}/man8/cf-runagent.8*

%files serverd
%{_initrddir}/cfengine-serverd
%{_bindir}/cf-serverd
%{_mandir}/man8/cf-serverd.8*

%files monitord
%{_initrddir}/cfengine-monitord
%{_bindir}/cf-monitord
%{_mandir}/man8/cf-monitord.8*

%files execd
%{_initrddir}/cfengine-execd
%{_bindir}/cf-execd
%{_mandir}/man8/cf-execd.8*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
