%define		mod_name	hosts_access
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: access defined by hosts.allow/hosts.deny
Summary(pl):	Modu³ do apache: dostêp na podstawie hosts.allow/hosts.deny
Name:		apache1-mod_%{mod_name}
Version:	1.0.0
Release:	0.1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.klomp.org/mod_hosts_access/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	3720e303cfde50e94586f484a903aa41
URL:		http://www.klomp.org/mod_hosts_access/
BuildRequires:	apache1-devel
BuildRequires:	libwrap-devel
Requires(post,preun):	%{apxs}
Requires:	apache1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir     /etc/httpd

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
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README INSTALL
%attr(755,root,root) %{_pkglibdir}/*
