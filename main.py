import argparse
import sys

from pytracert import Tracer


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--hops",
        type=int,
        help="Max value of intermediate nodes",
        default=30
    )

    parser.add_argument(
        "--destination",
        "-d",
        type=str,
        help="Destination domain name"
    )

    args = parser.parse_args(args=argv)
    tracert = Tracer(destination=args.destination, hops=args.hops)
    return tracert.run()


if __name__ == "__main__":
    # without script name
    main(sys.argv[1:])
