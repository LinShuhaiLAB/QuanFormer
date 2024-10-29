import argparse
from pathlib import Path
from utils import build_roi
from utils.detection_helper import get_targeted_features
from utils.io_utils import get_files, read_targeted_features, export_results
from utils.predict_utils import build_predictor
from utils.quantify import quantify
from utils.postprocess import post_process
import pickle


def get_args_parser():
    parser = argparse.ArgumentParser('Set QuanFormer', add_help=False)

    parser.add_argument('--type', default='mzML', help='type of raw data files')

    parser.add_argument('--ppm', default=10, help='ppm for EIC extraction')

    parser.add_argument('--source', default='resources/example/mzML',
                        help='path to raw data directory')

    # targeted features
    parser.add_argument('--feature',
                        default="resources/example/faeture.csv",
                        help='path to feature file')

    # CentWave for untargeted features
    parser.add_argument('--polarity', default='negative', help='polarity')

    parser.add_argument('--peakWidth', default=(5, 50), help='peak width')

    parser.add_argument('--s2n', default=5, help='signal to noise')

    parser.add_argument('--noise', default=100, help='noise level')

    parser.add_argument('--mzDiff', default=0.005, help='mz difference')

    parser.add_argument('--prefilter', default=3, help='pre-filtering')


    # prediction
    parser.add_argument('--images_path', default="resources/example/output",
                        help='path to output eic files')

    parser.add_argument('--output',
                        default="resources/example/output/area.csv",
                        help='path to output files')

    parser.add_argument('--eic_plot',
                        default=True,
                        help='plot EICs or not, first use must be True')

    parser.add_argument('--plot',
                        default=True,
                        help='plot predictions or not')

    # model
    parser.add_argument('--model',
                        default=r"checkpoint0029.pth",
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
        xic_info = get_targeted_features(args.source, args.polarity, args.ppm, args.peakWidth,
                                         args.s2n, args.noise, args.mzDiff, args.prefilter)

    # EIC build

    xic_list = build_roi(paths, xic_info, args.eic_plot, args)
    import pickle
    with open('xic_list.pkl', 'wb') as f:
        pickle.dump(xic_list, f)

    #  peak detection
    results = build_predictor(args.model, args.images_path, plot=args.plot)

    xic_list_load = pickle.load(open('xic_list.pkl', 'rb'))
    # quantification
    area = quantify(xic_list_load, results, xic_info)

    # export
    export_results(area, args.output)

    # post process
    post_process(args.output, args.feature)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Set QuanFormer', parents=[get_args_parser()])
    args = parser.parse_args()
    if args.images_path:
        Path(args.images_path).mkdir(parents=True, exist_ok=True)
    main(args)






