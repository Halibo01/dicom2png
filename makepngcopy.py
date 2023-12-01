import os
import sys
import pydicom as pdm
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np
from tqdm import tqdm
import argparse
import cv2 as cv
import shutil
import warnings
warnings.filterwarnings("ignore")

bitvalues = [8, 16, 24]

def makepng2(image_dir, bit):
    n = np.uint8
    if bit == 16:
        n = np.uint16
    rgb = False
    if bit == 24:
        rgb = True
        bit = 8
    dicom = pdm.read_file(image_dir)
    data = apply_voi_lut(dicom.pixel_array, dicom)
    if dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * ((2**bit) - 1)).astype(n)
    if rgb:
        data = cv.cvtColor(data, cv.COLOR_GRAY2RGB)
    return data


def dir_scan(path:str) -> str:
    for i in os.scandir(path):
        if i.is_file():
            yield i.path
        elif i.is_dir():
            yield i.path
            yield from dir_scan(i.path)

def trueorfalse(string):
    if string.strip().lower() == "y" or string.strip().lower() == "yes" or string.strip().lower() == "ye":
        return True
    else:
        print("Abort")
        return False
    
def createfile(directory:str) -> str:
    newdir = directory
    if os.path.exists(directory):
        k = 2
        while True:
            if os.path.exists(directory + "_" + str(k)):
                k += 1
                continue
            newdir = directory + "_" + str(k)
            break
        print("Storing files in \"" + newdir + "\"")
    os.makedirs(newdir)
    return newdir

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--workingdir", metavar="dir", required=True, type=str, default=None, help="Directory that you want to work with")
    parser.add_argument("-D", "--destinationdir", metavar="dir", required=True, type=str, default=None, help="Destination that you want to copy all files")
    parser.add_argument("-R", "--resize", metavar="x y", required=False, type=int, nargs=2, help="Resizing to desired size")
    parser.add_argument("-B", "--bit", type=int, default=24, help="Bit of the image. you can write 8, 16 or 24. 8 is 8 bit grayscale\n16 is 16 bit grayscale\n24 is 24 bit rgb image. Default: 24", choices=bitvalues)
    parser.add_argument("-y", action="store_true",help="Directly do the process without asking something")
    args = parser.parse_args(sys.argv[1:])
    count = 0
    Y = args.y
    resizeit = False
    if args.resize != None:
        resizeit = True
        shape = (args.resize[0], args.resize[1])
    workdir = args.workingdir
    destdir = args.destinationdir
    bit = args.bit

    if os.path.isfile(workdir):
        print("Workingdir that you entered is a file. Please write a directory that dicom files inside for a proper task.")
        os._exit(3)
    elif not os.path.exists(workdir):
        print("Folder that you want to work is not exists. Abort")
        os._exit(3)
    elif os.listdir(workdir) == []:
        print("Folder that you want to work is empty. Abort")
        os._exit(2)
    if (not os.path.exists(destdir) and os.path.exists(os.path.dirname(destdir))) and not Y:
        print("Destination folder is not exists do you want to create a new file? [N/Y]: ", end="")
        q = input()
        if trueorfalse(q):
            destdir = createfile(destdir)
            os.makedirs(destdir)
        else:
            os._exit(130)
    elif (not os.path.exists(destdir) and os.path.exists(os.path.dirname(destdir))) and Y:
        print("Creating file...")
        os.makedirs(destdir)
    elif os.listdir(destdir) != [] and not Y:
        print("Destination folder is not empty do you want to create another file for not to lose any data? [N/Y]: ", end="")
        q = input()
        if trueorfalse(q):
            destdir = createfile(destdir)
        else:
            os._exit(130)
    elif os.listdir(destdir) != [] and Y:
        print("Creating another file...")
        destdir = createfile(destdir)
    try:
        for i in dir_scan(workdir):
            count += 1
        for i in tqdm(dir_scan(workdir), total=count):
            dir = i.replace(workdir, destdir)
            if os.path.isdir(i):
                os.makedirs(dir, exist_ok=True)
            else:
                if i.endswith(".dicom"):
                    dir = dir[:-5] + "png"
                    image = makepng2(i, bit)
                    if resizeit:
                        image = cv.resize(image, shape, interpolation=cv.INTER_AREA)
                    cv.imwrite(dir, image)
                else:
                    shutil.copy2(i, dir)
    except KeyboardInterrupt:
        print("Interrupted... Abort.")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
