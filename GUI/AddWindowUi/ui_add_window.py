# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_add_widget(object):
    def setupUi(self, add_widget):
        if not add_widget.objectName():
            add_widget.setObjectName(u"add_widget")
        add_widget.resize(497, 41)
        add_widget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.horizontalLayout = QHBoxLayout(add_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_name = QComboBox(add_widget)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setMinimumSize(QSize(175, 0))
        self.comboBox_name.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.comboBox_name)

        self.comboBox_type = QComboBox(add_widget)
        self.comboBox_type.setObjectName(u"comboBox_type")

        self.horizontalLayout.addWidget(self.comboBox_type)

        self.lineEdit_points = QLineEdit(add_widget)
        self.lineEdit_points.setObjectName(u"lineEdit_points")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_points.sizePolicy().hasHeightForWidth())
        self.lineEdit_points.setSizePolicy(sizePolicy)
        self.lineEdit_points.setMaximumSize(QSize(75, 50))

        self.horizontalLayout.addWidget(self.lineEdit_points)

        self.button_confirm = QPushButton(add_widget)
        self.button_confirm.setObjectName(u"button_confirm")
        self.button_confirm.setMaximumSize(QSize(50, 16777215))
        self.button_confirm.setFlat(True)

        self.horizontalLayout.addWidget(self.button_confirm)

        self.button_ignore = QPushButton(add_widget)
        self.button_ignore.setObjectName(u"button_ignore")
        self.button_ignore.setMaximumSize(QSize(50, 50))
        self.button_ignore.setFlat(True)

        self.horizontalLayout.addWidget(self.button_ignore)


        self.retranslateUi(add_widget)

        QMetaObject.connectSlotsByName(add_widget)
    # setupUi

    def retranslateUi(self, add_widget):
        add_widget.setWindowTitle(QCoreApplication.translate("add_widget", u"Form", None))
        self.lineEdit_points.setPlaceholderText(QCoreApplication.translate("add_widget", u"Points", None))
        self.button_confirm.setText(QCoreApplication.translate("add_widget", u"Confirm", None))
        self.button_ignore.setText(QCoreApplication.translate("add_widget", u"Ignore", None))
    # retranslateUi

