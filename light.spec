Summary:	Light - Yet Another Mozilla Based Browser
Summary(pl):	Light - jeszcze jedna przegl±darka oparta na Mozilli (gecko)
Name:		light
Version:	1.4.7
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://www.ne.jp/asahi/linux/timecop/software/%{name}-%{version}.tar.bz2
Patch0:		%{name}-mozilla.patch
URL:		http://www.ne.jp/asahi/linux/timecop/#light
Requires:	mozilla-embedded >= 0.9.2-4
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	mozilla-devel >= 0.9.2-4
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libplds4.so libplc4.so libnspr4.so libgtksuperwin.so libxpcom.so

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
This is "Yet Another Mozilla Based Browser", called "Light".

%description -l pl
To jest jeszcze jedna przegl±darka oparta na Mozilli o nazwie "Light".

%prep
%setup -q
%patch0 -p1

%build
autoconf
%configure \
	--with-mozilla-libs=/usr/X11R6/lib \
	--with-mozilla-includes=/usr/X11R6/include/mozilla

%{__make} OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install src/light $RPM_BUILD_ROOT%{_bindir}

gzip -9nf AUTHORS ChangeLog README TODO

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.html
%attr(755,root,root) %{_bindir}/*
