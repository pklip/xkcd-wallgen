import glob
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", dest="in_path",
                        help="path to folder containg wallpapers")
    args = parser.parse_args()

    for file in glob.glob(os.join(args.in_path, "*.png")):
        print file