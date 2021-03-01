%if 0%{?rhel} && ! 0%{?epel}
%bcond_with ansible
%else
%bcond_without ansible
%endif

%if 0%{?rhel}
Name: rhel-system-roles
%else
Name: linux-system-roles
%endif
Url: https://github.com/linux-system-roles/
Summary: Set of interfaces for unified system management
Version: 1.0.0
Release: 32%{?dist}

#Group: Development/Libraries
License: GPLv3+ and MIT and BSD
%global installbase %{_datadir}/linux-system-roles
%global _pkglicensedir %{_licensedir}/%{name}
%global rolealtprefix linux-system-roles.
%global roleprefix %{name}.
%global roleinstprefix %{nil}
%global rolealtrelpath ../../linux-system-roles/
%if 0%{?rhel}
%global roleinstprefix %{roleprefix}
%global installbase %{_datadir}/ansible/roles
%global rolealtrelpath %{nil}
%endif

%if 0%{?rhel}
%global collection_namespace redhat
%global collection_name rhel_system_roles
%else
%global collection_namespace fedora
%global collection_name linux_system_roles
%endif
%global subrole_prefix "private_${role}_subrole_"

%global collection_version %{version}

# Helper macros originally from macros.ansible by Igor Raits <ignatenkobrain>
# Not available on RHEL, so we must define those macros locally here without using ansible-galaxy

# Not used (yet). Could be made to point to AH in RHEL - but what about CentOS Stream?
#%%{!?ansible_collection_url:%%define ansible_collection_url() https://galaxy.ansible.com/%%{collection_namespace}/%%{collection_name}}

%{!?ansible_collection_files:%define ansible_collection_files %{_datadir}/ansible/collections/ansible_collections/%{collection_namespace}/}

%if %{with ansible}
BuildRequires: ansible >= 2.9.10
%endif

%if %{undefined ansible_collection_build}
%if %{without ansible}
# Empty command. We don't have ansible-galaxy.
%define ansible_collection_build() :
%else
%define ansible_collection_build() ansible-galaxy collection build
%endif
%endif

%if %{undefined ansible_collection_install}
%if %{without ansible}
# Simply copy everything instead of galaxy-installing the built artifact.
%define ansible_collection_install() mkdir -p %{buildroot}%{ansible_collection_files}; cp -a . %{buildroot}%{ansible_collection_files}/%{collection_name}/
%else
%define ansible_collection_install() ansible-galaxy collection install -n -p %{buildroot}%{_datadir}/ansible/collections %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif
%endif

# For each role, call either defcommit() or deftag(). The other macros
# (%%id and %%shortid) can be then used in the same way in both cases.
# This way  the rest of the spec file des not need to know whether we are
# dealing with a tag or a commit.
%global archiveext tar.gz
# list of role names
%global rolenames %nil
# list of assignments that can be used to populate a bash associative array variable
%global rolestodir %nil
%define getarchivedir() %(p=%{basename:%{S:%{1}}}; echo ${p%%.%{archiveext}})

%define defcommit() %{expand:%%global ref%{1} %{2}
%%global shortcommit%{1} %%(c=%%{ref%{1}}; echo ${c:0:7})
%%global extractdir%{1} %%{expand:%%getarchivedir %{1}}
%%{!?repo%{1}:%%global repo%{1} %%{rolename%{1}}}
%%global archiveurl%{1} %%{?forgeorg%{1}}%%{!?forgeorg%{1}:%%{url}}%%{repo%{1}}/archive/%%{ref%{1}}/%%{repo%{1}}-%%{ref%{1}}.tar.gz
%%global rolenames %%{?rolenames} %%{rolename%{1}}
%%global roletodir%{1} [%{rolename%{1}}]="%{extractdir%{1}}"
%%global rolestodir %%{?rolestodir} %{roletodir%{1}}
}

%define deftag() %{expand:%%global ref%{1} %{2}
%%global extractdir%{1} %%{expand:%%getarchivedir %{1}}
%%{!?repo%{1}:%%global repo%{1} %%{rolename%{1}}}
%%global archiveurl%{1} %%{?forgeorg%{1}}%%{!?forgeorg%{1}:%%{url}}%%{repo%{1}}/archive/%%{ref%{1}}/%%{repo%{1}}-%%{ref%{1}}.tar.gz
%%global rolenames %%{?rolenames} %%{rolename%{1}}
%%global roletodir%{1} [%{rolename%{1}}]="%{extractdir%{1}}"
%%global rolestodir %%{?rolestodir} %%{roletodir%{1}}
}

#%%defcommit 1 43eec5668425d295dce3801216c19b1916df1f9b
%global rolename1 postfix
%deftag 1 0.1

#%%defcommit 2 6cd1ec8fdebdb92a789b14e5a44fe77f0a3d8ecd
%global rolename2 selinux
%deftag 2 1.1.1

%defcommit 3 924650d0cd4117f73a7f0413ab745a8632bc5cec
%global rolename3 timesync
#%%deftag 3 1.0.0

