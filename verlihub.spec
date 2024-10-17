%define rel r2
%define verlihub_user verlihub
%define verlihub_group verlihub
%define verlihub_home %{_logdir}/%{name}
%define release %mkrel 2
%define name verlihub
%define devel %mklibname %{name} -d
%define libs %mklibname %{name}


Name: %{name}
Version: 0.9.8e
Release: %{release}
Summary: Direct Connect (p2p) Server
License: GPL
Group: System/Servers
Url: https://www.verlihub-project.org
Source: http://www.verlihub-project.org/download/%{name}-%{version}-%{rel}.tar.bz2
Source1: %{name}.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires: gcc-c++ glibc-devel libgeoip-devel mysql-devel libpcre-devel zlib-devel
Requires: mysql-client

%description
This program let's you have a p2p server for file sharing.

%package -n %{devel}
Summary: The files needed for %{name} development
Group: System/Servers
Requires: lib%{name} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{devel}
The %{devel} package contains the necessary include files
for developing applications with %{name}

%package -n %{libs}
Summary: The library files needed for %{name}
Group: System/Servers
Provides: lib%{name} = %{version}-%{release}

%description -n %{libs}
The %{libs} package contains the necessary library for %{name}

%prep
%setup -q -n %{name}-%{version}-%{rel}

%build
export PTHREAD_LIBS=-lpthread
autoreconf -fi
%configure
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
install -d -m1775 %{buildroot}%{_bindir}
install -d -m1775 %{buildroot}%{_libdir}
install -d -m1775 %{buildroot}%{_includedir}/%{name}
install -d -m1775 %{buildroot}%{_var}/run/%{name}
install -d -m1775 %{buildroot}%{_var}/log/%{name}
install -m0755 src/.libs/%{name} %{buildroot}%{_bindir}
install -m0755 src/.libs/*.la %{buildroot}%{_libdir}
install -m0755 src/.libs/*.so %{buildroot}%{_libdir}
install -m0755 src/*.h %{buildroot}%{_includedir}/%{name}/
install -d %{buildroot}%{_sysconfdir}/%{name}/plugins
install -d %{buildroot}%{_sysconfdir}/%{name}/scripts
install -m0755 plugins/plugman/.libs/*.so* %{buildroot}%{_sysconfdir}/%{name}/plugins
install -m0644 share/config/* %{buildroot}%{_sysconfdir}/%{name}
install -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%pre
/usr/sbin/groupadd -r -f %{verlihub_group} ||:
/usr/sbin/useradd -g %{verlihub_group} -c 'The verlihub Daemon' \
       -d %{verlihub_home} -s /dev/null -r %{verlihub_user} >/dev/null 2>&1 ||:

%files
%defattr(0750,root,%{verlihub_group},-)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_sysconfdir}/%{name}/scripts
%defattr(1755,root,%{verlihub_group},-)
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}
%defattr(-,root,root,-)
%doc AUTHORS README* ChangeLog TODO
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sysconfdir}/%{name}/plugins/*
%{_bindir}/%{name}
%{_initrddir}/%{name}

%files -n %{libs}
%defattr(-,root,root,-)
%{_libdir}/*.so*

%files -n %{devel}
%defattr(-,root,root,-)
%{_libdir}/*.la
%{_includedir}/%{name}/*
