#
# Conditional build:
# _with_gtk1	- use gtk+ 1.2 instead of 2.x
#
%define		minmozver	3:1.2.1
%define		gtkv		gtk%{?_with_gtk1:1}%{!?_with_gtk1:2}
Summary:	Light - Yet Another Mozilla Based Browser
Summary(pl):	Light - jeszcze jedna przegl±darka oparta na Mozilli (gecko)
Name:		light
Version:	1.4.12
Release:	5.1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.ne.jp/asahi/linux/timecop/software/%{name}-%{version}.tar.bz2
# Source0-md5:	b83da71a3504cbb7812d0b56bf709cd9
Source1:	%{name}.desktop
Patch0:		%{name}-mozilla1.1-noxfer.patch
Patch1:		%{name}-mozilla1.2b.patch
Patch2:		%{name}-mozilla1.4.patch
Patch3:		%{name}-gtk2.patch
URL:		http://www.ne.jp/asahi/linux/timecop/#light
BuildRequires:	autoconf
%{?_with_gtk1:BuildRequires:	gtk+-devel >= 1.2.6}
%{!?_with_gtk1:BuildRequires:	gtk+2-devel >= 2.0.0}
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded(%{gtkv}) >= %{minmozver}
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
%{!?_with_gtk1:BuildRequires:	pkgconfig}
BuildRequires:	zlib-devel
Requires:	mozilla-embedded(%{gtkv}) = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
This is "Yet Another Mozilla Based Browser", called "Light".

%description -l pl
To jest jeszcze jedna przegl±darka oparta na Mozilli o nazwie "Light".

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{!?_with_gtk1:%patch3 -p1}

%build
%{__autoconf}
%configure \
	--with-mozilla-libs=/usr/lib \
	--with-mozilla-includes="/usr/include/mozilla -I/usr/include/mozilla/gtkembedmoz -I/usr/include/mozilla/necko -I/usr/include/mozilla/xpcom -I/usr/include/mozilla/string -I/usr/include/mozilla/embed_base -I/usr/include/mozilla/docshell -I/usr/include/mozilla/content -I/usr/include/mozilla/webbrwsr -I/usr/include/mozilla/webbrowserpersist -I/usr/include/mozilla/find -I/usr/include/mozilla/webshell -I/usr/include/mozilla/gfx -I/usr/include/mozilla/shistory -I/usr/include/mozilla/appcomps -I/usr/include/mozilla/uconv -I/usr/include/mozilla/widget -I/usr/include/mozilla/dom -I/usr/include/mozilla/layout -I/usr/include/mozilla/mozxfer -I/usr/include/mozilla/nkcache -I/usr/include/mozilla/pref" \
	--with-nspr-includes=/usr/include/nspr \
	--enable-mozilla-cvs

%{__make} OPT="%{rpmcflags} -DNEW_H=\<new.h\>"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_applnkdir}/Network/WWW}

install src/light $RPM_BUILD_ROOT%{_bindir}/light-bin

cat > $RPM_BUILD_ROOT%{_bindir}/light <<EOF
#!/bin/sh

MOZILLA_FIVE_HOME=/usr/lib/mozilla
export MOZILLA_FIVE_HOME

exec %{_bindir}/light-bin \$@
EOF

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/*.html
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*.desktop
