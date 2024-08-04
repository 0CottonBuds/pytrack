# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_record.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QProgressBar, QSizePolicy, QVBoxLayout, QWidget)

class Ui_window_record(object):
    def setupUi(self, window_record):
        if not window_record.objectName():
            window_record.setObjectName(u"window_record")
        window_record.resize(400, 55)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(window_record.sizePolicy().hasHeightForWidth())
        window_record.setSizePolicy(sizePolicy)
        window_record.setMinimumSize(QSize(400, 50))
        window_record.setMaximumSize(QSize(6000, 55))
        window_record.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_2 = QVBoxLayout(window_record)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(window_record)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_name = QLabel(self.frame)
        self.label_name.setObjectName(u"label_name")
        font = QFont()
        font.setPointSize(12)
        self.label_name.setFont(font)

        self.verticalLayout.addWidget(self.label_name)

        self.label_total_time = QLabel(self.frame)
        self.label_total_time.setObjectName(u"label_total_time")

        self.verticalLayout.addWidget(self.label_total_time)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_2)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.progressBar = QProgressBar(window_record)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(400, 0))
        self.progressBar.setMaximumSize(QSize(400, 16777215))
        self.progressBar.setStyleSheet(u"QProgressBar::chunk {\n"
"    \n"
"	\n"
"	background-color: rgb(177, 255, 153);\n"
"	border-radius: 6px;\n"
"	border-left:1px black;\n"
"}\n"
"QProgressBar {\n"
"border: 1px solid rgba(33, 37, 43, 180);\n"
"border-radius: 10px;\n"
"text-align: right;\n"
"background-color:rgb(255, 255, 255);\n"
"color: black;\n"
"}\n"
"")
        self.progressBar.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar)


        self.retranslateUi(window_record)

        QMetaObject.connectSlotsByName(window_record)
    # setupUi

    def retranslateUi(self, window_record):
        window_record.setWindowTitle(QCoreApplication.translate("window_record", u"Form", None))
        self.label_name.setText(QCoreApplication.translate("window_record", u"Name:", None))
        self.label_total_time.setText(QCoreApplication.translate("window_record", u"Total Time:", None))
    # retranslateUi

