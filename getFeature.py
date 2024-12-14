import argparse
from utils.detection_helper import get_features


def get_args_parser():
    parser = argparse.ArgumentParser('Run get_features function with command line arguments.', add_help=False)
    parser.add_argument("--source", default='resources/example',
                        help="Directory containing the input data files.")
    parser.add_argument("--polarity", default='positive',
                        choices=["positive", "negative"],
                        help="Polarity of the MS data (Positive or Negative).")
    parser.add_argument("--ppm", type=int, default=10, help="MS1 ppm tolerance.")
    parser.add_argument("--minWidth", type=int, default=5,
                        help="Min peak width. Default is 5.")
    parser.add_argument("--maxWidth", type=int, default=50,
                        help="Max peak width. Default is 50.")
    parser.add_argument("--s2n", type=int, default=5, help="Signal-to-noise ratio threshold. Default is 5.")
    parser.add_argument("--noise", type=int, default=100, help="Noise threshold. Default is 100.")
    parser.add_argument("--mzDiff", type=float, default=0.015, help="m/z difference threshold. Default is 0.015.")
    parser.add_argument("--prefilter", type=int, default=3, help="Prefilter threshold. Default is 3.")
    return parser


def main(args):

    get_features(
        args.source,
        args.polarity,
        args.ppm,
        args.minWidth,
        args.maxWidth,
        args.s2n,
        args.noise,
        args.mzDiff,
        args.prefilter
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Search ROIs', parents=[get_args_parser()], add_help=False)

    args = parser.parse_args()
    main(args)