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
        return imageList  # exit method here
    # gather images by types
    for type in types:
        specific_type_images = glob.glob(directory + type)
        # add one type images list to main array
        imageList.extend(specific_type_images)
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
            rotation = float(words[3])  # rad
            center_x = float(words[4])
            center_y = float(words[5])
            labels_txt.close()
            return major_axis, minor_axis, rotation, center_x, center_y
    labels_txt.close()
    return 0.0, 0.0, 0.0, 0.0, 0.0


def Check_what_kind_of_label(labels_txt_path, image_name):  # ivedama txt failo direktorija ir einamos image pavadinimas
    labels_txt = open(labels_txt_path, "r")                 # atidaromas txt failas
    lines = labels_txt.readlines()                          # nuskaitomos failo eilutes
    for line in lines:                                      # iteruojama per eilutes
        words = line.split()                                # eilute splitinama i zodzius
        name = words[0]                                     # name = prilyginamas pirmam eilutes zodziui
        if image_name == name:                              #
            if int(words[1]) == 1:                          # jei eilutes 2 zodis == 1  --True--
                defektuotas = 1                             # priskiriamas atskirimo zodis
                labels_txt.close()                          # uzdaromas txt failas
                return defektuotas                          # funkcija grazina atsakyma
            if int(words[1]) == 0:                          # jei eilutes 2 zodis == 0
                nedefektuotas = 0                           # priskiriamas atskirimo zodis 0   --False--
                labels_txt.close()                          # uzdaromas txt failas
                return nedefektuotas                        # funkcija grazina atsakyma


def Getting_right_file(path, image_name):           # ivedama lable direktorija  ir nurodomas failo pavadinimas
    image_paths = GatherImagesFromDirectory(path)   # nurenkami failai is nurodytos direktorijos
    for image_path in image_paths:                  # iteruojama per surinktus failus
        file_name = GetFileName(image_path)         # gaunamas iteruojamo failo pavadinimas
        if file_name[0:4] == image_name:            # jei pirmos 4 pavadinimo rades sutampa su nurodutu failu
            file = image_path                       # file = priskiriama rastas sutampantis failas
            return file                             # funkcija grazina atsakyma
        else:                                       # visais kitais atvejais
            continue                                # grizti i for cikla ir testi darba


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


