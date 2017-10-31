#!/usr/bin/env python3
import os

import ninja_syntax


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.rule('gen', ['./gen.py'])
    n.build('build.ninja', 'gen', './gen.py', variables={'generator': 1})

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if __name__ == '__main__':
    main()
