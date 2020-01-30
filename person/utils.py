
from rest_framework.serializers import ValidationError
from rest_framework import status


import numpy as np
from PIL import Image


class CustomAPIException(ValidationError):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def get_string_vector(image):
    im = Image.open(image) #reopen after verify
    im = im.resize((300,300))
    normalaized_arr = np.array(im).flatten() / 255
    string_vector = ','.join([arr_el for arr_el in normalaized_arr.astype(str)])
    return string_vector

def compare_vector(vector1, vector2):
    arr1 = np.fromstring(vector1, sep=',')
    arr2 = np.fromstring(vector2, sep=',')
    result = np.linalg.norm(arr1 - arr2)
    return result




