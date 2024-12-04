1. create your rpm build env for RPM < 4.6,4.7
mkdir -p ~/rpmbuild/{RPMS,SRPMS,BUILD,SOURCES,SPECS,tmp}

cat <<EOF >~/.rpmmacros
%_topdir   %(echo $HOME)/rpmbuild
%_tmppath  %{_topdir}/tmp
EOF

cd ~/rpmbuild
2. create the tarball of your project
mkdir toybinprog-1.0
mkdir -p toybinprog-1.0/usr/bin
mkdir -p toybinprog-1.0/etc/toybinprog
install -m 755 toybinprog toybinprog-1.0/usr/bin
install -m 644 toybinprog.conf toybinprog-1.0/etc/toybinprog/

tar -zcvf toybinprog-1.0.tar.gz toybinprog-1.0/
3. Copy to the sources dir
cp toybinprog-1.0.tar.gz SOURCES/

cat <<EOF > SPECS/toybinprog.spec
# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Summary: A very simple toy bin rpm package
Name: toybinprog
Version: 1.0
Release: 1
License: GPL+
Group: Development/Tools
SOURCE0 : %{name}-%{version}.tar.gz
URL: http://toybinprog.company.com/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# in builddir
cp -a * %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/*

%changelog
* Thu Apr 24 2009  Elia Pinto <devzero2000@rpm5.org> 1.0-1
- First Build

EOF
4. build the source and the binary rpm
rpmbuild -ba SPECS/toybinprog.spec