#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", dest="dir",
                        help="path to folder containing files to be linked to", required=True)
    parser.add_argument("-p", "--pattern", dest="pattern",
                        help="pattern of files to include (e.g. \"*.png\")", default="*")
    parser.add_argument("-s", "--symlink", dest="symlink",
                        help="symlink which will point to the random file", required=True)
    parser.add_argument("-f", "--force", dest="force",
                        help="enforce that link points to another file than before", action="store_true", default=False)

    args = parser.parse_args()

    files = glob.glob(os.path.join(args.dir, args.pattern))

    symlink_exists = os.path.isfile(args.symlink)
    symlink_is_link = os.path.islink(args.symlink)

    # if symlink already exists check it and remove it
    if symlink_exists:
        if symlink_is_link:
            symlink_target = os.readlink(args.symlink)

            if args.force:
                # remove file from list if symlink already points to that file
                for file in files:
                    if os.path.abspath(file) == os.path.abspath(symlink_target):
                        files.remove(file)

        os.remove(args.symlink)

    # pick random index of files list
    rnd = random.randrange(0, len(files))

    # set symlink to random file
    os.symlink(files[rnd], args.symlink)
    print os.readlink(args.symlink)