def Rototion_and_fliping_and_lable_making():
    ###################### is imputu gaunami kintamieji
    kintamasis1 = input("Enter --Class-- name for augmntation: ")
    kintamasis2 = input("Enter is this gona be --1--Test-- or --2--Train-- data:")

    ###################### nurodomas kelias iki senu --images--
    path_to_photo = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Nauja\DAGM_KaggleUpload\{}".format(
        kintamasis1) + '\{}'.format(kintamasis2) + '//'

    ###################### nurodomas kelias iki senu --lable--
    path_to_labels = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Nauja\DAGM_KaggleUpload\{}".format(
        kintamasis1) + '\{}'.format(kintamasis2) + '\Label/'

    ######################  Sukurimas Class folderio naujoje bazeje
    linkas = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Nauja\Sugeneruota_baze\{}".format(kintamasis1) + '//'
    CreateDirectory(linkas)

    ###################### cia dedami sugeneruoti nauji --images--
    output_image_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Nauja\Sugeneruota_baze\{}".format(
        kintamasis1) + '\{}'.format(kintamasis2) + '/'
    CreateDirectory(output_image_dir)

    ###################### cia dedami sugeneruoti nauji --lable--
    output_labels_dir = r"C:\Users\Urtis\Desktop\Straipsniai\dagm\Nauja\Sugeneruota_baze\{}".format(
        kintamasis1) + '\{}'.format(kintamasis2) + '\Label/'
    CreateDirectory(output_labels_dir)

    ###################### nurodomas txt failiuko tikslus paemimo adresas
    labels_txt = path_to_labels + 'Labels.txt'

    ###################### collect all image from directory
    image_paths = GatherImagesFromDirectory(path_to_photo)
    ###################### reikia pakeisti kai irasoma nauja Class paskutiniu image NR.
    file_name = 128800

    for image_path in image_paths:
        file_name1 = GetFileName(image_path)  # gaunamas iteruojamo imago pavadinimas
        ar_defektuotas = Check_what_kind_of_label(labels_txt, file_name1)  # patikrinama ar image yra su defektu

        if ar_defektuotas == 0:  # jeigu einama image yra be defekto
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)             # nuskaitoma einama grayscale image
            file_name = int(file_name) + 1                                   # Failu pavadinimu skaiciuokle ++
            cv2.imwrite(output_image_dir + str(file_name) + '.png', image)   # irasomas image
            height, width = image.shape[:2]                                  # gaunamos image dimensijos
            label = np.zeros((height, width), np.uint8)                      # sukuriamas lable pagal gautas dimensijas
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label)  # irasomas lable

            new_img1 = cv2.rotate(image, rotateCode=0)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img1)
            height1, width1 = new_img1.shape[:2]
            label1 = np.zeros((height1, width1), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label1)

            new_img2 = cv2.rotate(image, rotateCode=1)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img2)
            height2, width2 = new_img2.shape[:2]
            label2 = np.zeros((height2, width2), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label2)

            new_img3 = cv2.rotate(image, rotateCode=2)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img3)
            height3, width3 = new_img3.shape[:2]
            label3 = np.zeros((height3, width3), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label3)

            new_fliped_img4 = cv2.flip(image, 1)
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_fliped_img4)
            height4, width4 = new_fliped_img4.shape[:2]
            label4 = np.zeros((height4, width4), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label4)

            new_img5 = cv2.rotate(new_fliped_img4, rotateCode=0)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img5)
            height5, width5 = new_img5.shape[:2]
            label5 = np.zeros((height5, width5), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label5)

            new_img6 = cv2.rotate(new_fliped_img4, rotateCode=1)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img6)
            height6, width6 = new_img6.shape[:2]
            label6 = np.zeros((height6, width6), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label6)

            new_img7 = cv2.rotate(new_fliped_img4, rotateCode=2)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img7)
            height7, width7 = new_img7.shape[:2]
            label7 = np.zeros((height7, width7), np.uint8)
            cv2.imwrite(output_labels_dir + str(file_name) + '.png', label7)

        if ar_defektuotas == 1:  # jeigu einama image yra su defektu
            image_d = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)                   # nuskaitoma einama grayscale image
            file_name = int(file_name) + 1                                           # Failu pavadinimu skaiciuokle ++
            cv2.imwrite(output_image_dir + str(file_name) + '.png', image_d)         # irasomas image
            label_d = cv2.imread(Getting_right_file(path_to_labels, file_name1))     # lable = randamas reikiamas failas
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label_d)  # irasomas lable

            new_img1_d = cv2.rotate(image_d, rotateCode=0)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img1_d)
            label1_d = cv2.rotate(label_d, rotateCode=0)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label1_d)

            new_img2_d = cv2.rotate(image_d, rotateCode=1)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img2_d)
            label2_d = cv2.rotate(label_d, rotateCode=1)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label2_d)

            new_img3_d = cv2.rotate(image_d, rotateCode=2)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img3_d)
            label3_d = cv2.rotate(label_d, rotateCode=2)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label3_d)

            new_fliped_img4_d = cv2.flip(image_d, 1)
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_fliped_img4_d)
            label4_d = cv2.flip(label_d, 1)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label4_d)

            new_img5_d = cv2.rotate(image_d, rotateCode=0)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img5_d)
            label5_d = cv2.rotate(label_d, rotateCode=0)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label5_d)

            new_img6_d = cv2.rotate(image_d, rotateCode=1)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img6_d)
            label6_d = cv2.rotate(label_d, rotateCode=1)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label6_d)

            new_img7_d = cv2.rotate(image_d, rotateCode=2)  # 0 = 90 degrees; 1 = 180 degrees; 2 = 270 degrees
            file_name = int(file_name) + 1
            cv2.imwrite(output_image_dir + str(file_name) + '.png', new_img7_d)
            label7_d = cv2.rotate(label_d, rotateCode=2)
            cv2.imwrite(output_labels_dir + str(file_name) + '_label.png', label7_d)


def main():
    Rototion_and_fliping_and_lable_making()


# what we will start? (entry point)
if __name__ == "__main__":
    main()
