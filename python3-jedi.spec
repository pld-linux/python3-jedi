#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (failing at start as of 0.17.0)

Summary:	An autocompletion tool for Python that can be used for text editors
Summary(pl.UTF-8):	Narzędzie do automatycznego dopełaniania dla Pythona, nadające się do użycia w edytorach
Name:		python3-jedi
Version:	0.19.2
Release:	1
License:	MIT (Jedi), Apache v2.0 (typeshed)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jedi/
Source0:	https://files.pythonhosted.org/packages/source/j/jedi/jedi-%{version}.tar.gz
# Source0-md5:	bc2dfcc3fdcd7a1384867b5c6f5bf519
URL:		https://pypi.org/project/jedi/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-colorama
BuildRequires:	python3-docopt
BuildRequires:	python3-parso >= 0.8.4
BuildRequires:	python3-parso < 0.9.0
BuildRequires:	python3-pytest >= 3.9.0
BuildRequires:	python3-pytest < 9
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-parso >= 0.8.4
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-jedi
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/jedi
%{py3_sitescriptdir}/jedi-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,docs,*.html,*.js}
%endif
