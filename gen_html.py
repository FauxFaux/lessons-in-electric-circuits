#!/usr/bin/env python3

import subprocess

import sys

HEAD = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> 
<html> 

<head>

<title>Lessons In Electric Circuits -- Volume {} - Chapter {}</title>
  <meta name="description" content="Ohm's Law">
  <meta name="keywords" content="book, ebook, textbook, tutorial, copyleft, copylefted,
  free, educational, free book, free ebook, free textbook, free download, copyleft book,
  copylefted book, electricity, electronics, electric circuit, spice, spice2g6,
  design science license, kuphaldt, tony kuphaldt, voltage, current, resistance, volt, ampere,
  ohm, power, watt, ohm's law, joule's law, resistor, varistor, negative resistance, polarity,
  voltage drop, spice, spice2g6, spice tutorial, using spice"> 
</head>

<body>

<body bgColor=white>

{}
<a href="index.html"><img src="contents.jpg alt="Contents"></a>
{}

<h1>Lessons In Electric Circuits -- Volume {}</h1>
<h1>Chapter {}</h1>
"""


def main():
    inp = sys.argv[1]
    output = sys.argv[2]

    raw_html = subprocess.check_output(['sed', '-f', 'bin/sml2html.sed', inp])

    with open(output, 'wb') as f:
        f.write(raw_html)


if __name__ == '__main__':
    main()
