# https://github.com/include-what-you-use/include-what-you-use/issues/679
%global longname include-what-you-use
%global owner %{longname}
%undefine __brp_mangle_shebangs
# Should instead define specific ignores like
#global __requires_exclude_from run_iwyu_tests.py fix_includes_test.py

Name:           iwyu
Version:        0.19
Release:        0.1%{?dist}
Summary:        C/C++ source files \#include analyzer based on clang

License:        NCSA
URL:            https://github.com/%{owner}/%{longname}
Source0:        https://github.com/%{owner}/%{longname}/archive/refs/tags/include-what-you-use-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang-devel >= 12.0
# NOTE: This should probably listed as a dependency for clang-devel but it's
# not, so make it explicit here
BuildRequires:  llvm-devel
# Some of the Clang libraries are only available statically and the use of the
# static library was approved (see https://fedorahosted.org/fesco/ticket/1370 )
BuildRequires:  llvm-static
BuildRequires:  zlib-devel
BuildRequires:  git
# Scripts are Python 2
BuildRequires:  python2-devel
#BuildRequires:  ncurses-devel
BuildRequires: clang-tools-extra

# Virtual provide the long name
Provides:  include-what-you-use = %{version}-%{release}
Provides:  include-what-you-use%{?_isa} = %{version}-%{release}

# It isn't building on ARM, so just exclude it for now (see https://bugzilla.redhat.com/show_bug.cgi?id=1192713 )
# Also, the tests use x86 assembly right now (see https://groups.google.com/forum/#!topic/include-what-you-use/lEuN5tr-0y0 )
ExclusiveArch: %{ix86} x86_64


%description
"Include what you use" means this: for every symbol (type, function, variable,
or macro) that you use in foo.cc (or foo.cpp), either foo.cc or foo.h
should \#include a .h file that exports the declaration of that symbol. The
include-what-you-use tool is a program that can be built with the clang
libraries in order to analyze \#includes of source files to find
include-what-you-use violations, and suggest fixes for them.


%prep
%autosetup -n %{longname}-%{version}


%build
%cmake
%cmake_build


%install
%cmake_install
cd %{buildroot}%{_bindir}
ln -s include-what-you-use iwyu
ln -s fix_includes.py fix_includes
ln -s iwyu_tool.py iwyu_tool


%check
# Change dir into the build path chosen by cmake_install
cd %{__cmake_builddir}
# Need to have the clang headers at the correct relative path (see https://github.com/include-what-you-use/include-what-you-use/issues/100 )
ln -s %{_libdir} %{_lib}
PATH=$PWD/bin:$PATH
ln -s ../fix_includes.py
ln -s ../fix_includes_test.py
ln -s ../iwyu_test_util.py
ln -s ../run_iwyu_tests.py
ln -s ../tests
%{__python2} run_iwyu_tests.py
%{__python2} fix_includes_test.py


%files
%{_bindir}/include-what-you-use
%{_bindir}/iwyu
%{_bindir}/fix_includes
%{_bindir}/fix_includes.py
%{_bindir}/iwyu_tool
%{_bindir}/iwyu_tool.py
%dir %{_datadir}/include-what-you-use
%{_datadir}/include-what-you-use/*.imp
%{_mandir}/man1/*


%changelog
* Mon Mar 27 2023 Francois Poirotte <francois.poirotte@csgroup.eu> - 0.19-0.1
- Rebuild with latest upstream release (0.19)

* Sat Jun 19 2021 Edd Salkield <edd@salkield.uk> - 0.16-1
- Official 0.16/LLVM 4.0 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-0.5.20171001git576e80f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-0.4.20171001git576e80f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-0.3.20171001git576e80f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-0.2.20171001git576e80f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 04 2017 Tom Stellard <tstellar@redhat.com> - 0.9-0.1.20171001git576e80f
- Update to git snapshot that works with LLVM 5

* Wed Aug 02 2017 Dave Johansen <davejohansen@gmail.com> - 0.8-4
- Official 0.8/LLVM 4.0 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 02 2017 Dave Johansen <davejohansen@gmail.com> - 0.8-1
- Use 0.8 to work with LLVM 4.0

* Thu Mar 30 2017 Tom Stellard <tstellar@redhat.com> - 0.7-3.20130330git.23253ec
- Update to git snapshot that works with LLVM4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Dave Johansen <davejohansen@gmail.com> - 0.7-1
- Upstream release

* Thu May 12 2016 Dave Johansen <davejohansen@gmail.com> - 0.6-1
- Upstream release

* Wed Feb 24 2016 Dave Johansen <davejohansen@gmail.com> - 0.6-0.2
- Remove use of rand() in badinc test

* Wed Feb 24 2016 Dave Johansen <davejohansen@gmail.com> - 0.6-0.1
- Test build against 3.8

* Thu Feb 04 2016 Dave Johansen <davejohansen@gmail.com> - 0.5-3
- Changes for new llvm cmake build system

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Dave Johansen <davejohansen@gmail.com> - 0.5-1
- Upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Dave Johansen <davejohansen@gmail.com> - 0.4-2
- Added iwyu_tool

* Mon Jun 01 2015 Dave Johansen <davejohansen@gmail.com> - 0.4-1
- Update to 0.4 based on clang 3.6.0

* Tue Jan 27 2015 Dave Johansen <davejohansen@gmail.com> - 0.3-1
- Update to 0.3 based on clang 3.5.0

* Fri Apr 25 2014 Dave Johansen <davejohansen@gmail.com> - 0.2-1
- Initial RPM release
