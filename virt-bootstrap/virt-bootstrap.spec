%if ( 0%{?rhel} >= 8 || 0%{?fedora} >= 23 )
%global py_ver 3
%global python_sitelib %{python3_sitelib}
%global py_build %{py3_build}
%global py_install %{py3_install}
%global python %{__python3}
%else
%global py_ver 2
%global python_sitelib %{python2_sitelib}
%global py_build %{py2_build}
%global py_install %{py2_install}
%global python %{__python2}
%endif

Name: virt-bootstrap
Version: 1.1.1
Release: 3%{?dist}
Summary: System container rootfs creation tool

License: GPLv3+
URL: https://github.com/virt-manager/virt-bootstrap
Source0: https://virt-manager.org/download/sources/virt-bootstrap/%{name}-%{version}.tar.gz

# Upstream patches

BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/bin/git
BuildRequires: python%{py_ver}-devel
BuildRequires: python%{py_ver}-libguestfs
BuildRequires: python%{py_ver}-passlib
BuildRequires: python%{py_ver}-setuptools
BuildRequires: fdupes

%if 0%{?el7}
Requires: python-libguestfs
%else
Requires: python%{py_ver}-libguestfs
%endif
Requires: python%{py_ver}-passlib
Requires: skopeo
Requires: libvirt-sandbox

BuildArch: noarch

%description
Provides a way to create the root file system to use for
libvirt containers.

%prep
%autosetup -S git

%build
%py_build

%install
%py_install
%fdupes %{buildroot}%{_prefix}

# Replace '#!/usr/bin/env python%{py_ver}' with '#!/usr/bin/python%{py_ver}'
# The format is ideal for upstream, but not a distro. See:
# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for f in $(find %{buildroot} -type f -executable -print); do
    sed -i '1 s/^#!\/usr\/bin\/env python%{py_ver}/#!%{python}/' $f || :
done

# Delete '#!/usr/bin/env python'
# The format is ideal for upstream, but not a distro. See:
# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for f in $(find %{buildroot} -type f \! -executable -print); do
    sed -i '/^#!\/usr\/bin\/env python/d' $f || :
done

%files
%license LICENSE
%doc README.md ChangeLog AUTHORS
%{_bindir}/virt-bootstrap
%{python_sitelib}/virtBootstrap
%{python_sitelib}/virt_bootstrap-*.egg-info
%{_mandir}/man1/virt-bootstrap*

%changelog
* Thu Apr 30 2020 Jerzy Drozdz <jerzy.drozdz@jdsieci.pl> - 1.1.1-3
- Backport to EL7

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Fabiano Fidêncio <fabiano@fidencio.org> - 1.1.1-1
- Update to new upstream release: 1.1.1
- Resolves: rhbz#1727771

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.7

* Thu May 31 2018 Fabiano Fidêncio <fabiano@fidencio.org> -1.1.0-1
- Update to new upstream release: 1.1.0

* Thu May 17 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 1.0.0-2
- Set "BuildArch: noarch" as this is an arch independent package
- Drop "Buildroot" tag as it's obsolete
- Drop "%%defattr" tag as it's obsolete
- Add "BuildRequires: /usr/bin/git" (due to %%autosetup -S git)
- Add a note to make clear that the patches are backported from upstream
- Replace '#!/usr/bin/env python3' with '#!/usr/bin/python3'
- Delete '#!/usr/bin/env python' from non executable files

* Wed May 16 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 1.0.0-1
- Initial release
