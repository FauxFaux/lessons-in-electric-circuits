#!/usr/bin/env python3

import argparse

import subprocess
import tempfile

import time

HEAD = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> 
<html> 

<head>

<title>Lessons In Electric Circuits -- Volume {0} - Chapter {1}</title>
  <meta name="description" content="Ohm's Law">
  <meta name="keywords" content="book, ebook, textbook, tutorial, copyleft, copylefted,
  free, educational, free book, free ebook, free textbook, free download, copyleft book,
  copylefted book, electricity, electronics, electric circuit, spice, spice2g6,
  design science license, kuphaldt, tony kuphaldt, voltage, current, resistance, volt, ampere,
  ohm, power, watt, ohm's law, joule's law, resistor, varistor, negative resistance, polarity,
  voltage drop, spice, spice2g6, spice tutorial, using spice"> 
</head>

<body bgColor=white>

{2}

<h1>Lessons In Electric Circuits -- Volume {0}</h1>
<h1>Chapter {1}</h1>
"""

LINKS = """
{}
<a href="index.html"><img src="../shared/contents.png" alt="Contents"></a>
{}
"""

FOOT = """
<hr>

<p>
<i>Lessons In Electric Circuits</i> copyright (C) 2000-2017 Tony R. Kuphaldt,
under the terms and conditions of the <a href="{}_A3.html">Design Science License</a>.
</p>

{}

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', nargs=1, required=True)
    parser.add_argument('--out', nargs=1, required=True)
    parser.add_argument('--prev', nargs=1)
    parser.add_argument('--next', nargs=1)
    parser.add_argument('--volume', nargs=1, required=True)
    parser.add_argument('--chapter', nargs=1, required=True)
    args = parser.parse_args()

    inp = args.src[0]
    output = args.out[0]
    volume = args.volume[0]
    chapter = args.chapter[0]

    raw_html = subprocess.check_output(['sed', '-f', 'bin/sml2html.sed', inp]).decode('utf-8')

    prev = ''
    next = ''

    if args.prev:
        prev = '<a href="{}"><img src="../shared/previous.png" alt="Previous"/></a>'.format(args.prev[0])

    if args.next:
        next = '<a href="{}"><img src="../shared/next.png" alt="Next"/></a>'.format(args.next[0])

    links = LINKS.format(prev, next)

    with tempfile.NamedTemporaryFile(mode='w') as t:
        t.write(HEAD.format(
            volume,
            chapter,
            links
        ))
        t.write(raw_html)
        t.write(FOOT.format(volume, links))
        t.flush()

        ret = subprocess.call(['tidy', '-indent', '-clean', '-q', '-output', output, t.name])

        # 1: warnings. Sigh.
        assert ret in (0, 1)

if __name__ == '__main__':
    main()
