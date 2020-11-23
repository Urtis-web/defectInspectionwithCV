import os
import glob
import cv2
import numpy as np
import math

# self-explanatory method
def GatherImagesFromDirectory(directory):
    # define supproted types
    types = ['*.png', '*.bmp', '*.jpg']
    # define image list
    imageList = []
    # check if directory exist
    if not os.path.exists(directory):
        print('Directory doesn\'t exist, return empty image path array')
        return imageList #exit method here
    # gather images by types
    for type in types:
        print('Gathering type: ' + type)
        specificTypeImages = glob.glob(directory + type)
        # add one type images list to main array
        imageList.extend(specificTypeImages)
    imageList.sort()
    return imageList

def GetFileName(path):
    name_with_extension = os.path.basename(path)
    name = os.path.splitext(name_with_extension)[0]
    return name

def CreateDirectory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Directory ", directory, " Created ")
    else:
        print("Directory ", directory, " already exists")


def GetLabel(labels_txt_path, image_name):
    labels_txt = open(labels_txt_path, "r")
    lines = labels_txt.readlines()
    for line in lines:
        words = line.split()
        name = words[0]
        if image_name == name:
            major_axis = float(words[1])
            minor_axis = float(words[2])
            rotation = float(words[3]) #rad
            center_x = float(words[4])
            center_y = float(words[5])
            labels_txt.close()
            return major_axis, minor_axis, rotation, center_x, center_y
    labels_txt.close()
    return 0.0,0.0,0.0,0.0,0.0

def positives():
    path_to_positive = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Class6_def/"
    positive_labels_output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Class6_def_label/"
    positive_labels_txt = path_to_positive + 'labels.txt'
    CreateDirectory(positive_labels_output_dir)
    # Positives
    # collect all image from directory
    positive_image_paths = GatherImagesFromDirectory(path_to_positive)
    for positive_image_path in positive_image_paths:
        image = cv2.imread(positive_image_path, cv2.IMREAD_GRAYSCALE)
        # get image dimensions
        height, width = image.shape[:2]
        label = np.zeros((height, width), np.uint8)
        file_name = GetFileName(positive_image_path)
        major_axis, minor_axis, rotation, center_x, center_y = GetLabel(positive_labels_txt, file_name)
        rotation_degrees = (rotation * 180.0 / math.pi)
        cv2.ellipse(label, (int(center_x), int(center_y)), (int(major_axis), int(minor_axis)), rotation_degrees, 0,
                    360, 255, -1)
        cv2.imshow('image', image)
        cv2.imshow('label', label)
        cv2.imwrite(positive_labels_output_dir + file_name + '.png', label)
        cv2.waitKey(1)

def negatives():
    # Negative
    path_to_negative = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Class6/"
    negative_labels_output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Class6_label/"
    CreateDirectory(negative_labels_output_dir)
    # collect all image from directory
    negative_image_paths = GatherImagesFromDirectory(path_to_negative)
    for negative_image_path in negative_image_paths:
        image = cv2.imread(negative_image_path, cv2.IMREAD_GRAYSCALE)
        # get image dimensions
        height, width = image.shape[:2]
        label = np.zeros((height, width), np.uint8)
        file_name = GetFileName(negative_image_path)
        cv2.imshow('image', image)
        cv2.imshow('label', label)
        cv2.imwrite(negative_labels_output_dir + file_name + '.png', label)
        cv2.waitKey(1)

def Sobel():
    # fh = open(r"C:\Users\Urtis\PycharmProjects\Darbai_su_vaizdu\corsera\{}".format(fname1))
    fname1 = input("Enter file name, where to take pictures from: ")
    path_to_photos = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname1)
    if not os.path.exists(path_to_photos):
        print('Directory doesn\'t exist,')
        return print("uzluzimas")


    fname2 = input("Enter file name, where to put pictures with Sobel filter to: ")
    positive_sobel_output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname2)
    CreateDirectory(positive_sobel_output_dir)
    try:
        image_paths = GatherImagesFromDirectory(path_to_photos)
    except:
        print("pukst")


    label1 = "Y"
    label2 = "X"
    for image_path in image_paths:
        file_name = GetFileName(image_path)

        image = cv2.imread(image_path)

        image_Y = cv2.Sobel(image, cv2.CV_8UC1, 0, 1)
        cv2.imshow("Sobel image", image_Y)
        cv2.imwrite(positive_sobel_output_dir + file_name + '.png', label1)
        cv2.waitKey(10)

        image_X = cv2.Sobel(image, cv2.CV_8UC1, 1, 0)
        cv2.imshow("Sobel image", image_X)
        cv2.imwrite(negative_labels_output_dir + file_name + '.png', label2)
        cv2.waitKey(10)


def main():

    #positives()

    #negatives()
    Sobel()
# what we will start? (entry point)
if __name__ == "__main__":
    main()