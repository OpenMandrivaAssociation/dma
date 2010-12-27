%define	name		dma
%define	version		0.2
%define	release		1

%define sendmail_command %{_sbindir}/%{name}

Summary:	dma is an end-system mail server and supports queueing and local & remote mail delivery via SMTP and SSL/TLS
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
License:	BSD
URL:		http://gitorious.org/dma
Group:		Networking/Mail 
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	openssl-devel

Provides:	sendmail-command

# The source was obtained from upstream git repository:
# git clone git://gitorious.org/dma/dma.git
# pushd dma
# git archive --prefix=dma-X.Y/ -o ../dma-X.Y.tar commit_id
# popd 
# bzip2 dma-X.Y.tar
Source0:	dma-%{version}.tar.bz2	
Source1:	dma-aliases
Source2:	README.urpmi
Patch0:		dma-0.2-mdv-fix-build-in-rpm-env.patch
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
%doc TODO README VERSION README.urpmi
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
%make CFLAGS="%optflags -DDMA_VERSION='\"%{version}\"' -DLIBEXEC_PATH='\"%{_libdir}\"'" LIBEXEC=%{_libdir} PREFIX=%{_prefix}

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