%defcommit 4 77596fdd976c6160d6152c200a5432c609725a14
%global rolename4 kdump
#%%deftag 4 1.0.0

%defcommit 5 bda206d45c87ee8c1a5284de84f5acf5e629de97
%global rolename5 network
#%%deftag 5 1.0.0

%defcommit 6 485de47b0dc0787aea077ba448ecb954f53e40c4
%global rolename6 storage
#%%deftag 6 1.2.2

%defcommit 7 e81b2650108727f38b1c856699aad26af0f44a46
%global rolename7 metrics
#%%deftag 7 0.1.0

#%%defcommit 8 cfa70b6b5910b3198aba2679f8fc36aad45ca45a
%global rolename8 tlog
%deftag 8 1.1.0

%defcommit 9 e5e5abb35fb695e22ccffa855c98ab882650480e
%global rolename9 kernel_settings
#%%deftag 9 1.0.1

%defcommit 10 4b07edf4e84882c9d0fb979092ba5953aac0b4d5
%global rolename10 logging
#%%deftag 10 0.2.0

#%%defcommit 11 4b6cfca4dd24e53a4bc4e07635601d7c104346c1
%global rolename11 nbde_server
%deftag 11 1.0.1

%defcommit 12 3af7452e4861ee2363b29b23bf78bf11e06be142
%global rolename12 nbde_client
#%%deftag 12 1.0.1

%defcommit 13 50041ce55348fcce34aba4cbe3ea160c5d890ab3
%global rolename13 certificate
#%%deftag 13 1.0.1

%defcommit 14 76b2d5b0460dba22c5d290c1af96e4fdb3434cb9
%global rolename14 crypto_policies

%global forgeorg15 https://github.com/willshersystems/
%global repo15 ansible-sshd
%global rolename15 sshd
%defcommit 15 032054b47813692874ac76ca8d601ed4b97bcbdc

%defcommit 16 effa0a0d993832dee726290f263a2182cf3eacda
%global rolename16 ssh

%defcommit 17 779bb78559de58bb5a1f25a4b92039c373ef59a4
%global rolename17 ha_cluster

%global mainid e5ed203b2d7224c0bf0c3fd55452456c8f468cad
Source: %{url}auto-maintenance/archive/%{mainid}/auto-maintenance-%{mainid}.tar.gz
Source1: %{archiveurl1}
Source2: %{archiveurl2}
Source3: %{archiveurl3}
Source4: %{archiveurl4}
Source5: %{archiveurl5}
Source6: %{archiveurl6}
Source7: %{archiveurl7}
Source8: %{archiveurl8}
Source9: %{archiveurl9}
Source10: %{archiveurl10}
Source11: %{archiveurl11}
Source12: %{archiveurl12}
Source13: %{archiveurl13}
Source14: %{archiveurl14}
Source15: %{archiveurl15}
Source16: %{archiveurl16}
Source17: %{archiveurl17}

# Script to convert the collection README to Automation Hub.
# Not used on Fedora.
Source998: collection_readme.sh

# Patch11: rhel-system-roles-postfix-pr5.diff
# Patch12: postfix-meta-el8.diff

# Patch21: selinux-tier1-tags.diff
# Patch22: selinux-bz-1926947-no-variable-named-present.diff

# Patch31: timesync-tier1-tags.diff

# Patch41: rhel-system-roles-kdump-pr22.diff
# Patch42: kdump-tier1-tags.diff
# Patch43: kdump-meta-el8.diff
# Patch44: kdump-fix-newline.diff

# Patch51: network-epel-minimal.diff
# # Not suitable for upstream, since the files need to be executable there
# Patch52: network-permissions.diff
# Patch53: network-tier1-tags.diff
# Patch55: network-disable-bondtests.diff
# Patch56: network-pr353.diff

# Patch62: storage-partition-name.diff
# Patch63: storage-no-disks-existing.diff
# Patch64: storage-trim-volume-size.diff

# Patch71: metrics-mssql-x86.diff

# Patch151: sshd-example.diff
# Patch152: sshd-work-on-ansible28-jinja27.diff

BuildArch: noarch

# These are needed for md2html.sh to build the documentation
BuildRequires: asciidoc
BuildRequires: pandoc
BuildRequires: highlight
BuildRequires: python3
BuildRequires: python3-six
BuildRequires: python3dist(ruamel.yaml)

Requires: python3-jmespath

Obsoletes: rhel-system-roles-techpreview < 1.0-3

%if %{undefined __ansible_provides}
Provides: ansible-collection(%{collection_namespace}.%{collection_name}) = %{collection_version}
%endif
# be compatible with the usual Fedora Provides:
Provides: ansible-collection-%{collection_namespace}-%{collection_name} = %{version}-%{release}

# We need to put %%description within the if block to avoid empty
# lines showing up.
%if 0%{?rhel}
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Red Hat Enterprise Linux.
%else
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Fedora, Red Hat Enterprise Linux & CentOS.
%endif

