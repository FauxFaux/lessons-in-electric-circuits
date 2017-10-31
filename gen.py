#!/usr/bin/env python3
import os

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


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.rule('gen', ['./gen.py'])
    n.build('build.ninja', 'gen', './gen.py', variables={'generator': 1})

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if __name__ == '__main__':
    main()
