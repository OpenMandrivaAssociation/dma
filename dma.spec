%define sendmail_command %{_sbindir}/%{name}

Summary:	An end-system mail server
Name:		dma
Version:	0.7
Release:	%mkrel 1
License:	BSD
URL:		https://github.com/corecode/dma
Group:		Networking/Mail
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel

Provides:	sendmail-command

# The source was obtained from upstream git repository:
# git clone git://github.com/corecode/dma.git
# pushd dma
# git archive --prefix=dma-X.Y/ -o ../dma-X.Y.tar commit_id
# popd
# xz -z -e dma-X.Y.tar
Source0:	dma-%{version}.tar.xz
Source1:	dma-aliases
Source2:	README.urpmi
Patch0:		dma-0.5-mdv-fix-build-in-rpm-env.patch
Patch1:		dma-0.2-mdv-locate-aliases-in-dma-etc-subdir.patch

%description
DragonFly Mail Agent (dma) is a small and secure MTA (mail transport agent) for
end-system use.
It features:
– daemon-less operation
– queueing
– aliases
– local delivery
– remote delivery via SMTP
– SSL support via STARTTLS and SSL
– SMTP AUTH LOGIN and -MD5 (for smart hosts)

%files
%defattr(-,root,root)
%doc TODO README.markdown VERSION README.urpmi
%attr(2755, root, mail)%{_sbindir}/%{name}
%attr(4750, root, mail)%{_libdir}/dma-mbox-create
%{_mandir}/man8/%{name}.8.*
%attr(770, root, mail)%{_var}/spool/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/auth.conf
%config(noreplace) %{_sysconfdir}/%{name}/aliases

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0
%patch1

%build
%make -j1 CFLAGS="%{optflags} \
	-DDMA_VERSION='\"%{version}\"' \
	-DLIBEXEC_PATH='\"%{_libdir}\"' \
	-DCONF_PATH='\"/etc/dma\"'" \
	LIBEXEC=%{_libdir} \
	PREFIX=%{_prefix}

%install
%__rm -rf %{buildroot}
%makeinstall DESTDIR=%{buildroot} LIBEXEC=%{_libdir} PREFIX=%{_prefix}

%__install -d %{buildroot}/%{_sysconfdir}/%{name}
%__cp auth.conf %{buildroot}/%{_sysconfdir}/%{name}/auth.conf
%__cp dma.conf %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
%__cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}/aliases
%__install -m644 %{SOURCE2} README.urpmi

%clean
%__rm -rf %{buildroot}

%post
/usr/sbin/update-alternatives --install %{_sbindir}/sendmail sendmail-command %{sendmail_command} 5 --slave %{_prefix}/lib/sendmail sendmail-command-in_libdir %{sendmail_command}

%postun
if [ ! -e %{sendmail_command} ]; then 
      /usr/sbin/update-alternatives --remove sendmail-command %{_sendmail_command}
fi


%changelog
* Thu Jan 26 2012 Andrey Bondrov <abondrov@mandriva.org> 0.7-1
+ Revision: 769128
- New version 0.7, new URL

* Wed Dec 21 2011 Andrey Bondrov <abondrov@mandriva.org> 0.6-1
+ Revision: 744079
- New version 0.6

* Mon Dec 05 2011 Andrey Bondrov <abondrov@mandriva.org> 0.5-1
+ Revision: 737843
- New version 0.5, rediff patch0

* Thu Oct 06 2011 Andrey Bondrov <abondrov@mandriva.org> 0.3-1
+ Revision: 703297
- New version: 0.3

* Tue Dec 28 2010 John Balcaen <mikala@mandriva.org> 0.2-2mdv2011.0
+ Revision: 625599
- Bump release
- import dma

