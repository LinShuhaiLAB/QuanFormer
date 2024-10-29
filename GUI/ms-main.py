import os
import logging
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
from datetime import datetime

from natsort import natsorted
from GUI.ms import Ui_QuanFormer
from main import *

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.postprocess_thread = None
        self.area = None
        self.results = None
        self.xic_list = None
        self.xic_info = None
        self.paths = None
        self.current_time = None
        self.args = get_args_parser().parse_args([])
        self.ui = Ui_QuanFormer()
        self.ui.setupUi(self)
        self.bind()

        self.mzml_thread = None
        self.feature_thread = None
        self.export_thread = None
        self.model_thread = None
        self.eic_build_thread = None
        self.eic_output_thread = None
        self.predict_thread = None
        self.quantify_thread = None

    def bind(self):
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.ui.mzmlImport.clicked.connect(self.mzml_import)
        self.ui.featureImport.clicked.connect(self.feature_import)
        self.ui.modelLoad.clicked.connect(self.model_load)
        self.ui.pushButton.clicked.connect(self.set_output_dir)
        self.ui.eicBuild.clicked.connect(self.on_eic_build_clicked)
        self.ui.listWidget.currentItemChanged.connect(self.on_list_item_changed)
        self.ui.listWidget_2.currentItemChanged.connect(self.show_eic)
        self.ui.eicPredict.clicked.connect(self.on_eic_predict_clicked)
        self.ui.eicQuantify.clicked.connect(self.on_eic_quantify_clicked)
        self.ui.resultsExport.clicked.connect(self.on_results_export_clicked)
        self.ui.eicPostprogress.clicked.connect(self.on_eic_postprogress_clicked)

    def mzml_import(self):
        mzml_dir = QFileDialog.getExistingDirectory(self, "Select mzML Folder", "")
        if mzml_dir:
            self.args.source = mzml_dir
            self.ui.textBrowser.append(f"{self.current_time}  Successfully select mzML dir:  {self.args.source} ")

            self.mzml_thread = MzmlImportThread(mzml_dir)
            self.mzml_thread.import_finished.connect(
                lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
            self.mzml_thread.start()
        else:
            return None

    def feature_import(self):
        table_path, _ = QFileDialog.getOpenFileName(self, "Save Feature File", "", "Feature Files (*.csv)")
        if table_path:
            self.args.feature = table_path
            self.ui.textBrowser.append(
                f"{self.current_time}  Successfully import feature table:  {self.args.feature}")

            self.feature_thread = FeatureImportThread(table_path, self.ui.tableWidget)
            self.feature_thread.import_finished.connect(
                lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
            self.feature_thread.start()
        else:
            return None

    def model_load(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Save Model File", "", "Model Files (*.pth)")
        if model_path:
            self.args.model = model_path
            self.ui.textBrowser.append(
                f"{self.current_time}  Successfully load model:  {self.args.model}")

            self.model_thread = ModelImportThread(model_path)
            self.model_thread.import_finished.connect(
                lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
            self.model_thread.start()
        else:
            return None

    def set_output_dir(self):
        eic_output_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
        if eic_output_dir:
            self.args.images_path = eic_output_dir
            self.ui.textBrowser.append(
                f"{self.current_time}  Successfully set output dir:  {self.args.images_path}")

            self.eic_output_thread = EicOutputThread(eic_output_dir)
            self.eic_output_thread.import_finished.connect(
                lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
            self.eic_output_thread.start()
        else:
            return None

    def on_eic_build_clicked(self):
        if self.args.source and self.args.feature:
            self.eic_build_thread = EicBuildThread(self.args.source, self.args.feature, self.args)
            self.eic_build_thread.build_finished.connect(self.on_eic_build_finished)
            self.ui.textBrowser.append(f"{self.current_time}  Start to build ROIs, wait for a moment please")
            self.eic_build_thread.start()
        else:
            self.ui.textBrowser.append(f"{self.current_time}  Please provide both mzML path and targeted feature path.")

    def on_list_item_changed(self):
        if self.args.images_path:
            new_path = os.path.join(self.args.images_path, self.ui.listWidget.currentItem().text())
            self.ui.listWidget_2.addItems(natsorted(d for d in os.listdir(new_path)))

    def show_eic(self):
        if self.ui.listWidget_2.currentItem():
            new_path = os.path.join(self.args.images_path,
                                    self.ui.listWidget.currentItem().text(),
                                    self.ui.listWidget_2.currentItem().text())
            fixed_size = QtCore.QSize(328, 251)
            self.ui.showEIC.setPixmap(QPixmap(new_path).scaled(fixed_size))

    def on_eic_predict_clicked(self):
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.ui.textBrowser.append(f"{self.current_time}  Start to predict ROIs, wait for a moment please")
        if self.xic_list is not None:  # 确保xic_list已初始化且不为空
            self.predict_thread = EicPredictThread(self.args.model, self.args.images_path,
                                                   self.ui.checkBox.isChecked())
            self.predict_thread.predict_finished.connect(self.on_eic_predict_finished)
            self.predict_thread.start()
        else:
            self.ui.textBrowser.append(f"{self.current_time}  No ROI data available to predict.")

    def on_eic_quantify_clicked(self):
        self.current_time = datetime.now().strftime("%H:%M:%S")
        if self.results is not None:
            self.quantify_thread = EicQuantifyThread(self.xic_list, self.results, self.xic_info)
            self.quantify_thread.quantify_finished.connect(self.on_eic_quantify_finished)
            self.quantify_thread.start()
        else:
            self.ui.textBrowser.append(f"{self.current_time}  No prediction results available for quantification.")

    def on_results_export_clicked(self):
        self.current_time = datetime.now().strftime("%H:%M:%S")
        if self.area is not None:
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "CSV Files (*.csv)")
            if output_path:
                self.args.output = output_path
                self.export_thread = ResultsExportThread(self.area, self.args.output, self.ui.tableWidget)
                self.export_thread.export_finished.connect(
                    lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
                self.export_thread.start()
            else:
                return None
        else:
            self.ui.textBrowser.append(f"{self.current_time}  No quantitative results available for export.")

    def on_eic_postprogress_clicked(self):
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.ui.textBrowser.append(f"{self.current_time}  Start to post process ROIs")
        if self.args.output:
            self.postprocess_thread = EicPostProcessThread(self.args.output, self.args.feature, self.ui.tableWidget)
            self.postprocess_thread.postprocess_finished.connect(
                lambda msg: self.ui.textBrowser.append(f"{self.current_time}  {msg}"))
            self.postprocess_thread.start()

    def on_eic_build_finished(self, msg, xic_info, xic_list, image_filenames):
        self.ui.textBrowser.append(f"{self.current_time}  {msg}")
        self.xic_info = xic_info
        self.xic_list = xic_list
        self.ui.listWidget.addItems(image_filenames)

    def on_eic_predict_finished(self, msg, results):
        self.ui.textBrowser.append(f"{self.current_time}  {msg}")
        self.results = results

    def on_eic_quantify_finished(self, msg, area):
        self.ui.textBrowser.append(f"{self.current_time}  {msg}")
        self.area = area



class MzmlImportThread(QtCore.QThread):
    import_finished = Signal(str)

    def __init__(self, mzml_dir):
        super().__init__()
        self.mzml_dir = mzml_dir

    def run(self):
        self.import_finished.emit("mzML import finished!")


class FeatureImportThread(QtCore.QThread):
    import_finished = Signal(str)

    def __init__(self, table_path, table_widget):
        super().__init__()
        self.table_path = table_path
        self.ui = table_widget

    def run(self):
        try:
            import pandas as pd
            df = pd.read_csv(self.table_path)
            self.ui.setRowCount(len(df))
            self.ui.setColumnCount(len(df.columns))
            self.ui.setHorizontalHeaderLabels(df.columns)
            self.ui.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            # 填充表格
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    self.ui.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

            self.import_finished.emit("Feature import finished!")
        except Exception as e:
            logging.error(f"Error importing features: {e}")
            self.import_finished.emit(f"Error: {str(e)}")


class ModelImportThread(QtCore.QThread):
    import_finished = Signal(str)

    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    def run(self):
        self.import_finished.emit("model load finished!")


class EicOutputThread(QtCore.QThread):
    import_finished = Signal(str)

    def __init__(self, eic_output_dir):
        super().__init__()
        self.eic_output_dir = eic_output_dir

    def run(self):
        self.import_finished.emit("output dir set finished!")


class EicBuildThread(QtCore.QThread):
    build_finished = Signal(str, object, object, list)

    def __init__(self, mzml_path, feature, args):
        super().__init__()

        self.source = mzml_path
        self.feature = feature
        self.args = args
        self.plot = True

    def run(self):
        paths = get_files(self.source, "mzML")
        xic_info = read_targeted_features(self.feature)
        xic_list = build_roi(paths, xic_info, self.plot, self.args)
        self.build_finished.emit(
            f"Successfully built EIC", xic_info, xic_list, [d for d in os.listdir(self.args.images_path)])


class EicPredictThread(QtCore.QThread):
    predict_finished = Signal(str, list)  # 发射一个字符串和结果字典

    def __init__(self, model_path, images_path, with_plot):
        super().__init__()
        self.model_path = model_path
        self.images_path = images_path
        self.with_plot = with_plot

    def run(self):
        if self.with_plot:
            results = build_predictor(self.model_path, self.images_path, plot=True)
            self.predict_finished.emit("Successfully predict ROIs with plot", results)
        else:
            results = build_predictor(self.model_path, self.images_path, plot=False)
            self.predict_finished.emit("Successfully predict ROIs without plot", results)
            

class EicQuantifyThread(QtCore.QThread):
    quantify_finished = Signal(str, list)

    def __init__(self, xic_list, results, xic_info):
        super().__init__()
        self.xic_list = xic_list
        self.results = results
        self.xic_info = xic_info

    def run(self):
        area = quantify(self.xic_list, self.results, self.xic_info)
        self.quantify_finished.emit("Successfully quantify ROIs", area)


class ResultsExportThread(QtCore.QThread):
    export_finished = Signal(str)

    def __init__(self, area, output, table_widget):
        super().__init__()
        self.area = area
        self.output = output
        self.table_widget = table_widget

    def run(self):
        export_results(self.area, self.output)
        self.export_finished.emit(f"Successfully exported results to: {self.output}")
        df = pd.read_csv(self.output)
        self.populate_table(df)

    def populate_table(self, df):
        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


class EicPostProcessThread(QtCore.QThread):
    postprocess_finished = Signal(str)

    def __init__(self, output, feature, table_widget):
        super().__init__()
        self.output = output
        self.feature = feature
        self.table_widget = table_widget

    def run(self):
        post_process(self.output, self.feature)
        self.postprocess_finished.emit("Successfully completed post-processing")
        df = pd.read_csv(self.output)
        self.populate_table(df)

    def populate_table(self, df):
        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
