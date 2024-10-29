import argparse
from pathlib import Path
from utils import build_eic
from utils.io_utils import get_files, read_targeted_features, export_results
from utils.predict_utils import build_predictor
from utils.quantify import quantify
from utils.postprocess import post_process
import pickle


def get_args_parser():
    parser = argparse.ArgumentParser('Set PeakFormer', add_help=False)

    parser.add_argument('--type', default='mzML', help='type of raw data files')

    parser.add_argument('--ppm', default=10, help='ppm for EIC extraction')

    parser.add_argument('--source', default='/Users/justzzya/TOF',
                        help='path to raw data directory')

    parser.add_argument('--feature',
                        default='data/FeatureTOF.csv',
                        help='path to feature file')

    parser.add_argument('--images_path', default='data/output',
                        help='path to output eic files')

    parser.add_argument('--output',
                        default='data/output/area.csv',
                        help='path to output files')

    parser.add_argument('--eic_plot',
                        default='True',
                        help='plot EICs or not, first use must be True')

    parser.add_argument('--plot',
                        default='False',
                        help='plot predictions or not')

    # model
    parser.add_argument('--model',
                        default='resources/weight.pth',
                        help='path to peak detection model')

    # parameters
    parser.add_argument('--num_classes', default=1, help='num of classes')

    parser.add_argument('--smooth_sigma', default=0, help='sigma for smoothing')

    parser.add_argument('--processes_number', default=8, help='number of processes')

    return parser


def main(args):

    # data import
    paths = get_files(args.source, args.type)
    # targeted samples
    if args.feature:
        xic_info = read_targeted_features(args.feature)

    # EIC build

    xic_list = build_eic(paths, xic_info, args.eic_plot, args)

    # with open('cancer_xic_list.pkl', 'wb') as f:
    #     pickle.dump(xic_list, f)
    #
    # with open('cancer_xic_list.pkl', 'rb') as f:
    #     xic_list_load = pickle.load(f)
    #
    # #  peak detection
    # results = build_predictor(args.model, args.images_path, plot=args.plot)
    #
    # # quantification
    # area = quantify(xic_list_load, results, xic_info)
    #
    # # export
    # export_results(area, args.output)
    #
    # # post process
    # post_process(args.output, args.feature)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Set PeakFormer', parents=[get_args_parser()])
    args = parser.parse_args()
    if args.images_path:
        Path(args.images_path).mkdir(parents=True, exist_ok=True)
    main(args)