%prep
%setup -q -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -n %{getarchivedir 0}

declare -A ROLESTODIR=(%{rolestodir})
for rolename in %{rolenames}; do
    mv "${ROLESTODIR[${rolename}]}" ${rolename}
done

cd %{rolename1}
#%%patch11 -p1
#%%patch12 -p1
cd ..
cd %{rolename2}
#%%patch21 -p1
#%%patch22 -p1
cd ..
cd %{rolename3}
#%%patch31 -p1
cd ..
cd %{rolename4}
#%%patch41 -p1
#%%patch42 -p1
#%%patch43 -p1
#%%patch44 -p1
cd ..
cd %{rolename5}
#%%patch51 -p1
#%%patch52 -p1
#%%patch53 -p1
#%%patch55 -p1
#%%patch56 -p1
cd ..
cd %{rolename6}
#%%patch62 -p1
#%%patch63 -p1
#%%patch64 -p1
cd ..
cd %{rolename7}
#%%patch71 -p1
cd ..
cd %{rolename15}
#%%patch151 -p1
#%%patch152 -p1
sed -r -i -e "s/ansible-sshd/linux-system-roles.sshd/" tests/*.yml examples/*.yml README.md
cd ..

# Replacing "linux-system-roles.rolename" with "rhel-system-roles.rolename" in each role
%if "%{roleprefix}" != "linux-system-roles."
for rolename in %{rolenames}; do
    find $rolename -type f -exec \
         sed "s/linux-system-roles[.]${rolename}\\>/%{roleprefix}${rolename}/g" -i {} \;
done
%endif

# Removing symlinks in tests/roles
for rolename in %{rolenames}; do
    if [ -d ${rolename}/tests/roles ]; then
        find ${rolename}/tests/roles -type l -exec rm {} \;
        if [ -d ${rolename}/tests/roles/linux-system-roles.${rolename} ]; then
            rm -r ${rolename}/tests/roles/linux-system-roles.${rolename}
        fi
    fi
done
rm %{rolename5}/tests/modules
rm %{rolename5}/tests/module_utils
rm %{rolename5}/tests/playbooks/roles

# transform ambiguous #!/usr/bin/env python shebangs to python3 to stop brp-mangle-shebangs complaining
find -type f -executable -name '*.py' -exec \
     sed -i -r -e '1s@^(#! */usr/bin/env python)(\s|$)@#\13\2@' '{}' +

%build
sh md2html.sh \
%{rolename1}/README.md \
%{rolename2}/README.md \
%{rolename3}/README.md \
%{rolename4}/README.md \
%{rolename5}/README.md \
%{rolename6}/README.md \
%{rolename7}/README.md \
%{rolename8}/README.md \
%{rolename9}/README.md \
%{rolename10}/README.md \
%{rolename11}/README.md \
%{rolename12}/README.md \
%{rolename13}/README.md \
%{rolename14}/README.md \
%{rolename15}/README.md \
%{rolename16}/README.md \
%{rolename17}/README.md

mkdir .collections
%if 0%{?rhel}
# Convert the upstream collection readme to the downstream one
%{SOURCE998} lsr_role2collection/collection_readme.md
%endif
./galaxy_transform.py "%{collection_namespace}" "%{collection_name}" "%{collection_version}" > galaxy.yml.tmp
mv galaxy.yml.tmp galaxy.yml

for role in %{rolename1} %{rolename2} %{rolename3} \
    %{rolename4} %{rolename5} %{rolename6} \
    %{rolename7} %{rolename8} %{rolename9} \
    %{rolename10} %{rolename11} %{rolename12} \
    %{rolename13} %{rolename14} %{rolename15} \
    %{rolename16} %{rolename17}; do
    python3 lsr_role2collection.py --role "$role" --src-path "$role" \
        --src-owner %{name} --subrole-prefix %{subrole_prefix} --dest-path .collections \
        --readme lsr_role2collection/collection_readme.md \
        --namespace %{collection_namespace} --collection %{collection_name}
done

cp -p galaxy.yml lsr_role2collection/.ansible-lint \
    .collections/ansible_collections/%{collection_namespace}/%{collection_name}
mkdir -p .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/sanity
cp -p lsr_role2collection/ignore-2.9.txt \
    .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/sanity

cd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_build

%install
mkdir -p $RPM_BUILD_ROOT%{installbase}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

cp -pR %{rolename1}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename1}
cp -pR %{rolename2}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename2}
cp -pR %{rolename3}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename3}
cp -pR %{rolename4}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename4}
cp -pR %{rolename5}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename5}
cp -pR %{rolename6}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename6}
cp -pR %{rolename7}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename7}
cp -pR %{rolename8}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename8}
cp -pR %{rolename9}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename9}
cp -pR %{rolename10}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename10}
cp -pR %{rolename11}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename11}
cp -pR %{rolename12}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename12}
cp -pR %{rolename13}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename13}
cp -pR %{rolename14}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename14}
cp -pR %{rolename15}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename15}
cp -pR %{rolename16}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename16}
cp -pR %{rolename17}      $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}%{rolename17}

