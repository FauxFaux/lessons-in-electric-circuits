#!/usr/bin/env python3
import os
import os.path
import re
import sys
from typing import Iterable, Tuple, Iterator, Dict

import ninja_syntax

# for f in *(/); do echo "'$f': ["; egrep -h '^[A-Z]*_[0-9]*\.html' $f/Makefile \
# | sed 's/.* : /'\''/; s/\.sml.*/'\'',/'; done

BOOK = (
    ('DC', [
        'basiccon',
        'ohm',
        'safety',
        'scientif',
        's_and_p',
        'divider',
        's_p',
        'dcmeter',
        'dcsignal',
        'dcnet',
        'batt',
        'conduct',
        'cap',
        'magnet',
        'inductor',
        'time',
    ]),

    ('AC', [
        'basicac',
        'complex',
        'xzl',
        'xzc',
        'xzrlc',
        'resonant',
        'mixed',
        'filters',
        'trans',
        'poly',
        'acpower',
        'acmeter',
        'acmotor',
        'lines',
    ]),

    ('Semi', [
        'amplif',
        'theory',
        'diode',
        'bjt',
        'jfet',
        'mosfet',
        'thyr',
        'opamp',
        'analog',
        'active',
        'dcdrive',
        'acdrive',
        'tubes',
    ]),

    ('Digital', [
        'numbers',
        'binary',
        'gates',
        'switches',
        'relays',
        'ladder',
        'boolean',
        'karnaugh',
        'combin',
        'multivib',
        'counters',
        'shiftreg',
        'a2d',
        'commun',
        'memory',
        'computer',
    ]),

    ('Ref', [
        'equation',
        'colors',
        'citable',
        'algebra',
        'trig',
        'calculus',
        'spice',
        'trouble',
        'symbol',
        'periodic',
    ]),

    ('Exper', [
        'intro',
        'basic',
        'dc',
        'ac',
        'discrete',
        'a_ic',
        'd_ic',
        '555',
    ]),
)

IMAGE = re.compile('<image(?:nf)?>([a-z0-9]+)\.(?:png|jpg|eps|gif)<')


def volumes() -> Iterable[str]:
    return [x[0] for x in BOOK]


def available_images() -> Dict[Tuple[str, str], str]:
    images = dict()

    for volume in volumes():
        for file in os.listdir("{}/images".format(volume)):
            root, fmt = os.path.splitext(file)
            name = (volume, root)

            if name in images:
                raise Exception("duplicate image: {}".format(name))

            images[name] = fmt[1:]

    return images


def image_links(path: str) -> Iterator[Tuple[str, str]]:
    with open(path) as f:
        for line in f:
            ma = IMAGE.search(line)
            if ma:
                yield ma.group(1)


def required_images():
    wanted = set()

    for volume, chapters in BOOK:
        for chapter in chapters:
            for link in image_links('{}/src/{}.sml'.format(volume, chapter)):
                wanted.add((volume, link))

    return wanted


def images(n):
    n.rule('cp', '$cp $in $out')
    n.rule('inkscape', '$inkscape $in --export-plain-svg=$out')
    n.rule('mogrify-png', 'convert -density 160 $in $out')
    n.rule('optipng', 'optipng -clobber -quiet $in -out $out')

    av = available_images()
    req = set(required_images())
    if not set(av.keys()).issuperset(req):
        print('Some images not available:')
        for img in req:
            if img not in av:
                print(' * ' + img)
        sys.exit(2)
    if av != req:
        print('Some images not used:')
        for img in sorted(set(av.keys()) - req):
            print(img)
    for volume, root in sorted(req):
        def dest(new_fmt: str) -> str:
            return '$html/{}/{}.{}'.format(volume, root, new_fmt)

        def tmp(new_fmt: str) -> str:
            return '$tmp/{}/{}.{}'.format(volume, root, new_fmt)

        def tmp_raw(new_fmt: str) -> str:
            return '$tmp/{}/raw-{}.{}'.format(volume, root, new_fmt)

        fmt = av[(volume, root)]
        src = '{}/images/{}.{}'.format(volume, root, fmt)

        if fmt in {'jpg', 'png'}:
            n.build(dest(fmt), 'cp', inputs=[src])
        elif fmt == 'eps':
            # n.build(dest('svg'), 'inkscape', inputs=[src])
            n.build(tmp_raw('png'), 'mogrify-png', inputs=[src])
            n.build(tmp('png'), 'optipng', inputs=[tmp_raw('png')])
            n.build(dest('png'), 'cp', tmp('png'))
        else:
            raise Exception('Unsupported format: ' + fmt)

    for f in ('contents', 'pdf', 'ps', 'src1', 'src2'):
        n.build('$html/shared/{}.png'.format(f), 'mogrify-png', 'shared-images/{}.eps'.format(f))

    for f in ('next', 'previous'):
        n.build('$html/shared/{}.png'.format(f), 'mogrify-png', 'shared-images/{}.svg'.format(f))

def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.variable('outdir', 'build')
    n.variable('html', '$outdir/html')
    n.variable('tmp', '$outdir/tmp')
    n.variable('cp', 'cp')
    n.variable('inkscape', 'inkscape')
    n.variable('tidy', 'tidy')

    n.rule('gen', ['./gen.py'])
    n.build('build.ninja', 'gen', './gen.py', variables={'generator': 1})

    n.rule('tidy', '$tidy -indent -clean -q -output $out $in || [ $$? -ne 2 ]')
    for volume in volumes():
        n.build('$html/{}/index.html'.format(volume), 'tidy', '{}/index.html'.format(volume))

    images(n)

    n.rule('sml2html', ['./gen_html.py', '--src=$in', '--out=$out',
                        '--volume=$volume', '--chapter=$chapter',
                        '--next=$next', '--prev=$prev'])
    for volume, chapters in BOOK:
        for i, chapter in enumerate(chapters):
            if i == 0:
                prev_link = 'index.html'
            else:
                prev_link = '{}_{}.html'.format(volume, i + 1 - 1)

            if i == len(chapters):
                next_link = 'index.html'
            else:
                next_link = '{}_{}.html'.format(volume, i + 1 + 1)

            n.build('$html/{}/{}_{}.html'.format(volume, volume, i + 1),
                    'sml2html',
                    inputs='{}/src/{}.sml'.format(volume, chapter),
                    implicit='gen_html.py',
                    variables={
                        'volume': volume,
                        'chapter': (i + 1),
                        'next': next_link,
                        'prev': prev_link,
                    })

    for f in (
        'index.html',
        'log.html',
        'ac.jpg',
        'dc.jpg',
        'digi.jpg',
        'exp.jpg',
        'gnu.jpg',
        'ref.jpg',
        'semi.jpg',
        'thegimp.png',
        'tux.png',
        'vim1.png',
        'xctitle.png',
    ):
        n.build('$html/' + f, 'cp', 'Home/' + f)

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if __name__ == '__main__':
    main()
