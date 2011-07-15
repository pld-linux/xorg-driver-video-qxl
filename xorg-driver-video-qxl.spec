Summary:	X.org video driver for QXL virtual GPU
Summary(pl.UTF-8):	Sterownik obrazu X.org dla wirtualnych procesorów graficznych QXL
Name:		xorg-driver-video-qxl
Version:	0.0.14
Release:	1
License:	MIT
Group:		X11/Applications
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-qxl-%{version}.tar.bz2
# Source0-md5:	3e1098302cc2efc7950322d9341537f4
# TODO: drop this patch after spice-protocol > 0.8.0 release
Patch0:		%{name}-spice.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(macros) >= 1.389
BuildRequires:	spice-protocol >= 0.7.0
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
X.org video driver for QXL virtual GPU, which can be found in the
RedHat Enterprise Virtualisation system, and also in the spice
project.

%description -l pl.UTF-8
Sterownik obrazu X.org dla wirtualnych procesorów graficznych QXL,
które można znaleźć w systemie RedHat Enterprise Virtualisation oraz
w projekcie spice.

%prep
%setup -q -n xf86-video-qxl-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

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