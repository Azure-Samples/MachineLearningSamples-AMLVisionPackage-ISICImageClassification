import argparse, os, shutil
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import Button, Label, Scale, Tk, HORIZONTAL

####################################
# Description
# This script creates a UI which can be used for annotating images. Given a directory of images, the user can
# navigate through the images, and annotate each image with a label (e.g. dog, cat, etc). This annotation can be done
# either by pressing on the respective button for the label, or by using a hotkey.
#
# This script can be called from the command line. To show a help message run:
#    python annotation_UI.py --help
#
# Example call:
#    python annotation_UI.py C:/images/unlabeled C:/images/labeled dog cat rabbit
#
# where the meaning of the three parameters are:
#    First parameter : directory which contains the images to be annotated.
#    Second parameter: outDir: root directory where the images will be moved to after they were annotated.
#    Third parameter : space-separated list of all possible labels.
#
# After an image was annotated, it is moved from the directory of unlabeled images to a subdirectory in the output
# directory, where the name of the subdirectory equals the name of the label (e.g. outDir/dog).
####################################

####################################
# Parameters (best left unchanged)
####################################
boxWidth = 17
boxHeight = 2
maxImgSize = 800
additionalLabels = ["UNCLEAR", "SKIP"]


####################################
# Helper functions
####################################
def uiCallback(objType, text):
    global uiState
    uiState = (objType, text)

def getTkLabel(text):
    return Label(text=text, width=boxWidth, height=boxHeight, fg="blue")

def getTkButton(text, objType, callbackString):
    return Button(text=text, command=lambda s=callbackString: uiCallback(objType, s),
                  width=boxWidth, height=boxHeight, bg="white")
def imread(imgPath):
    if not os.path.exists(imgPath):
        raise Exception("ERROR: image path does not exist: " + imgPath)
    img = cv2.imread(imgPath)
    if img is None:
        raise Exception("ERROR: cannot load image " + imgPath)
    return img

def imconvertCv2Pil(img):
    return Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

def imconvertCv2Tk(img):
    return ImageTk.PhotoImage(imconvertCv2Pil(img))

def imresize(img, scale, interpolation = cv2.INTER_LINEAR):
    return cv2.resize(img, (0,0), fx=scale, fy=scale, interpolation=interpolation)

def imresizeMaxDim(img, maxDim, interpolation = cv2.INTER_LINEAR):
    scale = 1.0 * maxDim / max(img.shape[:2])
    return imresize(img, scale, interpolation)

def getFilesInDirectory(directory, postfix = ""):
    assert os.path.exists(directory), "Directory {} does not exist.".format(directory)
    fileNames = [s for s in os.listdir(directory) if not os.path.isdir(os.path.join(directory,s))]
    if not postfix or postfix == "":
        return fileNames
    else:
        return [s for s in fileNames if s.lower().endswith(postfix)]

def makeDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


####################################
# Main
####################################
# Parse input arguments
parser = argparse.ArgumentParser(description='Image labeling user interface.')
parser.add_argument("imgDir", help="Input directory which contains the images to be labeled.")
parser.add_argument("outDir", help="Output drectory where the labeled images will be moved or copied to.")
parser.add_argument("labels", nargs = '*', help = 'List of possible labels to be annotated.')
args = parser.parse_args()
imgDir = args.imgDir
outDir = args.outDir
labels = args.labels

# Init
tk = Tk()
labels = np.sort(labels).tolist()
labels += additionalLabels
imgFilenames = getFilesInDirectory(imgDir)
assert len(imgFilenames)>0, "No images found in directory %s." % imgDir
imgLabels = [None] * len(imgFilenames)

# Add next image button, previous image button, and image selection slider
getTkLabel("CONTROLS").grid(column=0)
getTkButton("Next image [->]",     "scrollButton", "NextImage").grid(column=0)
getTkButton("Previous image [<-]", "scrollButton", "PreviousImage").grid(column=0)
tk.bind('<Right>', lambda _: uiCallback("scrollButton", "NextImage"))
tk.bind('<Left>',  lambda _: uiCallback("scrollButton", "PreviousImage"))
slider = Scale(from_=0, to=len(imgFilenames)-1, orient=HORIZONTAL, command = lambda _: uiCallback("slider", ""))
slider.grid(column=0)

# Add label buttons and hotkeys support
getTkLabel("").grid(column=0)
getTkLabel("LABELS").grid(column=0)
labelButtons = {}
for index,label in enumerate(labels):
    b = getTkButton("{} [{}]".format(label,index+1), "labelButton", label)
    b.grid(column = 0)
    labelButtons[label] = b
    tk.bind(index+1, lambda _,s=label: uiCallback("labelButton", s))

# Keep UI open until user closes the window
uiState = None
while True:
    imgIndex = slider.get()
    imgLabel = imgLabels[imgIndex]
    imgFilename = imgFilenames[imgIndex]

    # Update UI
    for b in labelButtons.values():
        b.configure(bg="white")
    if imgLabel in labels:
        labelButtons[imgLabel].configure(bg="green")
    tk.title("Image Label Annotation (image filename: {})".format(imgFilename))

    # Load image from unlabeled directory, or when image was already moved then from its new path
    if imgLabel == None:
        imgPath = os.path.join(imgDir, imgFilename)
    else:
        imgPath = os.path.join(outDir, imgLabel, imgFilename)
    img = imread(imgPath)

    # Show image
    imgTk = imconvertCv2Tk(imresizeMaxDim(img, maxImgSize))
    Label(tk, image=imgTk).grid(row=0, column=1, rowspan=maxImgSize)
    tk.update_idletasks()
    tk.update()

    # Busy-wait until user triggers an event
    uiState = None
    while uiState == None:
        tk.update_idletasks()
        tk.update()

    # Slider was used to scroll to new image
    if uiState[0] == "slider":
        pass

    # Go to next image
    elif uiState == ("scrollButton", "NextImage"):
        slider.set(min(imgIndex + 1, len(imgFilenames)-1))

    # Go to previous image
    elif uiState == ("scrollButton", "PreviousImage"):
        slider.set(max(imgIndex - 1,0))

    # Update annotation and go to next image
    elif uiState[0] == "labelButton":
        newLabel = uiState[1]
        imgLabels[imgIndex] = newLabel

        dstDir = os.path.join(outDir, newLabel)
        makeDirectory(dstDir)
        dstImgPath = os.path.join(dstDir, imgFilename)
        if imgPath != dstImgPath:
            shutil.move(imgPath, dstImgPath)
        slider.set(min(imgIndex + 1, len(imgFilenames) - 1))
        print("Label for image {} set to {}.".format(imgFilename, newLabel))

    else:
        raise Exception("State {} is invalid.".format(uiState))

tk.destroy()
print("DONE.")