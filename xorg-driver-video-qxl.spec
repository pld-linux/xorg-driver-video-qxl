#
# Conditional build:
%bcond_without	pcsc	# spiceccid PC/SC driver
%bcond_without	xspice	# xspice driver
#
%if %{without xspice}
%undefine	with_pcsc
%endif
Summary:	X.org video driver for QXL virtual GPU
Summary(pl.UTF-8):	Sterownik obrazu X.org dla wirtualnych procesorów graficznych QXL
Name:		xorg-driver-video-qxl
Version:	0.1.4
Release:	4
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-qxl-%{version}.tar.bz2
# Source0-md5:	41e234f38fe8045eef7ade83c34f6dd4
Patch0:		%{name}-cast.patch
Patch1:		libcacard.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%{?with_pcsc:BuildRequires:	libcacard-devel}
BuildRequires:	libdrm-devel >= 2.4.46
BuildRequires:	libtool
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(macros) >= 1.389
BuildRequires:	spice-protocol >= 0.12.0
%{?with_xspice:BuildRequires:	spice-server-devel >= 0.6.3}
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10.0
BuildRequires:	xorg-proto-fontsproto-devel
BuildRequires:	xorg-proto-randrproto-devel
BuildRequires:	xorg-proto-renderproto-devel
BuildRequires:	xorg-proto-videoproto-devel
BuildRequires:	xorg-proto-xf86dgaproto-devel
BuildRequires:	xorg-util-util-macros >= 1.4
BuildRequires:	xorg-xserver-server-devel >= 1.0.99.901
%{?requires_xorg_xserver_videodrv}
Requires:	libdrm >= 2.4.46
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

%package -n pcsc-driver-spiceccid
Summary:	Chip/Smart Card Interface Devices driver for Spice
Summary(pl.UTF-8):	Sterownik CCID dla Spice
Group:		Libraries
Requires:	pcsc-lite

%description -n pcsc-driver-spiceccid
Chip/Smart Card Interface Devices driver for Spice.

This driver is built to interface to pcsc-lite as a serial smartcard
device. It translates the IFD (Interface device) ABI into the Spice
protocol.

%description -n pcsc-driver-spiceccid -l pl.UTF-8
Sterownik CCID (Chip/Smart Card Interface Device) dla Spice.

Ten sterownik współpracuje z pcsc-lite jako szeregowy czytnik kart
procesorowych. Tłumaczy ABI IFD (Interface device) na protokół Spice.

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
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_pcsc:--enable-ccid --with-ccid-module-dir=%{_libdir}/pcsc/drivers} \
	%{?with_xspice:--enable-xspice}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/*/*.la
%if %{with pcsc}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README TODO
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/qxl_drv.so

%if %{with pcsc}
%files -n pcsc-driver-spiceccid
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pcsc/drivers/libspiceccid.so*
%endif

%if %{with xspice}
%files -n spice-xserver
%defattr(644,root,root,755)
%doc README.xspice examples/spiceqxl.xorg.conf.example
%attr(755,root,root) %{_bindir}/Xspice
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/spiceqxl_drv.so
%endif
