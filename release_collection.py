#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Red Hat, Inc.
# SPDX-License-Identifier: MIT

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

DEFAULT_GIT_SITE = "https://github.com"
DEFAULT_GIT_ORG = "linux-system-roles"


def build_collection(src_path, dest_path, galaxy, coll_rel, force):
    """
    Build a collection directory structure and the file.

    Convert the roles in src_path into a collection directory
    structure rooted at dest_path using the galaxy.yml metadata
    in galaxy and the collection_release metadata in coll_rel.
    The collection file for publishing will be in dest_path.
    """
    coll_dir = os.path.join(
        dest_path, "ansible_collections", galaxy["namespace"], galaxy["name"]
    )
    if os.path.isdir(coll_dir):
        if force:
            shutil.rmtree(coll_dir)
        else:
            raise Exception(
                "collection dest_path {} already exists - remove or use --force".format(
                    coll_dir
                )
            )
    os.makedirs(coll_dir, exist_ok=True)
    for rolename, roledata in coll_rel.items():
        if rolename.startswith("_"):
            continue
        roledir = os.path.join(src_path, rolename)
        if os.path.isdir(roledir):
            subprocess.check_call(["git", "fetch"], cwd=roledir)
            subprocess.check_call(
                ["git", "-c", "advice.detachedHead=false", "checkout", roledata["ref"]],
                cwd=roledir,
            )
            subprocess.check_call(["git", "pull"], cwd=roledir)
        else:
            git_url = "{}/{}/{}".format(
                DEFAULT_GIT_SITE,
                roledata.get("org", DEFAULT_GIT_ORG),
                roledata.get("repo", rolename),
            )
            subprocess.check_call(
                [
                    "git",
                    "-c",
                    "advice.detachedHead=false",
                    "clone",
                    "--depth",
                    "1",
                    "-q",
                    git_url,
                    "-b",
                    roledata["ref"],
                    roledir,
                ]
            )
        subprocess.check_call(
            [
                "python",
                "lsr_role2collection.py",
                "--src-owner",
                DEFAULT_GIT_ORG,
                "--role",
                rolename,
                "--src-path",
                src_path,
                "--dest-path",
                dest_path,
                "--namespace",
                galaxy["namespace"],
                "--collection",
                galaxy["name"],
            ]
        )
    shutil.copy(galaxy["_filename"], coll_dir)
    shutil.copy(coll_rel["_filename"], coll_dir)
    build_args = ["ansible-galaxy", "collection", "build", "-v"]
    if force:
        build_args.append("-f")
    build_args.append(coll_dir)
    subprocess.check_call(build_args, cwd=dest_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--galaxy-yml",
        type=open,
        default=os.environ.get("GALAXY_YML", "galaxy.yml"),
        help="Path/filename for galaxy.yml",
    )
    parser.add_argument(
        "--collection-release-yml",
        type=open,
        default=os.environ.get("COLLECTION_RELEASE_YML", "collection_release.yml"),
        help="Path/filename for collection_release.yml",
    )
    parser.add_argument(
        "--src-path",
        type=str,
        default=os.environ.get("COLLECTION_SRC_PATH"),
        help="Path to the directory containing the local clone of the role repos",
    )
    parser.add_argument(
        "--dest-path",
        type=str,
        default=os.environ.get(
            "COLLECTION_DEST_PATH", os.environ.get("HOME") + "/.ansible/collections"
        ),
        help=(
            "Path to collection base directory; collection directory structure "
            "will be created in DIR/ansible_collection/NAMESPACE/COLLECTION_NAME; "
            "collection package file will be created in DIR; "
            "default to ${HOME}/.ansible/collections"
        ),
    )
    parser.add_argument(
        "--force",
        default=False,
        action="store_true",
        help="Remove collection destination dir and file before creating",
    )
    args = parser.parse_args()

    galaxy = yaml.safe_load(args.galaxy_yml)
    galaxy["_filename"] = args.galaxy_yml.name
    coll_rel = yaml.safe_load(args.collection_release_yml)
    coll_rel["_filename"] = args.collection_release_yml.name
    workdir = None
    if not args.src_path:
        workdir = tempfile.mkdtemp(suffix=".lsr", prefix="collection")
        args.src_path = workdir
    try:
        build_collection(args.src_path, args.dest_path, galaxy, coll_rel, args.force)
    finally:
        if workdir:
            shutil.rmtree(workdir)


if __name__ == "__main__":
    sys.exit(main())
