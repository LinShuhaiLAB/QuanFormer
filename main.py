import argparse
from pathlib import Path
from utils import build_roi
from utils.detection_helper import get_features
from utils.io_utils import get_files, read_targeted_features, export_results
from utils.predict_utils import build_predictor
from utils.quantify import quantify
from utils.postprocess import post_process


def get_args_parser():
    parser = argparse.ArgumentParser('Set QuanFormer', add_help=False)

    parser.add_argument('--type', default='mzML', help='type of raw data files')

    parser.add_argument('--ppm', default=10, help='ppm for ROI extraction')

    parser.add_argument('--source', default='resources/example',
                        help='path to raw data directory')

    # targeted features
    parser.add_argument('--feature',
                        # default="resources/test_feature.csv",
                        help='path to feature file')

    # CentWave for untargeted features, only set when using untargeted mode.
    parser.add_argument('--polarity', default='negative', choices=["positive", "negative"],
                        help='polarity')

    parser.add_argument('--minWidth', default=5, help='min peak width')

    parser.add_argument('--maxWidth', default=50, help='max peak width')

    parser.add_argument('--s2n', default=5, help='signal to noise')

    parser.add_argument('--noise', default=100, help='noise level')

    parser.add_argument('--mzDiff', default=0.005, help='mz difference')

    parser.add_argument('--prefilter', default=3, help='pre-filtering')

    # prediction
    parser.add_argument('--images_path', default="resources/example/output",
                        help='path to output roi files')

    parser.add_argument('--output',
                        default="resources/example/output/area.csv",
                        help='path to output files')

    parser.add_argument('--threshold', default=0.99,
                        help='keep only predictions with 0.99 confidence')

    parser.add_argument('--roi_plot',
                        default=True,
                        help='plot ROIs or not, first use must be True')

    parser.add_argument('--plot',
                        default=True,
                        help='plot predictions or not')

    # model
    parser.add_argument('--model',
                        default='resources/checkpoint0029.pth',
                        help='path to peak detection model')

    # parameters
    parser.add_argument('--num_classes', default=1, help='num of classes')

    parser.add_argument('--smooth_sigma', default=0, help='sigma for smoothing')

    parser.add_argument('--processes_number', default=1, help='number of processes')

    return parser


def main(args):

    # data import
    paths = get_files(args.source, args.type)
    # targeted samples
    if args.feature:
        xic_info = read_targeted_features(args.feature)
    # untargeted samples
    else:
        xic_info = get_features(args.source, args.polarity, args.ppm, args.minWidth, args.maxWidth,
                                         args.s2n, args.noise, args.mzDiff, args.prefilter)

    # ROI build
    xic_list = build_roi(paths, xic_info, args.roi_plot, args)

    #  peak detection
    results = build_predictor(args.model, args.images_path, args.threshold, plot=args.plot)

    # quantification
    area = quantify(xic_list, results, xic_info)

    # export
    export_results(area, args.output)

    # post process
    post_process(args.output, xic_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Set QuanFormer', parents=[get_args_parser()])
    args = parser.parse_args()
    if args.images_path:
        Path(args.images_path).mkdir(parents=True, exist_ok=True)
    main(args)






