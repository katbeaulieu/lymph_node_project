#copied from part1, cisc 881 assignment, normalize intensities, crop images

import SimpleITK as sitk
import sys, os
#import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

nrrdDir = "C:\\Users\\kb48\\Downloads\\LymphNodeProject\\Segmentations\\"


def normalize_intensities():
   
    caster = sitk.CastImageFilter()
    for patient in os.listdir(nrrdDir):
        if patient.endswith(".nrrd"):
            image = sitk.ReadImage(nrrdDir + patient )
            origin = image.GetOrigin()
            direction = image.GetDirection()
            caster.SetOutputPixelType(sitk.sitkFloat64)
            image = caster.Execute(image)	
            norm_image = sitk.RescaleIntensity(image, 0.0, 1.0)
            image.SetOrigin(origin)
            image.SetDirection(direction)
            sitk.WriteImage(norm_image, nrrdDir + "normed_" + patient)

def main():
	normalize_intensities()

main()