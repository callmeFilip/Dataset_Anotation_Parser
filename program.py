import os
import sys
from enum import IntEnum

dirname = os.path.dirname(__file__)
try:
    filename = os.path.join(dirname, str(sys.argv[1]))
except IndexError:
    raise SystemExit((f"Usage: {sys.argv[0]} <filename>"))

base_file = open(filename, 'r')

precision = 7  # round(n, precison)
filename_extension = '.txt'


class Image_parameters_enum(IntEnum):
    width = 0
    height = 1
    x_top = 2
    y_top = 3
    x_bot = 4
    y_bot = 5
    class_t = 6


image_parameter = [0.0] * 7


def rescale_coordinates(coord_max, coord_curr):
    print(round(coord_curr/coord_max, precision))
    return round(coord_curr/coord_max, precision)


# iterate trough base_file
count = 0

while True:
    count += 1
    line = base_file.readline()
    if not line:
        break

    # extract path_name
    element_index = line.find(";")
    path_name = line[0: element_index - 4]  # remove filename extension
    path_name += filename_extension

    # extract numeric values
    for index in Image_parameters_enum:
        previous_element_index = element_index
        element_index = line.find(";", previous_element_index + 1)

        image_parameter[index] = float(
            line[previous_element_index + 1: element_index])

    image_parameter[Image_parameters_enum.class_t] = int(
        image_parameter[Image_parameters_enum.class_t])

    # rescale coordinates from 0 x (height/width) to 0 x 1
    image_parameter[Image_parameters_enum.x_top] = rescale_coordinates(
        image_parameter[Image_parameters_enum.width], image_parameter[Image_parameters_enum.x_top])

    image_parameter[Image_parameters_enum.y_top] = rescale_coordinates(
        image_parameter[Image_parameters_enum.height], image_parameter[Image_parameters_enum.y_top])

    image_parameter[Image_parameters_enum.x_bot] = rescale_coordinates(
        image_parameter[Image_parameters_enum.width], image_parameter[Image_parameters_enum.x_bot])

    image_parameter[Image_parameters_enum.y_bot] = rescale_coordinates(
        image_parameter[Image_parameters_enum.height], image_parameter[Image_parameters_enum.y_bot])

    output_file = open('Result/' + path_name, "w")
    output_file.write(str(image_parameter[Image_parameters_enum.class_t]) +
                      ' ' + str(image_parameter[Image_parameters_enum.x_top]) +
                      ' ' + str(image_parameter[Image_parameters_enum.y_top]) +
                      ' ' + str(image_parameter[Image_parameters_enum.x_bot]) +
                      ' ' + str(image_parameter[Image_parameters_enum.y_bot]))
    output_file.close()

base_file.close()
