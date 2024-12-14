#！pip install peakdetective
#!pip install sklearn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import PeakDetective
import PeakDetective.detection_helper as detection_helper
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pickle as pkl
import os
import shutil

#model parameters, not recomended to change
resolution = 60 #number of data point in 1 min EIC
window = 1.0 #size of EIC window (in minutes)
min_peaks = 100000 #minimum number of peaks used to train autoencoder
smooth_epochs = 10 #number of smoothing epochs to use
batchSizeSmoother = 64 #batch size for training smoother
validationSplitSmoother = 0.1 #fraction of data used for validation split when training smoother
minClassifierTrainEpochs = 200 #minimum number of epochs for training classifier
maxClassifierTrainEpochs = 1000 #maximum number of epochs for training classifier
classifierBatchSize = 4 #batch size for training classifier
randomRestarts = 1 #number of random restarts to use when training classifier
numValPeaks = 10 #number of validaiton peaks for user to label
numPeaksPerRound = 10 #number of peaks to label per active learning iteration
numCores = -1 #number of processor cores to use
numDataPoints = 3 #number of consequetive scans above noise to count as ROI

peakFile='/home/zzy/data/raw-mzml/good-mzml/QE-feature-ex-1.csv'
mzmlFolder='/home/zzy/data/raw-mzml/good-mzml/QE_TEST'
weightsPath = '/home/zzy/peakdetective/example_data_for_colab/xcms_example_data/PeakDetectiveObject/'
integ = PeakDetective.PeakDetective(numCores=numCores, resolution=resolution)

align=True
ms1ppm=5
cutoff=0.8

peaklist = pd.read_csv(peakFile,index_col=0)[["mz", "rt"]]

#load raw data
raw_data = []
for file in [x for x in os.listdir(mzmlFolder) if ".mzML" in x]:
    temp = PeakDetective.rawData()
    temp.readRawDataFile(mzmlFolder + "/" + file, ms1ppm)
    raw_data.append(temp)

X = integ.makeDataMatrix(raw_data,peaklist["mz"], peaklist["rt"].values, align=align)
for r in raw_data:
    peaklist[r.filename] = 1.0
peak_areas = integ.performIntegration(X, [r.filename for r in raw_data], peaklist, cutoff, defaultWidth=0.5,smooth=False)


peak_areas.to_csv("SB-qe_5.csv")