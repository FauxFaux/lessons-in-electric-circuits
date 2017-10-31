#!/usr/bin/env python3
import os
import os.path
import re
import sys
from typing import Iterable, Tuple, Iterator

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


def available_images():
    images = set()

    for volume in volumes():
        for file in os.listdir("{}/images".format(volume)):
            root = os.path.splitext(file)[0]
            name = (volume, root)

            if name in images:
                raise Exception("duplicate image: {}".format(name))

            images.add(name)

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


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.rule('gen', ['./gen.py'])
    n.build('build.ninja', 'gen', './gen.py', variables={'generator': 1})

    av = available_images()
    req = set(required_images())

    if not av.issuperset(req):
        print('Some images not available:')
        for img in req:
            if img not in av:
                print(' * ' + img)
        sys.exit(2)

    if av != req:
        print('Some images not used:')
        for img in sorted(av - req):
            print(img)

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if __name__ == '__main__':
    main()
