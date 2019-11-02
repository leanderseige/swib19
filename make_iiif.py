#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import cv2
import glob
import hashlib
import copy

def buildManifest(manifest,uri,folder):
    manifest['@id'] = uri
    manifest['label'] = folder
    manifest['sequences'][0]['@id'] = uri+"/sequence/1"
    return manifest

def addCanvasToManifest(manifest,canvas,uri,image,ic):
    # set IDs
    canvas['@id'] = uri+"/canvas/%d" % ic
    canvas['images'][0]['@id'] = uri+"/image/%d" % ic
    canvas['images'][0]['resource']['@id'] = uri+"/resource/%d" % ic
    # linke IDs
    canvas['images'][0]['on'] = canvas['@id']
    # set image dimensions
    img = cv2.imread(image)
    height = img.shape[0]
    width = img.shape[1]
    canvas['width'] = width
    canvas['images'][0]['resource']['width'] = width
    canvas['height'] = height
    canvas['images'][0]['resource']['height'] = height
    # set labels
    label = image.split('/')[1].replace('_',' ')
    canvas['label'] = label
    canvas['images'][0]['resource']['label'] = label
    # set service
    canvas['images'][0]['resource']['service']['@id'] = config['baseurl']+"/"+image
    # append canvas to manifest
    manifest['sequences'][0]['canvases'].append(canvas)
    return manifest

with open('config.json', 'r') as f:
    config = json.load(f)

with open('manifest_template.json', 'r') as f:
    manifest_template = json.load(f)

with open('canvas_template.json', 'r') as f:
    canvas_template = json.load(f)

folders = [f for f in glob.glob("imageapi/*")]
for folder in folders:
    manifest = copy.deepcopy(manifest_template)
    id = hashlib.md5(folder.encode()).hexdigest()
    uri = config['baseurl']+"/manifests/"+id+".json"
    manifest = buildManifest(manifest, uri, folder)
    images = [image for image in glob.glob(folder+"/*.tif")]
    ic = 1
    for image in images:
        canvas = copy.deepcopy(canvas_template)
        manifest = addCanvasToManifest(manifest,canvas,uri,image,ic)
        ic = ic +1
    filename = "presentationapi/manifests/"+id+".json"
    print "wite: "+filename
    with open(filename, 'w') as outfile:
        json.dump(manifest, outfile, sort_keys=True, indent=4, separators=(',', ': '))
