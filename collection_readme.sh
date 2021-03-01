#!/bin/bash

set -euxo pipefail

readme_md=${1:-"lsr_role2collection/collection_readme.md"}

sed -i -e '/## Currently supported distributions/{:1;/## Dependencies/!{N;b 1};s|.*|## Dependencies|}' \
    -e 's/\(Linux System Roles is a set of roles for managing Linux system components.\)/\1\n\nThis collection is available as a Technology Preview./' \
    -e 's/Linux/RHEL/g' \
    -e 's/Ansible Galaxy/Automation Hub/g' \
    -e 's/fedora\(.\)linux_system_roles/redhat\1rhel_system_roles/g' \
    -e 's/linux-system-roles/rhel-system-roles/g' \
    -e '/## Documentation/{:a;/## Support/!{N;b a};s|.*|## Documentation\nThe official RHEL System Roles documentation can be found in the [Product Documentation section of the Red Hat Customer Portal](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/administration_and_configuration_tasks_using_system_roles_in_rhel/index).\n\n## Support|}' \
    -e 's/$//' \
    $readme_md
