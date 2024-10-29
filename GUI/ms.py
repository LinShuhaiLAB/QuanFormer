# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ms.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableWidget, QTableWidgetItem, QTextBrowser,
    QWidget)

class Ui_QuanFormer(object):
    def setupUi(self, QuanFormer):
        if not QuanFormer.objectName():
            QuanFormer.setObjectName(u"QuanFormer")
        QuanFormer.resize(837, 603)
        self.centralwidget = QWidget(QuanFormer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.eicPostprogress = QPushButton(self.centralwidget)
        self.eicPostprogress.setObjectName(u"eicPostprogress")

        self.gridLayout.addWidget(self.eicPostprogress, 15, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 6, 2, 1)

        self.listWidget_2 = QListWidget(self.centralwidget)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.gridLayout.addWidget(self.listWidget_2, 11, 4, 5, 1)

        self.featureImport = QPushButton(self.centralwidget)
        self.featureImport.setObjectName(u"featureImport")

        self.gridLayout.addWidget(self.featureImport, 3, 2, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 8, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout.addWidget(self.listWidget, 11, 3, 5, 1)

        self.resultsExport = QPushButton(self.centralwidget)
        self.resultsExport.setObjectName(u"resultsExport")

        self.gridLayout.addWidget(self.resultsExport, 13, 1, 1, 1)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 16, 0, 1, 6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 5, 2, 1, 1)

        self.showEIC = QLabel(self.centralwidget)
        self.showEIC.setObjectName(u"showROIs")
        self.showEIC.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout.addWidget(self.showEIC, 1, 3, 10, 2)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        font1 = QFont()
        font1.setPointSize(14)
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 1, 1, 1, 1)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 4, 1, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 4, 2, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 10, 1, 1, 1)

        self.mzmlImport = QPushButton(self.centralwidget)
        self.mzmlImport.setObjectName(u"mzmlImport")

        self.gridLayout.addWidget(self.mzmlImport, 3, 1, 1, 1)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(218, 0))
        font2 = QFont()
        font2.setPointSize(8)
        self.tableWidget.setFont(font2)

        self.gridLayout.addWidget(self.tableWidget, 1, 5, 15, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 9, 2, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 6, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 7, 0, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 12, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 9, 0, 1, 1)

        self.eicQuantify = QPushButton(self.centralwidget)
        self.eicQuantify.setObjectName(u"roiQuantify")

        self.gridLayout.addWidget(self.eicQuantify, 11, 1, 1, 1)

        self.eicBuild = QPushButton(self.centralwidget)
        self.eicBuild.setObjectName(u"roiBuild")

        self.gridLayout.addWidget(self.eicBuild, 7, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 14, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)

        self.eicPredict = QPushButton(self.centralwidget)
        self.eicPredict.setObjectName(u"roiPredict")

        self.gridLayout.addWidget(self.eicPredict, 9, 1, 1, 1)

        self.modelLoad = QPushButton(self.centralwidget)
        self.modelLoad.setObjectName(u"modelLoad")

        self.gridLayout.addWidget(self.modelLoad, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 15, 6, 1, 1)

        QuanFormer.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(QuanFormer)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 837, 21))
        QuanFormer.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(QuanFormer)
        self.statusbar.setObjectName(u"statusbar")
        QuanFormer.setStatusBar(self.statusbar)

        self.retranslateUi(QuanFormer)

        QMetaObject.connectSlotsByName(QuanFormer)
    # setupUi

    def retranslateUi(self, QuanFormer):
        QuanFormer.setWindowTitle(QCoreApplication.translate("QuanFormer", u"QuanFormer", None))
        self.eicPostprogress.setText(QCoreApplication.translate("QuanFormer", u"postprogress", None))
        self.featureImport.setText(QCoreApplication.translate("QuanFormer", u"csv", None))
        self.label_4.setText(QCoreApplication.translate("QuanFormer", u"QuanFormer predict", None))
        self.label_2.setText(QCoreApplication.translate("QuanFormer", u"Feature table import", None))
        self.resultsExport.setText(QCoreApplication.translate("QuanFormer", u"csv", None))
        self.pushButton.setText(QCoreApplication.translate("QuanFormer", u"output", None))
        self.showEIC.setText("")
        self.label_8.setText(QCoreApplication.translate("QuanFormer", u"QuanFormer", None))
        self.label_10.setText(QCoreApplication.translate("QuanFormer", u"Model load", None))
        self.label_9.setText(QCoreApplication.translate("QuanFormer", u"Set ROIs output dir", None))
        self.label_5.setText(QCoreApplication.translate("QuanFormer", u"Peak quantify", None))
        self.mzmlImport.setText(QCoreApplication.translate("QuanFormer", u"mzML", None))
        self.checkBox.setText(QCoreApplication.translate("QuanFormer", u"plot", None))
        self.label_3.setText(QCoreApplication.translate("QuanFormer", u"ROIs build", None))
        self.label_7.setText(QCoreApplication.translate("QuanFormer", u"Results export", None))
        self.eicQuantify.setText(QCoreApplication.translate("QuanFormer", u"quantify", None))
        self.eicBuild.setText(QCoreApplication.translate("QuanFormer", u"ROIs", None))
        self.label_6.setText(QCoreApplication.translate("QuanFormer", u"Results postprogress", None))
        self.label.setText(QCoreApplication.translate("QuanFormer", u"mzML files import", None))
        self.eicPredict.setText(QCoreApplication.translate("QuanFormer", u"predict", None))
        self.modelLoad.setText(QCoreApplication.translate("QuanFormer", u"model", None))
    # retranslateUi

