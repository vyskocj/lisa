#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
python src/histology_analyser.py -i ~/data/medical/data_orig/jatra_mikro_data/Nejlepsi_rozliseni_nevycistene -t 6800 -cr 0 -1 100 300 100 300

"""



import sys
import os.path
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../extern/dicom2fem/src"))
import logging
logger = logging.getLogger(__name__)

import argparse


import numpy as np
import misc
import datareader
import SimpleITK as sitk
import scipy.ndimage
from PyQt4.QtGui import QApplication

import seed_editor_qt as seqt
import skelet3d
import segmentation


GAUSSIAN_SIGMA = 1


class HistologyAnalyser:
    def __init__ (self, data3d, metadata, threshold):
        self.data3d = data3d
        self.metadata = metadata
        self.threshold = threshold



    def run(self):
        import pdb; pdb.set_trace()
        #self.preprocessing()

        data3d_thr = segmentation.vesselSegmentation(
            self.data3d,
            segmentation = np.ones(self.data3d.shape, dtype='int8'),
            #segmentation = oseg.orig_scale_segmentation,
            threshold = -1,
            inputSigma = 0.15,
            dilationIterations = 2,
            nObj = 1,
            biggestObjects = False,
#        dataFiltering = True,
            interactivity = True,
            binaryClosingIterations = 5,
            binaryOpeningIterations = 1)
        #self.data3d_thri = self.muxImage(
        #        self.data3d_thr2.astype(np.uint16),
        #        metadata
        #        )
        #sitk.Show(self.data3d_thri)

        #self.data3di = self.muxImage(
        #        self.data3d.astype(np.uint16),
        #        metadata
        #        )
        #sitk.Show(self.data3di)

        import pdb; pdb.set_trace()
        app = QApplication(sys.argv)

        pyed = seqt.QTSeedEditor(
                data3d,
                contours=data3d_thr.astype(np.int8)
                )
        #app.exec_()

        import pdb; pdb.set_trace()
        data3d_skel = skelet3d.skelet3d(data3d_thr)

        pyed = seqt.QTSeedEditor(
                data3d, 
                contours=data3d_thr.astype(np.int8),
                seeds=data3d_skel
                )
        app.exec_()

        #import itk
        #itk.

        #self.output = sitk.GetArrayFromImage(dataskel)

#   konluce
        dataskel_nd = sitk.GetArrayFromImage(dataskel)
        conv_kernel = np.ones([3,3,3], dtype=np.int16)
        filtered_nd = scipy.ndimage.filters.convolve(dataskel_nd, conv_kernel)
        filtered_nd = filtered_nd[dataskel_nd==1]


        #cf = sitk.ConvolutionImageFilter()
        #filtered = cf.Execute(dataskel, conv_kernel)
        filtered = sitk.GetImageFromArray(filtered_nd.astype(np.int16))

        sitk.Show(filtered * 10)
        import pdb; pdb.set_trace()


    def preprocessing(self):
        self.data3d = scipy.ndimage.filters.gaussian_filter(
                self.data3d,
                GAUSSIAN_SIGMA
                )
        self.data3d_thr = self.data3d > self.threshold

        self.data3d_thr2 = scipy.ndimage.morphology.binary_opening(
                self.data3d_thr
                )
        #gf = sitk.SmoothingRecursiveGaussianImageFilter()
        #gf.SetSigma(5)
        #gf = sitk.DiscreteGaussianImageFilter()
        #gf.SetVariance(1.0)
        #self.data3di2 = gf.Execute(self.data3di)#, 5)

        pass



    def muxImage(self, data3d, metadata):
        data3di = sitk.GetImageFromArray(data3d)
        data3di.SetSpacing(metadata['voxelsize_mm'])

        return data3di


        

        #sitk.

    def show(self):
        app = QApplication(sys.argv)
        seqt.QTSeedEditor(self.output.astype(np.int16))
        app.exec_()





if __name__ == "__main__":
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    #logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(description='\
            3D visualization of segmentation\n\
            \npython show_segmentation.py\n\
            \npython show_segmentation.py -i resection.pkl -l 2 3 4 -d 4')
    parser.add_argument('-i', '--inputfile',
            default='organ.pkl',
            help='input file')
    parser.add_argument('-t', '--threshold', type=int,
            default=6600,
            help='data threshold, default 1')
    parser.add_argument('-cr', '--crop', type=int, metavar='N', nargs='+',
            default=[0,-1,0,-1,0,-1],
            help='segmentation labels, default 1')
    args = parser.parse_args()

    #data = misc.obj_from_file(args.inputfile, filetype = 'pickle')


    dr = datareader.DataReader()
    data3d, metadata = dr.Get3DData(args.inputfile)
# crop data
    cr = args.crop
    data3d = data3d[cr[0]:cr[1], cr[2]:cr[3], cr[4]:cr[5]]



    ha = HistologyAnalyser(data3d, metadata, args.threshold)
    ha.run()
    ha.show()
    

