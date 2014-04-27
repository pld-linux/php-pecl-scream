%define		php_name	php%{?php_suffix}
%define		modname		scream
%define		status		alpha
Summary:	break the silence operator
Summary(pl.UTF-8):	przełamanie operatora wyciszania
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.0
Release:	7
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	ec606b6b9f23bd7de532c7f77c953852
URL:		http://pecl.php.net/package/scream/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows you to disable the silence operator (@) to get all error
messages.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala na wyłączenie operatora wyciszania (@) w celu
uzyskania pełnych komunikatów błędu.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
