#
# Conditional build:
%bcond_without	xspice	# xspice driver
#
Summary:	X.org video driver for QXL virtual GPU
Summary(pl.UTF-8):	Sterownik obrazu X.org dla wirtualnych procesorów graficznych QXL
Name:		xorg-driver-video-qxl
Version:	0.0.17
Release:	1
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-qxl-%{version}.tar.bz2
# Source0-md5:	c0ee45ce06654b9f2e6ddac478d5fbd6
Patch0:		%{name}-cast.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(macros) >= 1.389
BuildRequires:	spice-protocol >= 0.8.1
%{?with_xspice:BuildRequires:	spice-server-devel >= 0.6.3}
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10.0
BuildRequires:	xorg-proto-fontsproto-devel
BuildRequires:	xorg-proto-randrproto-devel
BuildRequires:	xorg-proto-renderproto-devel
BuildRequires:	xorg-proto-videoproto-devel
BuildRequires:	xorg-proto-xf86dgaproto-devel
BuildRequires:	xorg-util-util-macros >= 1.4
BuildRequires:	xorg-xserver-server-devel >= 1.0.99.901
%{?requires_xorg_xserver_videodrv}
Requires:	xorg-lib-libpciaccess >= 0.10.0
Requires:	xorg-xserver-server >= 1.0.99.901
Provides:	xorg-driver-video
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
X.org video driver for QXL virtual GPU, which can be found in the
RedHat Enterprise Virtualisation system, and also in the spice
project.

%description -l pl.UTF-8
Sterownik obrazu X.org dla wirtualnych procesorów graficznych QXL,
które można znaleźć w systemie RedHat Enterprise Virtualisation oraz w
projekcie spice.

%package -n spice-xserver
Summary:	Xspice - X server and Spice server in one
Summary(pl.UTF-8):	Xspice - serwer X oraz serwer Spice w jednym
Group:		X11/Applications
Requires:	spice-server-libs >= 0.6.3
Requires:	xorg-xserver-server >= 1.0.99.901

%description -n spice-xserver
Xspice is an X server and Spice server in one. It consists of a
wrapper script for executing Xorg with the right parameters and
environment variables, a module named spiceqxl_drv.so implementing
three drivers: a video mostly code identical to the guest qxl X
driver, and keyboard and mouse reading from the spice inputs channel.

Xspice allows regular X connections, while a spice client provides the
keyboard and mouse and video output.

%description -n spice-xserver -l pl.UTF-8
Xspice to serwer X i serwer Spice w jednym. Składa się ze skryptu
wywołującego Xorg z właściwymi parametrami i zmiennymi środowiskowymi,
oraz modułu o nazwie spiceqxl_drv.so implementującego trzy sterowniki:
graficzny oparty na kodzie prawie identycznym ze sterownikiem X gościa
qxl, oraz klawiatury i myszy szytające z kanału wejćiowego spice.

Xspice pozwala na normalne połączenia X, podczas gdy klient spice
udostępnia wejście klawiatury i myszy oraz wyjście obrazu.

%prep
%setup -q -n xf86-video-qxl-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_xspice:--enable-xspice}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/*/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README TODO
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/qxl_drv.so

%if %{with xspice}
%files -n spice-xserver
%defattr(644,root,root,755)
%doc README.xspice examples/spiceqxl.xorg.conf.example
%attr(755,root,root) %{_bindir}/Xspice
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/spiceqxl_drv.so
%endif
