library("MSnbase")
library("xcms")

args = commandArgs(trailingOnly=TRUE)

pathData <- args[1] #path to your .mzML
charge <- args[2]
ppm <- as.numeric(args[3])
minWidth <- as.numeric(args[4])
maxWidth <- as.numeric(args[5])
noise <- as.numeric(args[7])#1
s2n <- as.numeric(args[8])#14.14
prefilter <- as.numeric(args[9])#1
mzDiff <- as.numeric(args[10])#.0001
frac <- as.numeric(args[11])
fn <- args[6]

register(SerialParam())


setwd(pathData)

files = list.files(pattern = "*.mzML")

numFiles = length(files)

xs = readMSData(files,mode="onDisk",msLevel=1)

xs = filterEmptySpectra(xs)

params <- CentWaveParam(ppm = ppm, peakwidth = c(minWidth, maxWidth),noise=noise,
                        snthresh = s2n,mzdiff = mzDiff,prefilter = c(prefilter,100),
                        mzCenterFun = "wMean",integrate = 1,fitgauss = FALSE,verboseColumns = FALSE)

xs2 <- findChromPeaks(xs,params,return.type="XCMSnExp")

pdp <- PeakDensityParam(sampleGroups = rep(1,numFiles),
                        minFraction = frac,bw=5)

xs2 = groupChromPeaks(xs2,param=pdp)


xs2 = adjustRtime(xs2, ObiwarpParam(binSize = 1,))

xs2 = groupChromPeaks(xs2,param=pdp)

xs3 = fillChromPeaks(xs2)

#format results
peakInfo = featureDefinitions(xs3)
intensities = featureValues(xs3)
peaktable = merge(peakInfo, intensities,
                          by = 'row.names', all = TRUE)

#write output
drop <- c("peakidx")
write.table(peaktable[,!(names(peaktable) %in% drop)],fn,sep="\t",row.names=FALSE,col.names=TRUE)


#xs3 = xs2

#xs4 = as(xs3, "xcmsSet")

#ann = annotate(xs4,polarity=charge,maxcharge=2,ppm=ppm)

#peaks = getPeaklist(ann)

#write.csv(peaks,fn)
       