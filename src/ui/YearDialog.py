# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'YearDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QWidget)
from  . import resource_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(157, 83)
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.cb_years = QComboBox(Dialog)
        self.cb_years.setObjectName(u"cb_years")

        self.gridLayout.addWidget(self.cb_years, 0, 3, 1, 1)

        self.bt_delete = QPushButton(Dialog)
        self.bt_delete.setObjectName(u"bt_delete")
        self.bt_delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_delete.setStyleSheet(u"margin-top: 3px")
        icon = QIcon()
        icon.addFile(u":/icons/assets/delete-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_delete.setIcon(icon)
        self.bt_delete.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.bt_delete, 1, 2, 1, 2)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.cb_years)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Anos", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"ANO", None))
        self.bt_delete.setText(QCoreApplication.translate("Dialog", u"DELETAR", None))
    # retranslateUi

