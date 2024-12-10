import pandas as pd
import os


class PeakList():
    def __init__(self, peakList=None):
        if type(peakList) == type(None):
            self.peakList = pd.DataFrame()
        else:
            self.peakList = peakList

    def from_df(self, df, sampleCols=None):
        self.peakList = df
        if sampleCols is None:
            self.sampleCols = [x for x in self.peakList.columns.values if
                               x not in ["mz", "rt", "rt_start", "rt_end", "isotope", "adduct", "peak group"]]
        else:
            self.sampleCols = sampleCols

    def to_csv(self, fn):
        self.peakList.to_csv(fn)

    def to_skyline(self, fn, polarity, moleculeListName="XCMS peaks"):
        transitionList = pd.DataFrame(self.peakList)
        transitionList["Precursor Name"] = ["unknown " + str(index) for index, row in transitionList.iterrows()]
        transitionList["Explicit Retention Time"] = [row["rt"] for index, row in
                                                     transitionList.iterrows()]
        polMapper = {"Positive": 1, "Negative": -1}
        transitionList["Precursor Charge"] = [polMapper[polarity] for index, row in transitionList.iterrows()]
        transitionList["Precursor m/z"] = [row["mz"] for index, row in transitionList.iterrows()]
        transitionList["Molecule List Name"] = [moleculeListName for _ in range(len(transitionList))]
        transitionList = transitionList[
            ["Molecule List Name", "Precursor Name", "Precursor m/z", "Precursor Charge",
             "Explicit Retention Time"]]
        transitionList.to_csv(fn)

    def readXCMSPeakList(self, filename, key=".mzML"):
        data = pd.read_csv(filename, index_col=0, sep="\t")
        data_form = {}
        self.sampleCols = [x for x in data.columns.values if key in x]
        for col in self.sampleCols:
            data[col] = data[col].fillna(0)
        for index, row in data.iterrows():
            data_form[index] = {"mz": row["mzmed"], "rt": row["rtmed"] / 60, "rt_start": row["rtmin"] / 60,
                                "rt_end": row["rtmax"] / 60}  # ,"isotope_xcms":row["isotopes"],"adduct_xcms":row["adduct"],"peak group":row["pcgroup"]}
            for col in self.sampleCols:
                data_form[index][col] = row[col]

        self.peakList = pd.DataFrame.from_dict(data_form, orient="index")

    def runXCMS(self, path, fn, polarity, ppm, peakWidth, noise=1000, s2n=1, prefilter=2, mzDiff=0.0001, minFrac=0.5):
        dir = os.path.dirname(__file__)
        os.system("Rscript " + os.path.join(dir, "find_peaks.R") + " " + path + " " + polarity + " " + str(
            ppm) + " " + str(peakWidth[0]) + " " + str(peakWidth[1]) + " " + fn + " " + str(noise) + " " + str(
            s2n) + " " + str(prefilter) + " " + str(mzDiff) + " " + str(minFrac))
        self.readXCMSPeakList(os.path.join(path, fn))

    def installRPackages(self):
        dir = os.path.dirname(__file__)
        os.system("Rscript " + os.path.join(dir, "install_R_packages.R"))


def get_targeted_features(datadir, polarity, ms1ppm, peakWidth = (5,50), s2n=5, noise=100, mzDiff=0.015, prefilter=3):

    det = PeakList()
    det.runXCMS(datadir, "xcms_peak_list.csv", polarity, ms1ppm, peakWidth,s2n=s2n,noise=noise,mzDiff=mzDiff,prefilter=prefilter)
    det.readXCMSPeakList(os.path.join(datadir, "xcms_peak_list.csv"))
    peakList = pd.DataFrame(det.peakList)
    peakList.to_csv(os.path.join(datadir, "peak_list.csv"), index=False)
    peakList = peakList.iloc[:, :2].reset_index(drop=True)
    peakList.rename(columns={"rt": "RT"}, inplace=True)
    peakList['Compound Name'] = range(1, len(peakList)+1)
    peakList.insert(0, 'Compound Name', peakList.pop('Compound Name'))

    return peakList


#
