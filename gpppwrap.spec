%define name gpppwrap
%define version 1.1
%define rel 2mdk


Summary: A graphical user interface arround the ppp-on/off scripts
Name: %{name}
Version: %{version}
Release: %{rel}
License: GPL
Group: System/Configuration/Networking
URL: http://www.toppoint.de/~utuxfan/g/index.html#gpppwrap
Source: http://www.toppoint.de/~utuxfan/g/%name-%version.tar.bz2
Source1:  dnrd-2.10.tar.bz2
Patch:  gpppwrap-1.0-sysconfdir.patch.bz2
Patch1: gpppwrap-dnrd.lfs.patch.bz2
Patch2: dnrd-2.10-makefile.patch.bz2 
Prereq: rpm-helper
Buildroot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: libgtk+-devel

%description
Many Internet Service Providers (ISPs) have different modem pools for e.g
14.4, 28.8, 56k etc... modems. gpppwrap is a graphical user interface to
conveniently select a phone number and dial into your ISP. It may also
be used if you switch frequently between different ISPs.  gpppwrap is
only a wrapper around the ppp-on/ppp-off scripts and gives you therefore
still the power and flexibility of these scripts.  The gpppwrap package
contians ppp-on/ppp-off perl scripts which are Set-UID root to give
ordinary users the possibility to setup a ppp connection to the selected
phone number. gpppwrap is based on the gtk GUI libraries.  This package
contains also a cgi-script called pppcontrol.  You can place it on your
local webserver and use it instead of gpppwrap to switch on/off the
ppp connection.  This is especially useful if you have windows clients
in the local network.

This RPM includes dnrd (domain name relay domain) which is a simple "proxy"
name server. It is meant to  be used for home  networks that can connect 
to the internet using one of several ISP's.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -c -a 1
cd %{name}-%{version} 
%patch -p1
%patch1 -p1
cd ..
(
cd dnrd-2.10/
%patch2 -p1
)

%build
%serverbuild
cd  %{name}-%{version}
make 
cd ..

%install
pushd %{name}-%{version}
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ppp/{peers,scripts}
mkdir -p $RPM_BUILD_ROOT/var/www/cgi-bin/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp -a etc/ppp/* $RPM_BUILD_ROOT%{_sysconfdir}/ppp/
install -m 755 gpppquery $RPM_BUILD_ROOT%{_bindir}/
install -m 755 cgi-bin/pppcontrol $RPM_BUILD_ROOT/var/www/cgi-bin/
install -m 755 dnrd_rc  $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/
install -m 755 man1/gpppwrap.1 $RPM_BUILD_ROOT%{_mandir}/man1/
popd

(
cd dnrd-2.10/src
make
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
make INSTDIR=$RPM_BUILD_ROOT%{_sbindir} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man8/dnrd install
install -m 644 ../doc/README-* ../doc/TODO ../doc/master.sample $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cd ../..
)

rm -rf $RPM_BUILD_ROOT%_prefix/man

%clean
rm -rf $RPM_BUILD_ROOT
%post
%_post_service  dnrd_rc

%preun
%_preun_service  dnrd_rc

%files
%defattr(-,root,root)
%doc %{name}-%{version}/README
%config(noreplace) %{_sysconfdir}/ppp
%config(noreplace) %{_sysconfdir}/rc.d/init.d/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
/var/www/cgi-bin/*

