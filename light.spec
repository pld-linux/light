
%define		minmozver	1.1

Summary:	Light - Yet Another Mozilla Based Browser
Summary(pl):	Light - jeszcze jedna przegl±darka oparta na Mozilli (gecko)
Name:		light
Version:	1.4.12
Release:	4
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.ne.jp/asahi/linux/timecop/software/%{name}-%{version}.tar.bz2
# Source0-md5:	b83da71a3504cbb7812d0b56bf709cd9
Source1:	%{name}.desktop
Patch0:		%{name}-mozilla1.1-noxfer.patch
Patch1:		%{name}-mozilla1.2b.patch
URL:		http://www.ne.jp/asahi/linux/timecop/#light
BuildRequires:	autoconf
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	zlib-devel
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
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

%build
%{__autoconf}
%configure \
	--with-mozilla-libs=/usr/X11R6/lib \
	--with-mozilla-includes="/usr/X11R6/include/mozilla -I/usr/X11R6/include/mozilla/gtkembedmoz -I/usr/X11R6/include/mozilla/necko -I/usr/X11R6/include/mozilla/xpcom -I/usr/X11R6/include/mozilla/string -I/usr/X11R6/include/mozilla/embed_base -I/usr/X11R6/include/mozilla/docshell -I/usr/X11R6/include/mozilla/content -I/usr/X11R6/include/mozilla/webbrwsr -I/usr/X11R6/include/mozilla/webbrowserpersist -I/usr/X11R6/include/mozilla/find -I/usr/X11R6/include/mozilla/webshell -I/usr/X11R6/include/mozilla/gfx -I/usr/X11R6/include/mozilla/shistory -I/usr/X11R6/include/mozilla/appcomps -I/usr/X11R6/include/mozilla/uconv -I/usr/X11R6/include/mozilla/widget -I/usr/X11R6/include/mozilla/dom -I/usr/X11R6/include/mozilla/layout -I/usr/X11R6/include/mozilla/mozxfer -I/usr/X11R6/include/mozilla/nkcache -I/usr/X11R6/include/mozilla/pref" \
	--with-nspr-includes=/usr/include/nspr \
	--enable-mozilla-cvs

%{__make} OPT="%{rpmcflags} -DNEW_H=\<new.h\>"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_applnkdir}/Network/WWW}

install src/light $RPM_BUILD_ROOT%{_bindir}/light-bin

cat > $RPM_BUILD_ROOT%{_bindir}/light <<EOF
#!/bin/sh

MOZILLA_FIVE_HOME=/usr/X11R6/lib/mozilla
export MOZILLA_FIVE_HOME

exec %{_bindir}/light-bin \$@
EOF

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
rm -f %{_libdir}/mozilla/components/{compreg,xpti}.dat
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/*.html
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*.desktop
