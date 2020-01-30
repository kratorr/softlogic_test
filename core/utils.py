import numpy as np


def get_string_vector(im):
    normalaized_arr = np.array(im).flatten() / 255
    string_vector = ','.join([arr_el for arr_el in normalaized_arr.astype(str)])
    return string_vector

def compare_vector(vector1, vector2):
    arr1 = np.fromstring(vector1, sep=',')
    arr2 = np.fromstring(vector2, sep=',')
    result = np.linalg.norm(arr1 - arr2)
    return result