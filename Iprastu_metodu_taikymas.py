import os
import glob
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def Uzklausa_is_kur_imti_foto():
    fname = input("Enter file name, where to take pictures from: ")                       # nurodomas inputas
    path_to_photos = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'   # direktorija ikeliama i kintamaji
    if fname == "skip":
        return print("SKIPINAM")
    if not os.path.exists(path_to_photos):                                                 # jeigu ivestas inputas nenurodo esamos direktorijos meta klaida
        print('Directory doesn\'t exist,')                                                 #
        return print("uzluzimas")                                                          #
    return path_to_photos

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

def Sobel_X(path_to_photos):
    fname = input("Enter file name, where to put pictures with Sobel_X filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    positive_sobel_output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) +'//'
    CreateDirectory(positive_sobel_output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image_X = cv2.Sobel(image, cv2.CV_8UC1, 1, 0)
        cv2.imshow("Sobel_X image", image_X)
        cv2.imwrite(positive_sobel_output_dir + file_name + '.png', image_X)
        cv2.waitKey(10)
        cv2.destroyWindow("Sobel_X image")

def Sobel_Y(path_to_photos):
    fname = input("Enter file name, where to put pictures with Sobel_Y filter to: ")               # nurodomas inputas
    if fname == "skip":
        return print("SKIPINAM")
    positive_sobel_output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) +'//'  # direktorija ikeliama i kintamaji
    CreateDirectory(positive_sobel_output_dir)                                                     # sukuriamas folderis jeigu toks neegzistuoja
    image_paths = GatherImagesFromDirectory(path_to_photos)                                        # surenka foto is direktorijos

    for image_path in image_paths:                                            # for ciklas iteruoja per surinktas foto
        file_name = GetFileName(image_path)                                   # pasiimamas failo(foto) pavainimas
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)                  # nuskaitoma nuotrauka ir paverciama grayscale
        image_Y = cv2.Sobel(image, cv2.CV_8UC1, 0, 1)                         # pritaikomas Sobelio filtras Y asimi
        cv2.imshow("Sobel_Y image", image_Y)                                  # parodoma foto su pritaikytu Sobelio filtru
        cv2.imwrite(positive_sobel_output_dir + file_name + '.png', image_Y)  # irasoma foto su pritaikytu Sobelio filtru i nurodyta direktorija, tuo paciu pavadinimu
        cv2.waitKey(10)                                                       # pauze
        cv2.destroyWindow("Sobel_Y image")                                    # uzdaroma foto, kad neuzterstu viewerio

def binary_threshold(path_to_photos):
    fname = input("Enter file name, where to put pictures with binary threshold filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        ret,image_threshold = cv2.threshold(image, 75, 255, cv2.THRESH_BINARY)
        cv2.imshow("binary threshold image", image_threshold)
        cv2.imwrite(output_dir + file_name + '.png', image_threshold)
        cv2.destroyWindow("binary threshold image")
        cv2.waitKey(10)

def binary_inverted_threshold(path_to_photos):
    fname = input("Enter file name, where to put pictures with binary inverted threshold filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        ret,image_threshold = cv2.threshold(image, 75, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("binary inverted threshold image", image_threshold)
        cv2.imwrite(output_dir + file_name + '.png', image_threshold)
        cv2.destroyWindow("binary inverted threshold image")
        cv2.waitKey(10)

def OTSU_threshold(path_to_photos):
    fname = input("Enter file name, where to put pictures with OTSU_threshold filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Otsu's thresholding
        ret2, image_threshold = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow("binary inverted threshold image", image_threshold)
        cv2.imwrite(output_dir + file_name + '.png', image_threshold)
        cv2.destroyWindow("binary inverted threshold image")
        cv2.waitKey(10)

def OTSU_threshold_with_Gaussian_blur(path_to_photos):
    fname = input("Enter file name, where to put pictures with OTSU_threshold_with_Gaussian_blur filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(image, (5, 5), 0)
        ret3, image_threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow("binary inverted threshold image", image_threshold)
        cv2.imwrite(output_dir + file_name + '.png', image_threshold)
        cv2.destroyWindow("binary inverted threshold image")
        cv2.waitKey(10)

def Laplacian(path_to_photos):
    fname = input("Enter file name, where to put pictures with Laplacian filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image_Laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        cv2.imshow("Laplacian image", image_Laplacian)
        cv2.imwrite(output_dir + file_name + '.png', image_Laplacian)
        cv2.destroyWindow("Laplacian image")
        cv2.waitKey(10)

def Find_contours(path_to_photos):
    fname = input("Enter file name, where to put pictures with Find_contours filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Otsu's thresholding after Gaussian filtering
        ret,image_threshold = cv2.threshold(image_gray, 75, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(image_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # create an empty image for contours
        img_contours = np.zeros(image_gray.shape)
        # draw the contours on the empty image
        cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
        # save image
        cv2.imshow("Find_contours", img_contours)
        cv2.imwrite(output_dir + file_name + '.png', img_contours)
        cv2.destroyWindow("Find_contours")
        cv2.waitKey(10)

def Canny_edge_detection_blur(path_to_photos):
    fname = input("Enter file name, where to put pictures with Canny_edge_detection_blur filter to: ")
    if fname == "skip":
        return print("SKIPINAM")
    output_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\{}".format(fname) + '//'
    CreateDirectory(output_dir)
    image_paths = GatherImagesFromDirectory(path_to_photos)

    for image_path in image_paths:
        file_name = GetFileName(image_path)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(image, (5, 5), 0)
        imgCanny = cv2.Canny(blur,50,50)
        cv2.imshow("binary inverted threshold image", imgCanny)
        cv2.imwrite(output_dir + file_name + '.png', imgCanny)
        cv2.destroyWindow("binary inverted threshold image")
        cv2.waitKey(10)

def main():
    path = Uzklausa_is_kur_imti_foto()
    #Sobel_X(path)
    #Sobel_Y(path)
    #binary_threshold(path)
    #binary_inverted_threshold(path)
    #OTSU_threshold(path)
    #OTSU_threshold_with_Gaussian_blur(path)
    #Laplacian(path)
    #Find_contours(path)
    Canny_edge_detection_blur(path)
# what we will start? (entry point)
if __name__ == "__main__":
    main()