from ANPR import ANPR
import cv2 as cv
import argparse
import os
from imutils import paths
import imutils
dir_path = 'D:/Car_Parking/Images/self_cap_Data/test_Data/data/images/train'


def cleanup_text(text):
    # strip out non ASCII text so we can draw the text on the image
    # using openCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def get_license_plate_text():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    # ap.add_argument("-i", "--input", required=True,
    # 	help="path to input directory of images")
    ap.add_argument("-c", "--clear-border", type=int, default=True,
                    help="whether or to clear border pixels before OCR'ing")
    ap.add_argument("-p", "--psm", type=int, default=7,
                    help="default PSM mode for OCR'ing license plates")
    ap.add_argument("-d", "--debug", type=int, default=-1,
                    help="whether or not to show additional visualizations")
    args = vars(ap.parse_args())
    # initialize our ANPR class
    anpr = ANPR(debug=args["debug"] > 0)
    # grab all image paths in the input directory
    # imagePaths = sorted(list(paths.list_images(args["input"])))
    # loop over all image paths in the input directory
    for imagePath in os.listdir(dir_path):
        # load the input image from disk and resize it
        print(os.path.join(dir_path, imagePath))
        image = cv.imread(os.path.join(dir_path, imagePath))
        image = imutils.resize(image, width=600)
        # apply automatic license plate recognition
        (lpText, lpCnt) = anpr.find_and_ocr(image, psm=args["psm"],
                                            clearBorder=args["clear_border"] > 0)
        # only continue if the license plate was successfully OCR'd
        if lpText is not None and lpCnt is not None:
            # fit a rotated bounding box to the license plate contour and
            # draw the bounding box on the license plate
            box = cv.boxPoints(cv.minAreaRect(lpCnt))
            box = box.astype("int")
            cv.drawContours(image, [box], -1, (0, 255, 0), 2)
            # compute a normal (unrotated) bounding box for the license
            # plate and then draw the OCR'd license plate text on the
            # image
            (x, y, w, h) = cv.boundingRect(lpCnt)
            cv.putText(image, cleanup_text(lpText), (x, y-15),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            # show the output ANPR image
            print("[INFO] {}".format(lpText))
            cv.imshow("Output ANPR", image)
            return lpText
            # cv.waitKey(0)
        else:
            print("License Plate not found")
