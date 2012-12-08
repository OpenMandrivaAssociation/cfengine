%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		cfengine
Version:	2.2.10
Release:	11
Summary:	Cfengine helps administer remote BSD and System-5-like systems
License:	GPLv2+
Group:		Monitoring
URL:		http://www.cfengine.org
Source0:	http://www.cfengine.org/downloads/%{name}-%{version}.tar.gz
Source4:	cfservd.init
Source5:	cfexecd.init
Source6:	cfenvd.init
Patch0:		cfengine-2.2.9-fix-format-errors.patch
Patch1:		cfengine-2.2.10-fix-warning-for-recurse-statement.patch 
Patch2:		cfengine_remove_broken_ldflag_change.patch
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel
BuildRequires:	db5-devel
BuildRequires:	tetex-latex texinfo 
Requires(pre):	rpm-helper
Requires(preun):rpm-helper

%description
Cfengine, the configuration engine, is a very high level language for
simplifying the task of administrating and configuring large numbers
of workstations. Cfengine uses the idea of classes and a primitive
form of intelligence to define and automate the configuration of large
systems in the most economical way possible.

%package	base
Summary:	Cfengine base files
Group:		Monitoring

%description	base
This package contain the cfengine base files needed by all subpackages.

%package	cfagent
Summary:	Cfengine agent
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}

%description	cfagent
This package contain the cfengine agent.

%package	cfservd
Summary:	Cfengine server daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description	cfservd
This package contain the cfengine server daemon.

%package	cfexecd
Summary:	Cfengine agent execution wrapper
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):rpm-helper

%description	cfexecd
This package contain the cfengine agent execution wrapper.

%package	cfenvd
Summary:	Cfengine anomaly detection daemon
Group:		Monitoring
Requires:	%{name}-base = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(preun):rpm-helper

%description	cfenvd
This package contain the cfengine anomaly detection daemon.

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
%patch0 -p 1
%patch1 -p 1
%patch2 -p1
autoreconf -fi

