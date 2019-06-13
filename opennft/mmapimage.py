# -*- coding: utf-8 -*-

import collections
import numpy as np


def get_image_shape(image_name: str, eng, nargout: int) -> np.ndarray:
    return np.array(eng.evalin('base', 'size({})'.format(image_name), nargout=nargout), dtype=np.int32)


def read_memmap_image(fp, shape, offset: int, dtype: str = 'uint8'):
    return np.memmap(
        fp,
        dtype=dtype,
        mode='r',
        shape=tuple(shape),
        offset=offset,
        order='F'
    )


class ProjectionImagesReader:
    """The class for reading projection images from memmap file
    """

    _projection_images_mapping = collections.OrderedDict([
        ('transversal', 'imgt'),
        ('sagittal', 'imgs'),
        ('coronal', 'imgc'),
    ])

    def __init__(self):
        self._projection_images = {}
        self.clear()

    @property
    def transversal(self) -> np.ndarray:
        """Returns transversal image projection
        """
        return self._projection_images['transversal']

    @property
    def sagittal(self) -> np.ndarray:
        """Returns sagittal image projection
        """
        return self._projection_images['sagittal']

    @property
    def coronal(self) -> np.ndarray:
        """Returns coronal image projection
        """
        return self._projection_images['coronal']

    def read(self, memmap_filename: str, matlab_engine):
        """Reads projection images from memmap file
        """
        with open(memmap_filename, 'r') as fp:
            offset = 0

            for proj_name, image_name in self._projection_images_mapping.items():
                shape = get_image_shape(image_name, matlab_engine, nargout=3)
                self._projection_images[proj_name] = read_memmap_image(fp, shape, offset)
                offset += shape.prod()

    def clear(self):
        """Clean up all data
        """
        self._projection_images = {proj: None for proj in self._projection_images_mapping}