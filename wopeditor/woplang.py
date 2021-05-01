import argparse
import json
import sys


from texnomagic import lang


def woplang(*cargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('word', nargs='+', help='Words of Power')
    args = parser.parse_args(cargs)
    txlang = lang.TexnoMagicLanguage()
    text = " ".join(args.word)
    out = txlang.parse(text)
    try:
        print(json.dumps(out, indent=4, sort_keys=False))
    except TypeError:
        print(out)
    return 0


def main():
    cargs = sys.argv[1:]
    sys.exit(woplang(*cargs))


if __name__ == '__main__':
    main()