chmod 644 inputs/*

%build
%serverbuild
%configure2_5x --with-workdir=%{_localstatedir}/lib/%{name} --enable-shared
%make

%install
%makeinstall

# texi broken?
%if 0
%makeinstall_std -C doc
%else
cd doc
for i in *.8; do
	install -m644 $i -D %{buildroot}%{_mandir}/man8/$i
done
for i in *.info; do
	install -m644 $i -D %{buildroot}%{_infodir}/$i
done
%endif
cd -

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/cfservd
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/cfexecd
install -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/cfenvd

# everything installed there is doc, actually
rm -rf %{buildroot}%{_datadir}/%{name}

%post base
if [ $1 = 1 ]; then
    [ -f "%{_localstatedir}/lib/%{name}/ppkeys/localhost.priv" ] || cfkey >/dev/null 2>&1
fi

%post cfexecd
%_post_service cfexecd

%preun cfexecd
%_preun_service cfexecd

%post cfenvd
%_post_service cfenvd

%preun cfenvd
%_preun_service cfenvd

%post cfservd
%_post_service cfservd

%preun cfservd
%_preun_service cfservd

%files base
%doc inputs/*.example
%{_sysconfdir}/cfengine
%{_sbindir}/cfkey
%{_sbindir}/cfshow
%{_sbindir}/cfdoc
%{_localstatedir}/lib/%{name}
%{_mandir}/man8/cfengine.8.*
%{_mandir}/man8/cfkey.8.*
%{_mandir}/man8/cfshow.8.*
%{_infodir}/*


%files cfagent
%{_sbindir}/cfagent
%{_sbindir}/cfenvgraph
%{_sbindir}/cfrun
%{_sbindir}/cfetool*
%{_mandir}/man8/cfagent.8.*
%{_mandir}/man8/cfenvgraph.8.*
%{_mandir}/man8/cfetool*.8.*
%{_mandir}/man8/cfrun.8.*

%files cfservd
%{_initrddir}/cfservd
%{_sbindir}/cfservd
%{_mandir}/man8/cfservd.8.*

%files cfenvd
%{_initrddir}/cfenvd
%{_sbindir}/cfenvd
%{_mandir}/man8/cfenvd.8.*

%files cfexecd
%{_initrddir}/cfexecd
%{_sbindir}/cfexecd
%{_mandir}/man8/cfexecd.8.*

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-10
+ Revision: 663363
- mass rebuild

* Thu Mar 31 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.2.10-9
+ Revision: 649376
- work around texi2dvi issue for now..
- build against db 5.1
- cleanups

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-8mdv2011.0
+ Revision: 603822
- rebuild

* Fri May 14 2010 Michael Scherer <misc@mandriva.org> 2.2.10-7mdv2010.1
+ Revision: 544803
- fix BR
- fix BR
- fix License
- add missing manpages

* Tue Apr 06 2010 Funda Wang <fwang@mandriva.org> 2.2.10-6mdv2010.1
+ Revision: 531924
- rebuild for new openssl

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-5mdv2010.1
+ Revision: 511555
- rebuilt against openssl-0.9.8m

* Thu Dec 31 2009 Funda Wang <fwang@mandriva.org> 2.2.10-4mdv2010.1
+ Revision: 484335
- rebuild for db4.8

* Thu Sep 24 2009 Olivier Blin <oblin@mandriva.com> 2.2.10-3mdv2010.0
+ Revision: 448221
- fix configure ldflags damage (from Arnaud Patard)
  This stuff is plain broken. The configure script should never ever
  override the values given to him. It's even more broken on multilibs
  systems : For instance, if one has o32 system with mips 64bit libs...

* Thu Sep 10 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.10-2mdv2010.0
+ Revision: 436647
- fix spurrious warning for recurse keyword in editfiles action

* Tue Jun 23 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.10-1mdv2010.0
+ Revision: 388684
- new version

* Thu Feb 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.9-1mdv2009.1
+ Revision: 337969
- new maintainace release (3.0.0 doesn't build standalone yet)
- keep bash completion in its own package

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.8-3mdv2009.1
+ Revision: 314522
- rebuilt against db4.7

* Wed Sep 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.8-2mdv2009.0
+ Revision: 287842
- ship vim syntax file in vim package

* Thu Aug 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.8-1mdv2009.0
+ Revision: 271895
- new version

* Tue Jun 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.7-1mdv2009.0
+ Revision: 223773
- new version
- cosmetic in init scripts

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue May 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.6-1mdv2009.0
+ Revision: 201900
- new version
  drop -fPIC flag, merged upstream
- update fpic patch
- new version

* Sat Mar 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.3-5mdv2008.1
+ Revision: 189472
- completion fixes

* Thu Feb 28 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.3-4mdv2008.1
+ Revision: 176197
- fix typo in cfservd dependencies

* Sat Dec 29 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.3-3mdv2008.1
+ Revision: 139202
- revert to previous setup with distinct services and subpackage, merging causes too much troubles without real advantage
- rename patch2 correctly

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-2mdv2008.1
+ Revision: 138177
- second try to add -fPIC
- added -fPIC in P1
- rebuilt against bdb 4.6.x

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - merge various services, and their associated subpackages
    - new version
    - bash completion

* Thu Jul 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.1-1mdv2008.0
+ Revision: 53677
- new version


* Tue Feb 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.22-1mdv2007.0
+ Revision: 126593
- new version
  init script harmonisation with other packages

* Wed Feb 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.20-3mdv2007.1
+ Revision: 120777
- added vim syntax file

* Fri Sep 15 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.20-2mdv2007.0
- unzip all additional sources
- more dependencies in init scripts
- allow configuration in init script, so as to redefine CFINPUTS if needed
- drop unused sources

* Thu May 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.20-1mdk
- new version
- drop patches, incriminated script is not shipped anymore
- drop cron task and default configuration, too much site-specific
- make init scripts LSB-compliants

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.1.16-3mdk
- rebuilt against openssl-0.9.8a

* Sat Oct 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.16-2mdk
- security fixes from security team:
 - patch vicf.in so it can run without error (P1)
 - security update for CAN-2005-2960 (P0)
- add CFOPTIONS to cron script

* Sat Oct 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.16-1mdk
- New release 2.1.16

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1.15-2mdk
- fix rpmlint errors (PreReq)

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1.15-1mdk
- 2.1.15
- fix rpmlint errors (PreReq)

* Sat Apr 23 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.14-1mdk
- New release 2.1.14
- drop patches
- new subpackage split: base, cfagent, cfservd, cfexecd, cfenvd

* Tue Feb 08 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-7mdk 
- really fix cron script

* Mon Feb 07 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.1.12-6mdk
- split cfservd into separate package
- fix config file location

* Thu Jan 20 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-5mdk 
- fix update.conf not executed (patch1, from upstream subversion)
- fix initscripts
- less arbitrary default configuration

* Tue Jan 18 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-4mdk 
- add service scripts for cfservd, cfenvd, cfexecd
- s/Linux Mandrake/Mandrakelinux/ in cron script (thx misc)

* Tue Jan 18 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-3mdk 
- set work dir to /var/lib/cfengine
- set backup to /var/lib/cfengine/backups
- autogen keys as postinstall

* Tue Jan 18 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-2mdk 
- switch to automake1.8
- drop cfd, no longer used
- fix cron task
- configuration for cron task in /etc/sysinit/cfengine
- fix config file
- bzip2 additional files

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.1.12-1mdk 
- new version
- fix url
- exec in /etc are not configuration
- drop patch 0, no more use
- spec cleanup
- use macros

* Wed Jun 09 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.6.5-4mdk
- force use of autoconf2.5 and automake1.4
- be sure to build everything in %%build (therefore run make twice)
- wipe out buildroot at the beginning of %%install
- fix permissions on docs
- update prereq on /sbin/chkconfig to rpm-helper
- cosmetics

