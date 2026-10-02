import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def create_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit", description="Console toolkit: calculator and converter"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help="calculate expression")
    calc_parser.add_argument("expression", help='for example: "2 + 3 * 4"')

    convert_parser = subparsers.add_parser(
        "convert", help="convert value between units"
    )
    convert_parser.add_argument("value", help="number to convert")
    convert_parser.add_argument("--from", dest="from_", required=True, help="from unit")
    convert_parser.add_argument("--to", dest="to_", required=True, help="to unit")

    return parser


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.from_, args.to_)
    except ToolkitError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
