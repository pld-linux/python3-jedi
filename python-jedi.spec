#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (failing at start as of 0.17.0)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	An autocompletion tool for Python that can be used for text editors
Summary(pl.UTF-8):	Narzędzie do automatycznego dopełaniania dla Pythona, nadające się do użycia w edytorach
Name:		python-jedi
# keep 0.17.x here for python2 support
Version:	0.17.2
Release:	7
License:	MIT (Jedi), Apache v2.0 (typeshed)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jedi/
Source0:	https://files.pythonhosted.org/packages/source/j/jedi/jedi-%{version}.tar.gz
# Source0-md5:	f012668907d76cebe9c4766f3b806fcf
URL:		https://pypi.org/project/jedi/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-colorama
BuildRequires:	python-docopt
BuildRequires:	python-parso >= 0.7.0
BuildRequires:	python-parso < 0.8.0
BuildRequires:	python-pytest >= 3.9.0
BuildRequires:	python-pytest < 5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-colorama
BuildRequires:	python3-docopt
BuildRequires:	python3-parso >= 0.7.0
BuildRequires:	python3-parso < 0.8.0
BuildRequires:	python3-pytest >= 3.9.0
BuildRequires:	python3-pytest < 5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-parso >= 0.7.0
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jedi is a static analysis tool for Python that is typically used in
IDEs/editors plugins. Jedi has a focus on autocompletion and goto
functionality. Other features include refactoring, code search and
finding references.

%description -l pl.UTF-8
Jedi to narzędzie do statycznej analizy kodu dla Pythona, zwykle
używane w IDE i wtyczkach do edytorów. Jedi skupia się na funkcjach
automatycznego dopełniania oraz przemieszczania po kodzie. Pozostałe
funkcje obejmują refaktorowanie, przeszukiwanie kodu i wyszukiwanie
odwołań.

%package -n python3-jedi
Summary:	An autocompletion tool for Python that can be used for text editors
Summary(pl.UTF-8):	Narzędzie do automatycznego dopełaniania dla Pythona, nadające się do użycia w edytorach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-jedi
Jedi is a static analysis tool for Python that is typically used in
IDEs/editors plugins. Jedi has a focus on autocompletion and goto
functionality. Other features include refactoring, code search and
finding references.

%description -n python3-jedi -l pl.UTF-8
Jedi to narzędzie do statycznej analizy kodu dla Pythona, zwykle
używane w IDE i wtyczkach do edytorów. Jedi skupia się na funkcjach
automatycznego dopełniania oraz przemieszczania po kodzie. Pozostałe
funkcje obejmują refaktorowanie, przeszukiwanie kodu i wyszukiwanie
odwołań.

%package apidocs
Summary:	API documentation for Python jedi module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jedi
Group:		Documentation

%description apidocs
API documentation for Python jedi module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jedi.

%prep
%setup -q -n jedi-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.rst LICENSE.txt README.rst
%{py_sitescriptdir}/jedi
%{py_sitescriptdir}/jedi-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jedi
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/jedi
%{py3_sitescriptdir}/jedi-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,docs,*.html,*.js}
%endif
