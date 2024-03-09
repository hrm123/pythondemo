import os
import sys
import shutil
import uuid
import subprocess
import urllib.request
import math
import random


class Point(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be iterable')

    def __str__(self):
        return 'Vector:{}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


point1 = Point([1, 2, 3])
print(point1)