#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API

Summary:	Library to create components for Wayland using the Layer Shell protocol and GTK4
Summary(pl.UTF-8):	Biblioteka do tworzenia komponentów Waylanda przy użyciu protokołu Layer Shell i GTK4
Name:		gtk4-layer-shell
Version:	1.3.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/wmww/gtk4-layer-shell/releases
Source0:	https://github.com/wmww/gtk4-layer-shell/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dfc6a164894e5cded49b197645e0f84b
URL:		https://github.com/wmww/gtk4-layer-shell
BuildRequires:	gcc >= 6:4.7
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk4-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	wayland-devel >= 1.10.0
BuildRequires:	wayland-protocols >= 1.16
%{?with_vala:BuildRequires:	vala}
Requires:	wayland%{?_isa} >= 1.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library to write GTK4 applications that use Layer Shell. Layer Shell
is a Wayland protocol for desktop shell components, such as panels,
notifications and wallpapers. You can use it to anchor your windows to
a corner or edge of the output, or stretch them across the entire
output. This library only makes sense on Wayland compositors that
support Layer Shell, and will not work on X11. It supports all Layer
Shell features including popups and popovers (GTK popups Just Work
(TM)).

%description -l pl.UTF-8
Biblioteka do tworzenia aplikacji GTK4, wykorzystujących protokół Layer
Shell. Jest to protokół Wayland dla komponentów powłok graficznych,
takich jak panele, powiadomienia i tapety. Można go używać do
zakotwiczania okien w roku lub przy brzegu wyjścia, albo rozciągania
ich na całe wyjście. Biblioteka ma sens tylko dla zarządców składania
Wayland obsługujących protokół Layer Shell, nie będzie działać na X11.
Obsługuje wszystkie możliwości protokołu Layer Shell, w tym
wyskakujące okna.

%package preload
Summary:	gtk4-layer-shell preload library
Group:		Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description preload
liblayer-shell-preload.so is a hack to allow arbitrary Wayland apps to
use the Layer Shell protocol. It uses the same approach as
gtk4-layer-shell, but generalized to work with any libwayland-client
program. It's designed to be LD_PRELOADed into pre-built binaries, no
recompiling necessary.

%package devel
Summary:	Header files for gtk4-layer-shell library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gtk4-layer-shell
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gtk4-devel%{?_isa}
Requires:	wayland-devel%{?_isa} >= 1.10.0

%description devel
Header files for gtk4-layer-shell library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gtk4-layer-shell.

%package static
Summary:	Static gtk4-layer-shell library
Summary(pl.UTF-8):	Biblioteka statyczna gtk4-layer-shell
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static gtk4-layer-shell library.

%description static -l pl.UTF-8
Biblioteka statyczna gtk4-layer-shell.

%package apidocs
Summary:	API documentation for gtk4-layer-shell library
Summary(pl.UTF-8):	Dokumentacja API biblioteki gtk4-layer-shell
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for gtk4-layer-shell library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gtk4-layer-shell.

%package -n vala-gtk4-layer-shell
Summary:	gtk4-layer-shell API for Vala language
Summary(pl.UTF-8):	API gtk4-layer-shell dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-gtk4-layer-shell
gtk4-layer-shell API for Vala language.

%description -n vala-gtk4-layer-shell -l pl.UTF-8
API gtk4-layer-shell dla języka Vala.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Ddocs=true} \
	-Dvapi=%{__true_false vala}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

%meson_install

%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblayer-shell-preload.so $RPM_BUILD_ROOT%{_libdir}/%{name}

%{?with_static_libs:%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblayer-shell-preload.a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libgtk4-layer-shell.so.*.*.*
%ghost %{_libdir}/libgtk4-layer-shell.so.0
%{_libdir}/girepository-1.0/Gtk4LayerShell-1.0.typelib
%{_libdir}/girepository-1.0/Gtk4SessionLock-1.0.typelib

%files preload
%defattr(644,root,root,755)
%doc layer_shell_preload.md
%attr(755,root,root) %{_libdir}/%{name}/liblayer-shell-preload.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgtk4-layer-shell.so
%dir %{_includedir}/gtk4-layer-shell
%{_includedir}/gtk4-layer-shell/gtk4-layer-shell.h
%{_includedir}/gtk4-layer-shell/gtk4-session-lock.h
%{_pkgconfigdir}/gtk4-layer-shell-0.pc
%{_datadir}/gir-1.0/Gtk4LayerShell-1.0.gir
%{_datadir}/gir-1.0/Gtk4SessionLock-1.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtk4-layer-shell.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gtk4-layer-shell
%endif

%if %{with vala}
%files -n vala-gtk4-layer-shell
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gtk4-layer-shell-0.deps
%{_datadir}/vala/vapi/gtk4-layer-shell-0.vapi
%endif
