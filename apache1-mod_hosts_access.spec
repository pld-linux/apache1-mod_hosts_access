%define		mod_name	hosts_access
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: access defined by hosts.allow/hosts.deny
Summary(pl):	Modu³ do apache: dostêp na podstawie hosts.allow/hosts.deny
Name:		apache1-mod_%{mod_name}
Version:	1.0.0
Release:	0.2
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.klomp.org/mod_hosts_access/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	3720e303cfde50e94586f484a903aa41
URL:		http://www.klomp.org/mod_hosts_access/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	libwrap-devel
Requires(post,preun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Mod_hosts_access allows you to use the hosts.allow and hosts.deny
files to configure access to your apache webserver.

%description -l pl
Mod_hosts_access pozwala u¿ywaæ plików hosts.allow i hosts.deny do
okre¶lania dostêpu do zasobów serwera WWW apache.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -lwrap

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README INSTALL
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
