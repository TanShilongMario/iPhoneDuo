#!/usr/bin/env python3
"""Compose an opaque native-window crop over its sampled original background.
Requires Pillow; does not capture UI, remove backgrounds, or redraw screen content.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

def numbers(value, count):
    try:
        values = tuple(int(part.strip()) for part in value.split(','))
    except ValueError as error:
        raise argparse.ArgumentTypeError('use comma-separated integers') from error
    if len(values) != count:
        raise argparse.ArgumentTypeError(f'expected {count} integers')
    return values

def rect(value):
    return numbers(value, 4)

def pair(value):
    return numbers(value, 2)

def inside(box, size):
    l, t, r, b = box
    return 0 <= l < r <= size[0] and 0 <= t < b <= size[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--crop', type=rect, required=True, metavar='L,T,R,B')
    parser.add_argument('--sample', type=pair, required=True, metavar='X,Y')
    parser.add_argument('--canvas', type=pair, required=True, metavar='WIDTH,HEIGHT')
    parser.add_argument('--image-box', type=rect, required=True, metavar='L,T,R,B')
    parser.add_argument('--force', action='store_true', help='replace output and its JSON sidecar')
    args = parser.parse_args()
    sidecar = args.output.with_suffix('.json')
    if args.output.suffix.lower() != '.png':
        parser.error('output must use .png')
    if args.source.resolve() in {args.output.resolve(), sidecar.resolve()}:
        parser.error('output must not overwrite source')
    if not args.force and (args.output.exists() or sidecar.exists()):
        parser.error('output/sidecar exists; choose another filename or explicitly use --force')
    source = Image.open(args.source)
    if 'A' in source.getbands() and source.getchannel('A').getextrema() != (255,255):
        parser.error('source must be opaque; supply the original window capture, not an alpha cutout')
    source = source.convert('RGB')
    if not inside(args.crop, source.size) or not inside(args.image_box, args.canvas):
        parser.error('crop and image-box must fit their source/canvas and have positive area')
    sx, sy = args.sample
    if not (0 <= sx < source.width and 0 <= sy < source.height):
        parser.error('background sample must be inside the source image')
    background = source.getpixel(args.sample)
    crop = source.crop(args.crop)
    l,t,r,b = args.image_box
    scale = min((r-l)/crop.width, (b-t)/crop.height)
    size = (max(1,round(crop.width*scale)), max(1,round(crop.height*scale)))
    origin = (l+(r-l-size[0])//2, t+(b-t-size[1])//2)
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', args.canvas, background)
    canvas.paste(resized, origin)
    # Keep enough original matte around the body to avoid cutting antialiasing.
    edges = [crop.crop((0,0,crop.width,1)), crop.crop((0,crop.height-1,crop.width,crop.height)),
             crop.crop((0,0,1,crop.height)), crop.crop((crop.width-1,0,crop.width,crop.height))]
    border_delta = max(max(abs(channel-bg) for channel,bg in zip(pixel,background))
                       for edge in edges for pixel in edge.getdata())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output, optimize=True)
    report = dict(source=str(args.source), sourceSHA256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  sourceSize=list(source.size), crop=list(args.crop), sample=list(args.sample),
                  backgroundRGB=list(background), canvas=list(args.canvas), imageSize=list(size),
                  imageOrigin=list(origin), alphaMask=False, borderMaxChannelDelta=border_delta,
                  note='Original opaque crop; proportional resizing only. Inspect borders and actual text visually.')
    sidecar.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Saved {args.output}; RGB background {background}; no alpha mask.')
    if border_delta > 8:
        print('REVIEW: crop border differs from sampled background; check for clipped chassis, chrome, shadows or a nonuniform backdrop.')

if __name__ == '__main__':
    main()
