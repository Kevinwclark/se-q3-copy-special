# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# give credits
__author__ = "Kevin Clark with help from JT"

import re
import os
import sys
import shutil
import subprocess
import argparse


def get_special_paths(dirname):
    """Given a dirname, returns a list of all its special files."""
    files = os.listdir(dirname)
    double_under_regex = r'__\w*__'
    paths = []

    for f in files:
        if re.search(double_under_regex, f):
            paths.append(os.path.abspath(os.path.join(dirname, f)))
    return paths


def create_dir(path):
    """ checks to see if the dir exists, if not create it"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            print(f"creation of dir {path} did not work")
            return False
    return True


def copy_to(path_list, dest_dir):
    """copies files to a given dir"""
    create_dir_status = create_dir(dest_dir)
    if not create_dir_status:
        return -1
    for f in path_list:
        shutil.copyfile(f, os.path.join(dest_dir, os.path.basename(f)))


def zip_to(path_list, dest_zip):
    """zip files into given zip dir"""
    cmd = ['zip', '-j', dest_zip]
    cmd.extend(path_list)
    subprocess.run(cmd)
    return True


def main(args):
    """Main driver code for copyspecial."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    parser.add_argument('from_dir',
                        help='directory to grab special files from')
    ns = parser.parse_args(args)
    path_list = get_special_paths(ns.from_dir)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    if ns.todir:
        copy_to(path_list, ns.todir)
    if ns.tozip:
        zip_to(path_list, ns.tozip)
    for path in path_list:
        print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
