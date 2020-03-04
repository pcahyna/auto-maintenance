#!/bin/bash
# SPDX-License-Identifier: MIT

set -euo pipefail

if [ "${DEBUG:-false}" = true ] ; then
    set -x
fi

LSR_GH_ORG=${LSR_GH_ORG:-linux-system-roles}
LSR_BASE_DIR=${LSR_BASE_DIR:-~/linux-system-roles}

if ! type -p hub > /dev/null 2>&1 ; then
    echo ERROR: you must use the \"hub\" command line tool
    echo for interacting with github
    echo see https://github.com/github/hub
    echo e.g. on Fedora - dnf -y install hub
    exit 1
fi

if ! type -p jq > /dev/null 2>&1 ; then
    echo ERROR: you must use the \"jq\" command line tool
    echo for parsing JSON
    echo see https://stedolan.github.io/jq/manual/
    echo e.g. on Fedora - dnf -y install jq
    exit 1
fi

if [ ! -d $LSR_BASE_DIR ] ; then
    mkdir -p $LSR_BASE_DIR
fi

pushd $LSR_BASE_DIR > /dev/null

# get the list of repos under lsr

gh_get_all() {
    local uri=$1
    local field=$2
    local page=1
    while hub api ${uri}?page=$page | jq -e -r "$field" ; do
        page=$( expr $page + 1 )
    done
}

repos=$( gh_get_all orgs/linux-system-roles/repos '.[].name' )

for repo in $repos ; do
    echo Repo: $repo
    if [ $repo = kernel_settings ] ; then
        echo skipping
        continue
    fi
    # get a local clone of the repo
    if [ ! -d $LSR_BASE_DIR/$repo ] ; then
        HUB_PROTOCOL=https hub clone $LSR_GH_ORG/$repo
    fi
    cd $LSR_BASE_DIR/$repo
    # should have a remote called origin that points to lsr/repo
    if ! git remote get-url origin | grep -q $LSR_GH_ORG/$repo ; then
        echo Error: non-standard git remote config - origin does not point
        echo to $LSR_GH_ORG/$repo
        git remote get-url origin
        echo please use git remote to configure origin to point to $LSR_GH_ORG/$repo
        exit 1
    fi
    # make sure we have a fork of this under our personal space
    # this will also create a git remote in the local repo if there
    # is not already one
    HUB_PROTOCOL=ssh hub fork
    git fetch
    if [ -n "${1:-}" ] ; then
        if ! "$@" ; then
            echo ERROR: command in $( pwd ) failed
        fi
    fi
    cd ..
done
