
%define		minmozver	0.9.9

Summary:	Light - Yet Another Mozilla Based Browser
Summary(pl):	Light - jeszcze jedna przegl±darka oparta na Mozilli (gecko)
Name:		light
Version:	1.4.11
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.ne.jp/asahi/linux/timecop/software/%{name}-%{version}.tar.bz2
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

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
This is "Yet Another Mozilla Based Browser", called "Light".

%description -l pl
To jest jeszcze jedna przegl±darka oparta na Mozilli o nazwie "Light".

%prep
%setup -q

%build
autoconf
%configure \
	--with-mozilla-libs=/usr/X11R6/lib \
	--with-mozilla-includes="/usr/X11R6/include/mozilla -I/usr/X11R6/include/mozilla/gtkembedmoz -I/usr/X11R6/include/mozilla/necko -I/usr/X11R6/include/mozilla/xpcom -I/usr/X11R6/include/mozilla/string -I/usr/X11R6/include/mozilla/embed_base -I/usr/X11R6/include/mozilla/docshell -I/usr/X11R6/include/mozilla/content -I/usr/X11R6/include/mozilla/webbrwsr -I/usr/X11R6/include/mozilla/webbrowserpersist -I/usr/X11R6/include/mozilla/find -I/usr/X11R6/include/mozilla/webshell -I/usr/X11R6/include/mozilla/gfx -I/usr/X11R6/include/mozilla/shistory -I/usr/X11R6/include/mozilla/appcomps -I/usr/X11R6/include/mozilla/uconv -I/usr/X11R6/include/mozilla/widget -I/usr/X11R6/include/mozilla/dom -I/usr/X11R6/include/mozilla/layout -I/usr/X11R6/include/mozilla/mozxfer -I/usr/X11R6/include/mozilla/nkcache -I/usr/X11R6/include/mozilla/pref" \
	--with-nspr-includes=/usr/include/nspr \
	--enable-mozilla-cvs

%{__make} OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install src/light $RPM_BUILD_ROOT%{_bindir}/light-bin

cat > $RPM_BUILD_ROOT%{_bindir}/light <<EOF
#!/bin/sh

MOZILLA_FIVE_HOME=/usr/X11R6/lib/mozilla
export MOZILLA_FIVE_HOME

exec %{_bindir}/light-bin \$@
EOF

gzip -9nf AUTHORS ChangeLog README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.html
%attr(755,root,root) %{_bindir}/*
