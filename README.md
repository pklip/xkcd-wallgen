xkcd-wallgen
============

Generate xkcd wallpapers using python with cairo and pango

This is an initial python scripting approach to generate nice wallpapers from [xkcd](www.xkcd.com) (All credits to Randall Munroe).
It is intended to be used on linux and uses cairo for drawing the comics and pango for typesetting all the text (including the mouse over tooltips) using the matching [xkcd font](https://github.com/ipython/xkcd-font) which needs to be installed to the system.

Usage
-----
The main script is xkcd-wallgen.py
```bash
usage: xkcd-wallgen.py [-h] [-n NUMBERS [NUMBERS ...] | -r] -d DIMS DIMS
                       [-o OUT_PATH]

This generates wallpapers using the comic number(s) from xkcd (or random) for
the specified image dimension and saves them to the output directory

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBERS [NUMBERS ...], --numbers NUMBERS [NUMBERS ...]
                        numbers of xkcd comics to compose
  -r, --random          use random xkcd comic
  -d DIMS DIMS, --dimensions DIMS DIMS
                        dimensions in order x y
  -o OUT_PATH, --output_path OUT_PATH
                        path to save images to
```
The example wallpaper in the folder examples was generated with
```bash
./xkcd-wallgen.py -n 1597 -d 1600 900 -o examples
```


Known-issues
------------
* positioning of the tooltip text is really experimental but works fine, for most comics (at least for popular display resolutions).
* very early xkcd comics used JPG image format instead of PNG. Those will fail since cairo offers only function to read and write to PNG.
* no scaling for different resolutions is done
