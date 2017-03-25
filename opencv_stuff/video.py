#!/usr/bin/env python

'''
Video capture sample.

Sample shows how VideoCapture class can be used to acquire video
frames from a camera of a movie file. Also the sample provides
an example of procedural video generation by an object, mimicking
the VideoCapture interface (see Chess class).

'create_capture' is a convinience function for capture creation,
falling back to procedural video in case of error.

Usage:
    video.py [--shotdir <shot path>] [source0] [source1] ...'

    sourceN is an
     - integer number for camera capture
     - name of video file
     - synth:<params> for procedural video

Synth examples:
    synth:bg=../data/lena.jpg:noise=0.1
    synth:class=chess:bg=../data/lena.jpg:noise=0.1:size=640x480

Keys:
    ESC    - exit
    SPACE  - save current frame to <shot path> directory

'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
from numpy import pi, sin, cos

import cv2


from picamera.array import PiRGBArray
from picamera import PiCamera
import time


# built-in modules
from time import clock

# local modules
from tst_scene_render import TestSceneRender
import common

class VideoSynthBase(object):
    def __init__(self, size=None, noise=0.0, bg = None, **params):
        self.bg = None
        self.frame_size = (640, 480)
        if bg is not None:
            self.bg = cv2.imread(bg, 1)
            h, w = self.bg.shape[:2]
            self.frame_size = (w, h)

        if size is not None:
            w, h = map(int, size.split('x'))
            self.frame_size = (w, h)
            self.bg = cv2.resize(self.bg, self.frame_size)

        self.noise = float(noise)

    def render(self, dst):
        pass

    def read(self, dst=None):
        w, h = self.frame_size

        if self.bg is None:
            buf = np.zeros((h, w, 3), np.uint8)
        else:
            buf = self.bg.copy()

        self.render(buf)

        if self.noise > 0.0:
            noise = np.zeros((h, w, 3), np.int8)
            cv2.randn(noise, np.zeros(3), np.ones(3)*255*self.noise)
            buf = cv2.add(buf, noise, dtype=cv2.CV_8UC3)
        return True, buf

    def isOpened(self):
        return True

class Book(VideoSynthBase):
    def __init__(self, **kw):
        super(Book, self).__init__(**kw)
        backGr = cv2.imread('../data/graf1.png')
        fgr = cv2.imread('../data/box.png')
        self.render = TestSceneRender(backGr, fgr, speed = 1)

    def read(self, dst=None):
        noise = np.zeros(self.render.sceneBg.shape, np.int8)
        cv2.randn(noise, np.zeros(3), np.ones(3)*255*self.noise)

        return True, cv2.add(self.render.getNextFrame(), noise, dtype=cv2.CV_8UC3)

class Cube(VideoSynthBase):
    def __init__(self, **kw):
        super(Cube, self).__init__(**kw)
        self.render = TestSceneRender(cv2.imread('../data/pca_test1.jpg'), deformation = True,  speed = 1)

    def read(self, dst=None):
        noise = np.zeros(self.render.sceneBg.shape, np.int8)
        cv2.randn(noise, np.zeros(3), np.ones(3)*255*self.noise)

        return True, cv2.add(self.render.getNextFrame(), noise, dtype=cv2.CV_8UC3)



classes = dict(book=Book, cube=Cube)

presets = dict(
    empty = 'synth:',
    lena = 'synth:bg=../data/lena.jpg:noise=0.1',
    chess = 'synth:class=chess:bg=../data/lena.jpg:noise=0.1:size=640x480',
    book = 'synth:class=book:bg=../data/graf1.png:noise=0.1:size=640x480',
    cube = 'synth:class=cube:bg=../data/pca_test1.jpg:noise=0.0:size=640x480'
)


def create_capture(source = 0, fallback = presets['chess']):
    '''source: <int> or '<int>|<filename>|synth [:<param_name>=<value> [:...]]'
    '''
    source = str(source).strip()
    chunks = source.split(':')
    # handle drive letter ('c:', ...)
    if len(chunks) > 1 and len(chunks[0]) == 1 and chunks[0].isalpha():
        chunks[1] = chunks[0] + ':' + chunks[1]
        del chunks[0]

    source = chunks[0]
    try: source = int(source)
    except ValueError: pass
    params = dict( s.split('=') for s in chunks[1:] )

    cap = None
    if source == 'synth':
        Class = classes.get(params.get('class', None), VideoSynthBase)
        try: cap = Class(**params)
        except: pass
    else:
        cap = cv2.VideoCapture(source)
        if 'size' in params:
            w, h = map(int, params['size'].split('x'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
        if fallback is not None:
            return create_capture(fallback, None)
    return cap

if __name__ == '__main__':
    import sys
    import getopt

    print(__doc__)

    args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
    args = dict(args)
    shotdir = args.get('--shotdir', '.')
    if len(sources) == 0:
        sources = [ 0 ]

    caps = list(map(create_capture, sources))
    shot_idx = 0
    while True:
        imgs = []
        for i, cap in enumerate(caps):
            ret, img = cap.read()
            imgs.append(img)
            cv2.imshow('capture %d' % i, img)
        ch = cv2.waitKey(1)
        if ch == 27:
            break
        if ch == ord(' '):
            for i, img in enumerate(imgs):
                fn = '%s/shot_%d_%03d.bmp' % (shotdir, i, shot_idx)
                cv2.imwrite(fn, img)
                print(fn, 'saved')
            shot_idx += 1
    cv2.destroyAllWindows()