%if 0%{?rolealtprefix:1}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename1}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename1}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename2}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename2}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename3}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename3}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename4}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename4}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename5}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename5}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename6}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename6}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename7}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename7}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename8}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename8}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename9}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename9}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename10}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename10}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename11}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename11}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename12}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename12}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename13}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename13}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename14}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename14}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename15}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename15}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename16}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename16}
ln -s    %{rolealtrelpath}%{roleinstprefix}%{rolename17}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename17}
%endif

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kdump
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/postfix
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/network
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/storage
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/metrics
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/tlog
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kernel_settings
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/logging
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_server
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_client
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/certificate
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/crypto_policies
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/sshd
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/ssh
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/ha_cluster
mkdir -p $RPM_BUILD_ROOT%{_pkglicensedir}

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kdump/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kdump/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kdump
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kdump/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/kdump.COPYING

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}postfix/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}postfix/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/postfix
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}postfix/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/postfix.COPYING

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}selinux/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}selinux/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}selinux/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/selinux.COPYING
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}selinux/selinux-playbook.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux/example-selinux-playbook.yml

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}timesync/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}timesync/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}timesync/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/timesync.COPYING
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}timesync/examples/multiple-ntp-servers.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}timesync/examples/single-pool.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-pool-playbook.yml

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/network.LICENSE
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/bond_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/bridge_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bridge_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/eth_simple_auto.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_simple_auto-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/eth_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/infiniband.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-infiniband-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/macvlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-macvlan-playbook.yml
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/remove_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-remove_profile-playbook.yml
rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/remove_profile.yml
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/down_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-down_profile-playbook.yml
rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/down_profile.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/inventory \
   $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-inventory
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/ethtool_features.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-ethtool_features-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/ethtool_features_default.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-ethtool_features_default-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/bond_simple.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond_simple-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/eth_with_802_1x.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_with_802_1x-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/wireless_wpa_psk.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-wireless_wpa_psk-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/remove+down_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-remove+down_profile-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/dummy_simple.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-dummy_simple-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/ethtool_coalesce.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-ethtool_coalesce-playbook.yml
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/team_simple.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-team_simple-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth_dns_support.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_dns_support-playbook.yml

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}storage/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}storage/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/storage
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}storage/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/storage.LICENSE

rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/semaphore
rm -r $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/molecule

rm -r $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/.[A-Za-z]*
rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/tests/.git*

rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/roles
rmdir $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}metrics/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}metrics/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/metrics
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}metrics/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/metrics.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}tlog/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}tlog/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/tlog
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}tlog/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/tlog.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kernel_settings/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kernel_settings/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kernel_settings
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kernel_settings/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/kernel_settings.LICENSE
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}kernel_settings/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/kernel_settings.COPYING

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}logging/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}logging/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/logging
cp -p  $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}logging/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/logging.LICENSE
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}logging/COPYING \
    $RPM_BUILD_ROOT%{_pkglicensedir}/logging.COPYING

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_server/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_server/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_server
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_server/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/nbde_server.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_client/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_client/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_client
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}nbde_client/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/nbde_client.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}certificate/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}certificate/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/certificate
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}certificate/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/certificate.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}crypto_policies/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}crypto_policies/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/crypto_policies
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}crypto_policies/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/crypto_policies.LICENSE

cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}sshd/README.md \
    $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}sshd/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/sshd
cp -p $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}sshd/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/sshd.LICENSE
# referenced in the configuring-openssh-servers-using-the-sshd-system-role documentation module
# must be updated if changing the file path
mv $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}sshd/examples/example-root-login.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/sshd/example-root-login-playbook.yml
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}sshd/examples

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ssh/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ssh/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/ssh
cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ssh/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/ssh.LICENSE

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ha_cluster/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ha_cluster/README.html \
    $RPM_BUILD_ROOT%{_pkgdocdir}/ha_cluster
cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ha_cluster/LICENSE \
    $RPM_BUILD_ROOT%{_pkglicensedir}/ha_cluster.LICENSE
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ha_cluster/examples/simple.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/ha_cluster/example-simple-playbook.yml
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}ha_cluster/examples

cd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_install


