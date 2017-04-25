#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse
import glob
import os
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", dest="in_path",
                        help="path to folder containg wallpapers")

    args = parser.parse_args()

    regex = re.compile('xkcd([0-9]*)')

    for file in glob.glob(os.path.join(args.in_path, "*.png")):
        n = regex.findall(file)
        if len(n) > 0:
            print n[0],