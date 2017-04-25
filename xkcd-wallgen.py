#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import math

import argparse
import os.path

import urllib
import urllib2
from bs4 import BeautifulSoup

import cairo
import pango
import pangocairo

import tempfile


def resolveUrl(url):
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    finalurl = res.geturl()
    return finalurl


def getXkcdImageUrl(url):
    response = urllib.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    comic_div = soup.find_all(id="comic")
    img_url = comic_div[0].img["src"].strip("/")
    img_text = comic_div[0].img["title"]
    img_title = soup.find_all(id="ctitle")[0].text
    return img_url, img_title, img_text


def composeWallpaper(url, width, height, outfile):
    # create tempfile for intermediate image
    tmp_file = tempfile.NamedTemporaryFile()

    # resolve url
    res_url = resolveUrl(url)
    img_url, img_title, img_text = getXkcdImageUrl(res_url)
    urllib.urlretrieve("http://" + img_url, tmp_file.name)

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surf)

    # draw a background rectangle:
    context.rectangle(0, 0, width, height)
    context.set_source_rgb(1, 1, 1)
    context.fill()

    # draw picture
    pic_surf = cairo.ImageSurface.create_from_png(tmp_file.name)
    pic_width = pic_surf.get_width()
    pic_height = pic_surf.get_height()
    margin = 20
    width_ratio = float(width) / float(pic_width + 2 * margin)
    height_ratio = float(height) / float(pic_height + 2 * margin)
    scale_xy = min(height_ratio, width_ratio)
    scale_xy = min(1, scale_xy)

    context.save()
    context.translate((width - pic_width * scale_xy) / 2, (height - pic_height * scale_xy) / 2)
    context.scale(scale_xy, scale_xy)

    context.set_source_surface(pic_surf)
    context.paint()
    context.restore()

    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    layout = pangocairo_context.create_layout()

    # width of the text field (i know it's hacky but it looks good 99% of the time...)
    w = 420 if len(img_text) < 70 else (50 + int(math.sqrt(len(img_text))) * 40)
    #print w

    layout.set_width(int(round(w * pango.SCALE)))
    layout.set_wrap(pango.WRAP_WORD)
    font = pango.FontDescription("xkcd 15")
    layout.set_font_description(font)

    layout.set_text(img_text)
    context.set_source_rgb(0, 0, 0)

    text_width, text_height = layout.get_pixel_size()
    img_east = (width + pic_width * scale_xy) / 2
    img_west = (width - pic_width * scale_xy) / 2
    img_south = (height + pic_height * scale_xy) / 2
    if height - img_south > text_height + 2 * margin:
        # text under image
        text_xpos = min(width - text_width - margin, (img_west + img_east) / 2)
        text_ypos = img_south + margin
        layout_hyphen = pangocairo_context.create_layout()
        layout_hyphen.set_justify(pango.ALIGN_RIGHT)
        layout_hyphen.set_font_description(font)
        layout_hyphen.set_text("—")
        pangocairo_context.update_layout(layout_hyphen)
        context.move_to(text_xpos-15, text_ypos)
        layout_hyphen.context_changed()
        pangocairo_context.show_layout(layout_hyphen)

    else:
        # text right of image
        free_space_right = width - img_east
        if free_space_right < text_width + 2 * margin:
            layout.set_width(int(round((free_space_right - 2 * margin) * pango.SCALE)))
            text_width, text_height = layout.get_pixel_size()
        text_xpos = img_east + margin
        text_ypos = img_south - text_height

    pangocairo_context.update_layout(layout)
    context.move_to(text_xpos, text_ypos)
    layout.context_changed()
    pangocairo_context.show_layout(layout)

    # title+url
    layout_url = pangocairo_context.create_layout()
    layout_url.set_width(w * pango.SCALE)
    layout_url.set_wrap(pango.WRAP_WORD)
    font = pango.FontDescription("xkcd 12")
    layout_url.set_font_description(font)
    layout_url.set_text(img_title + "\n" + res_url)
    context.set_source_rgb(0, 0, 0)
    pangocairo_context.update_layout(layout_url)
    context.move_to(40, 40)
    layout_url.context_changed()
    pangocairo_context.show_layout(layout_url)

    with open(outfile, "wb") as image_file:
        surf.write_to_png(image_file)


if __name__ == "__main__":
    # img_url, img_text = getXkcdImageUrl("http://www.xkcd.com/482/");

    parser = argparse.ArgumentParser(description="This generates wallpapers using the comic number(s) from xkcd (or random) for the specified image dimension and saves them to the output directory")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--numbers", dest="numbers",
                        help="numbers of xkcd comics to compose", nargs="+")
    group.add_argument("-r", "--random", dest="random", action="store_true", default=True, help="use random xkcd comic")
    parser.add_argument("-d", "--dimensions", dest="dims",
                        help="dimensions in order x y", nargs=2, required=True)
    parser.add_argument("-o", "--output_path", dest="out_path",
                        help="path to save images to")

    args = parser.parse_args()
    if args.numbers is not None:
        args.random=False

    width = int(args.dims[0])
    height = int(args.dims[1])

    urls = []
    if args.random == True:
        urls.append(resolveUrl("https://c.xkcd.com/random/comic/"))

    if args.numbers is not None:
        for s in args.numbers:
            urls.append("https://xkcd.com/" + s + "/")

    for url in urls:
        try:
            n = filter(str.isdigit, url)
            filepath = "xkcd" + n + "_" + str(width) + "x" + str(height) +  ".png"
            if args.out_path is not None:
                filepath = os.path.join(args.out_path, filepath)
            print "Composing " + url + " to " + filepath
            composeWallpaper(url, width, height, filepath)
        except Exception as e:
            print "Something went wrong reading the image from " + url
            raise