%files
%if %{without ansible}
%dir %{_datadir}/ansible
%dir %{_datadir}/ansible/roles
%endif
%if "%{installbase}" != "%{_datadir}/ansible/roles"
%dir %{installbase}
%endif
%if 0%{?rolealtprefix:1}
%{_datadir}/ansible/roles/%{rolealtprefix}kdump
%{_datadir}/ansible/roles/%{rolealtprefix}postfix
%{_datadir}/ansible/roles/%{rolealtprefix}selinux
%{_datadir}/ansible/roles/%{rolealtprefix}timesync
%{_datadir}/ansible/roles/%{rolealtprefix}network
%{_datadir}/ansible/roles/%{rolealtprefix}storage
%{_datadir}/ansible/roles/%{rolealtprefix}metrics
%{_datadir}/ansible/roles/%{rolealtprefix}tlog
%{_datadir}/ansible/roles/%{rolealtprefix}kernel_settings
%{_datadir}/ansible/roles/%{rolealtprefix}logging
%{_datadir}/ansible/roles/%{rolealtprefix}nbde_server
%{_datadir}/ansible/roles/%{rolealtprefix}nbde_client
%{_datadir}/ansible/roles/%{rolealtprefix}certificate
%{_datadir}/ansible/roles/%{rolealtprefix}crypto_policies
%{_datadir}/ansible/roles/%{rolealtprefix}sshd
%{_datadir}/ansible/roles/%{rolealtprefix}ssh
%{_datadir}/ansible/roles/%{rolealtprefix}ha_cluster
%endif
%{installbase}/%{roleinstprefix}kdump
%{installbase}/%{roleinstprefix}postfix
%{installbase}/%{roleinstprefix}selinux
%{installbase}/%{roleinstprefix}timesync
%{installbase}/%{roleinstprefix}network
%{installbase}/%{roleinstprefix}storage
%{installbase}/%{roleinstprefix}metrics
%{installbase}/%{roleinstprefix}tlog
%{installbase}/%{roleinstprefix}kernel_settings
%{installbase}/%{roleinstprefix}logging
%{installbase}/%{roleinstprefix}nbde_server
%{installbase}/%{roleinstprefix}nbde_client
%{installbase}/%{roleinstprefix}certificate
%{installbase}/%{roleinstprefix}crypto_policies
%{installbase}/%{roleinstprefix}sshd
%{installbase}/%{roleinstprefix}ssh
%{installbase}/%{roleinstprefix}ha_cluster
%{_pkgdocdir}/*/example-*-playbook.yml
%{_pkgdocdir}/network/example-inventory
%{_pkgdocdir}/*/README.md
%{_pkgdocdir}/*/README.html
%doc %{installbase}/%{roleinstprefix}kdump/README.md
%doc %{installbase}/%{roleinstprefix}postfix/README.md
%doc %{installbase}/%{roleinstprefix}selinux/README.md
%doc %{installbase}/%{roleinstprefix}timesync/README.md
%doc %{installbase}/%{roleinstprefix}network/README.md
%doc %{installbase}/%{roleinstprefix}storage/README.md
%doc %{installbase}/%{roleinstprefix}metrics/README.md
%doc %{installbase}/%{roleinstprefix}tlog/README.md
%doc %{installbase}/%{roleinstprefix}kernel_settings/README.md
%doc %{installbase}/%{roleinstprefix}logging/README.md
%doc %{installbase}/%{roleinstprefix}nbde_server/README.md
%doc %{installbase}/%{roleinstprefix}nbde_client/README.md
%doc %{installbase}/%{roleinstprefix}certificate/README.md
%doc %{installbase}/%{roleinstprefix}crypto_policies/README.md
%doc %{installbase}/%{roleinstprefix}sshd/README.md
%doc %{installbase}/%{roleinstprefix}ssh/README.md
%doc %{installbase}/%{roleinstprefix}kdump/README.html
%doc %{installbase}/%{roleinstprefix}postfix/README.html
%doc %{installbase}/%{roleinstprefix}selinux/README.html
%doc %{installbase}/%{roleinstprefix}timesync/README.html
%doc %{installbase}/%{roleinstprefix}network/README.html
%doc %{installbase}/%{roleinstprefix}storage/README.html
%doc %{installbase}/%{roleinstprefix}metrics/README.html
%doc %{installbase}/%{roleinstprefix}tlog/README.html
%doc %{installbase}/%{roleinstprefix}kernel_settings/README.html
%doc %{installbase}/%{roleinstprefix}logging/README.html
%doc %{installbase}/%{roleinstprefix}nbde_server/README.html
%doc %{installbase}/%{roleinstprefix}nbde_client/README.html
%doc %{installbase}/%{roleinstprefix}certificate/README.html
%doc %{installbase}/%{roleinstprefix}crypto_policies/README.html
%doc %{installbase}/%{roleinstprefix}sshd/README.html
%doc %{installbase}/%{roleinstprefix}ssh/README.html
%doc %{installbase}/%{roleinstprefix}ha_cluster/README.html

%license %{_pkglicensedir}/*
%license %{installbase}/%{roleinstprefix}kdump/COPYING
%license %{installbase}/%{roleinstprefix}postfix/COPYING
%license %{installbase}/%{roleinstprefix}selinux/COPYING
%license %{installbase}/%{roleinstprefix}timesync/COPYING
%license %{installbase}/%{roleinstprefix}network/LICENSE
%license %{installbase}/%{roleinstprefix}storage/LICENSE
%license %{installbase}/%{roleinstprefix}metrics/LICENSE
%license %{installbase}/%{roleinstprefix}tlog/LICENSE
%license %{installbase}/%{roleinstprefix}kernel_settings/LICENSE
%license %{installbase}/%{roleinstprefix}kernel_settings/COPYING
%license %{installbase}/%{roleinstprefix}logging/LICENSE
%license %{installbase}/%{roleinstprefix}logging/COPYING
%license %{installbase}/%{roleinstprefix}nbde_server/LICENSE
%license %{installbase}/%{roleinstprefix}nbde_client/LICENSE
%license %{installbase}/%{roleinstprefix}certificate/LICENSE
%license %{installbase}/%{roleinstprefix}crypto_policies/LICENSE
%license %{installbase}/%{roleinstprefix}sshd/LICENSE
%license %{installbase}/%{roleinstprefix}ssh/LICENSE
%license %{installbase}/%{roleinstprefix}ha_cluster/LICENSE

%{ansible_collection_files}

%changelog
* Tue Feb 23 2021 Fernando Fernandez Mancera <ferferna@redhat.com> - 1.0.0-32
- Add patch for the inclusive language leftover on network-role README.md,
  Resolves rhbz#1931931

* Mon Feb 22 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-31
- Rebase certificate role to pick up a test fix, Resolves rhbz#1931568
- Rebase logging role to fix default private key path,
  upstream PR #218

* Mon Feb 22 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-30
- Correct merge botch in previous (ssh/README.md is a doc file)
- Update galaxy.yml even on Fedora, auto-maintenance may not have
  a consistent version number
- Update collection doc transformation to match a modified text
  and include the Tech Preview note again

* Thu Feb 18 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-29
- Change internal role prefix to more descriptive private_${role}_subrole_
- Sync spec improvements from Fedora and introduce helper macros
  No functional change except for license files location
- Disable mssql metrics test on non-x86_64 where the packages
  are not available. Upstream PR #73

* Wed Feb 17 2021 Rich Megginson <rmeggins@redhat.com> - 1.0.0-28
- Add patch for sshd https://github.com/willshersystems/ansible-sshd/pull/155
  for ansible 2.8/jinja 2.7 support for sshd role
- Rebase certificate, kernel_settings, nbde_client for jinja27
- Rebase the logging role, Resolves rhbz#1927943
- Rebase storage role, Resolves rhbz#1894651 - interpreatation of
  omitted parameters
- Apply storage PR #201 to dispense with the need of listing all disks
  in existing pools, Resolves rhbz1894676
- Apply storage PR #199 to allow reducing the requested volume sizes
  if needed to fit, Resolves rhbz1894647
- Rebase the network role, Resolves rhbz1893959, rhbz1893957
- Add the ssh client role, Resolves rhbz1893712
- Minor issue in selinux - no variable named present
  Resolves rhbz1926947
- Prefix internal roles with private_, resolves rhbz#1927417
- Add the ha_cluster role, Resolves rhbz#1893743

* Thu Feb 11 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-27
- Rebase the logging role, Resolves rhbz#1889484
- Fixes to collection docs and galaxy metadata from nhosoi
- Apply network PR #350 Resolves rhbz#1927392

* Wed Feb  3 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-26
- Rebase the metrics role, Resolves rhbz#1895188, rhbz#1893908

* Tue Jan 26 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-25
- Apply storage PR #153 to fix a problem with partition name on NVMe devices
  Resolves: rhbz1865990
- Remove symlinks to roles under tests
- Cleanup of role directories - remove files starting with . in roles' root
  directories and Git files under tests. Resolves rhbz#1650550
- Add collection support, make Version semver compatible: 1.0 -> 1.0.0
  Resolves rhbz#1893906
- Autogenerate Automation-Hub README.md if building for RHEL
- Renumber sources, Source is now auto-maintenance since it is the root
  of the source tree, kdump becomes Source4 (4 was originally firewall)
- Introduce bcond_with/without ansible, work on Fedora, RHEL and EPEL
- Rebase certificate role to include collection-related workarounds,
  no change in behavior intended
- Rebase network role, includes collection-related workarounds
- Revert an invasive network change to enable EPEL (PR #335) and implement
  a minimal version

* Fri Jan 15 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0-24
- Apply PR #63 for kdump to fix a problem in test introduced by rebase

* Fri Jan  8 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0-23
- Add {crypto_policies,sshd}/README.md to docfiles, thanks jjelen
- Fix role name in selinux patch
- Add sshd role example and README fix
- Fix role name in sshd role tests and docs
- Backport network role PR #298 to fix problems often triggered by the CI
  "error: down connection failed while waiting", Resolves rhbz#1817242
- Disable bond test in downstream CI, it started to break DNS in RHEL 8.4.
  Related rhbz#1915017

* Thu Jan  7 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0-22
- Rebase kdump, certificate, storage, selinux, nbde_client/server,
  kernel_settings in preparation for collections
  Includes upstream PR #168 for storage to prevent toggling encryption
  in safe mode, as it is a destructive operation. Resolves rhbz#1881524
- Introduce & use simpler macros for Sources management,
  similar to %%forgemeta
  https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/
- Use a script to perform prefix transformation for all roles to reduce
  the number of patches
- Rebase tlog to add exclude_{users,groups} support, Resolves rhbz#1895472
- Add crypto_policies role, Resolves rhbz#1893699
- Add sshd role, Resolves rhbz#1893696

* Mon Aug 24 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-19
- Rebase network role to latest upstream, resolves rhbz#1800627
  Drop a downstream patch with a test workaround that is not needed anymore.
- Fix script for role prefix transformation
- Rebase metrics role to pick up test changes, PR #19
- Rebase kernel_settings role to latest upstream, resolves rhbz#1851557

* Mon Aug 24 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-18
- Rebase storage role to latest upstream, resolves rhbz#1848254, rhbz#1851654,
  rhbz#1862867
- Rebase nbde_client role to latest upstream, resolves rhbz#1851654
- Rebase logging role to latest upstream, resolves rhbz#1851654, rhbz#1861318
- Rebase metrics role to latest upstream, resolves rhbz#1869390, rhbz#1869389,
  rhbz#1868378

* Fri Aug 21 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-17
- Rebase certificate role to latest upstream, resolves rhbz#1859547

* Mon Aug 10 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-16
- Rebase logging role to latest upstream, resolves rhbz#1854546, rhbz#1861318,
  rhbz#1860896, adds test for rhbz#1850790
- Rebase metrics role to latest upstream, resolves rhbz#1855544, rhbz#1855539,
  rhbz#1848763
- Fix whitespace in postfix role patch

* Fri Jul 31 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-15
- Rebase storage role to latest upstream, resolves rhbz#1854191, rhbz#1848250,
  rhbz#1850790 (including test)
- Rebase nbde_client role to latest upstream, adds test for rhbz#1850790
- Rebase certificate role to latest upstream, adds test for rhbz#1850790
- Rebase nbde_server role to latest upstream, resolves rhbz#1850790
  (including test)
- Rebase tlog role to latest upstream, resolves rhbz#1855424
- Rebase kernel_settings role to rev b8bc86b, resolves rhbz#1850790
- Add EL 8 to supported versions in postfix and kdump role metadata,
  resolves rhbz#1861661

* Mon Jul 20 2020 Rich Megginson <rmeggins@redhat.com> - 1.0-14
- Rebase certificate role to latest upstream, resolves rhbz#1858840

* Fri Jul 17 2020 Rich Megginson <rmeggins@redhat.com> - 1.0-13
- Rebase certificate role to latest upstream, resolves rhbz#1858316, rhbz#1848745

* Mon Jun 29 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-12
- Rebase network role to latest upstream, resolves rhbz#1822777, rhbz#1848472
- Rebase logging role to latest upstream, resolves rhbz#1850790,
  rhbz#1851804, rhbz#1848762
- Rebase certificate role to latest upstream, resolves rhbz#1848742,
  rhbz#1850790
- Rebase nbde_client role to latest upstream, resolves rhbz#1848766,
  rhbz#1850790

* Mon Jun 15 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-11
- Rebase network role to latest upstream
- Remove all the soon-unnecessary tier1 tags in test
- Add a workaround for rhbz#1800627 in test
- Modify patches to remove tier1 tags
- Add metrics, tlog, logging, kernel_settings roles
- Add nbde_client, nbde_server, certificate roles
- Rebase storage role to latest upstream: adds support for mdraid, LUKS,
  swap manangement

* Mon Oct 21 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-10
- Add the storage_safe_mode option, true by default, to prevent accidental
  data removal: rhbz#1763242, issue #42, PR #43 and #51.

* Thu Aug 15 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-9
- Add the storage role

* Thu Jun 13 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-7
- Update tests for the network role
- Fix typo in a test for the timesync role
- Tag tests suitable for Tier1 testing
- Rebase the network role to add support for device features (PR#115,
  rhbz#1696703) and atomic changes (PR#119, rhbz#1695161)
- network: apply upstream PR#121: allow modifying interface attributes
  without disrupting services (rhbz#1695157)

* Wed May 29 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-6
- Rebase the selinux role, fixes typo in tests, uncovered by Ansible 2.7,
  (rhbz#1677743) and lists all input variables in defaults
  to make Satellite aware of them (rhbz#1674004, PR#43)
- Rebase the kdump role to fix check mode problems: rhbz#1685904
- Rebase the timesync role: fixes check mode problems (rhbz#1685904)
  and lists all input variables in defaults (rhbz#1674004)
- Rebase the network role: keeps the interface up for state: up
  if persistent_state is absent and solves problems with defining
  VLAN and MACVLAN interface types (issue #19) (rhbz#1685902)

* Sat Jan 12 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-5
- spec file improvement: Unify the source macros with deftag() and defcommit()
- Update to upstream released versions and drop unnecessary patches.
- Unify the spec file with Fedora (no functional changes intended).
- Misc spec file comments fixes (by Mike DePaulo)
- Fix rpmlint error by escaping a previous changelog entry with a macro (by Mike DePaulo)
- Comply with Fedora guidelines by always using "cp -p" in %%install (by Mike DePaulo)
- Rebase network role - doc improvements, Fedora 29 and Ansible 2.7 support
- Regenerate network role patch to apply without offset
- Rebase kdump role to fix a forgotten edit, rhbz#1645633
- Update timesync examples: add var prefix (rhbz#1642152), correct role prefix
- Add Obsoletes for the -techpreview subpackage
- Add warnings to role READMEs and other doc updates, rhbz#1616018
- network: split the state setting into state and persistent_state, rhbz#1616014
- depend on python-jmespath as Ansible will not ship it, rhbz#1660559

* Tue Aug 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-4
- Format the READMEs as html, by vdolezal, with changes to use highlight
  (source-highlight does not understand YAML)

* Thu Aug  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-3
- Rebase the network role to the last revision (d866422).
  Many improvements to tests, introduces autodetection of the current provider
  and defaults to using profile name as interface name.
- Rebase the selinux, timesync and kdump roles to their 1.0rc1 versions.
  Many changes to the role interfaces to make them more consistent
  and conforming to Ansible best practices.
- Update the description.

* Fri May 11 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-4
- Fix complaints about /usr/bin/python during RPM build by making the affected scripts non-exec
- Fix merge botch

* Mon Mar 19 2018 Troy Dawson <tdawson@redhat.com> - 0.6-3.1
- Use -a (after cd) instead of -b (before cd) in %%setup

* Wed Mar 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-3
- Minor corrections of the previous change by Till Maas.

* Fri Mar  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-2
- Document network role options: static routes, ethernet, dns
  Upstream PR#36, bz1550128, documents bz1487747 and bz1478576

* Tue Jan 30 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-1
- Drop hard dependency on ansible (#1525655), patch from Yaakov Selkowitz
- Update the network role to version 0.4, solves bz#1487747, bz#1478576

* Tue Dec 19 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-3
- kdump: fix the wrong conditional for ssh checking and improve test (PR#10)

* Tue Nov 07 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-2
- kdump: add ssh support. upstream PR#9, rhbz1478707

* Tue Oct 03 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-1
- SELinux: fix policy reload when SELinux is disabled on CentOS/RHEL 6
  (bz#1493574)
- network: update to b856c7481bf5274d419f71fb62029ea0044b3ec1 :
  makes the network role idempotent (bz#1476053) and fixes manual
  network provider selection (bz#1485074).

* Mon Aug 28 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.4-1
- network: update to b9b6f0a7969e400d8d6ba0ac97f69593aa1e8fa5:
  ensure that state:absent followed by state:up works (bz#1478910), and change
  the example IP adresses to the IANA-assigned ones.
- SELinux: fix the case when SELinux is disabled (bz#1479546).

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-2
- We can't change directories to symlinks (rpm bug #447156) so keep the old
  names and create the new names as symlinks.

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-1
- Change the prefix to linux-system-roles., keeping compatibility
  symlinks.
- Update the network role to dace7654feb7b5629ded0734c598e087c2713265:
  adds InfiniBand support and other fixes.
- Drop a patch included upstream.

* Mon Jun 26 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-2
- Leave a copy of README and COPYING in every role's directory, as suggested by T. Bowling.
- Move the network example inventory to the documentation directory together.
  with the example playbooks and delete the now empty "examples" directory.
- Use proper reserved (by RFC 7042) MAC addresses in the network examples.

* Tue Jun 6 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-1
- Update the networking role to version 0.2 (#1459203)
- Version every role and the package separately. They live in separate repos
  and upstream release tags are not coordinated.

* Mon May 22 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-2
- Prefix the roles in examples and documentation with rhel-system-roles.

* Thu May 18 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-1
- Update to 0.1 (first upstream release).
- Remove the tuned role, it is not ready yet.
- Move the example playbooks to /usr/share/doc/rhel-system-roles/$SUBSYSTEM
  directly to get rid of an extra directory.
- Depend on ansible.

* Thu May 4 2017  Pavel Cahyna <pcahyna@redhat.com> - 0-0.1.20170504
- Initial release.
- kdump r. fe8bb81966b60fa8979f3816a12b0c7120d71140
- postfix r. 43eec5668425d295dce3801216c19b1916df1f9b
- selinux r. 1e4a21f929455e5e76dda0b12867abaa63795ae7
- timesync r. 33a1a8c349de10d6281ed83d4c791e9177d7a141
- tuned r. 2e8bb068b9815bc84287e9b6dc6177295ffdf38b
- network r. 03ff040df78a14409a0d89eba1235b8f3e50a750

