# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SupplierDialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QGridLayout,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QWidget)
from  . import resource_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(385, 304)
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.txt_supplier = QLineEdit(Dialog)
        self.txt_supplier.setObjectName(u"txt_supplier")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_supplier.sizePolicy().hasHeightForWidth())
        self.txt_supplier.setSizePolicy(sizePolicy)
        self.txt_supplier.setMinimumSize(QSize(200, 0))

        self.gridLayout.addWidget(self.txt_supplier, 1, 1, 1, 1)

        self.bt_delete = QPushButton(Dialog)
        self.bt_delete.setObjectName(u"bt_delete")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bt_delete.sizePolicy().hasHeightForWidth())
        self.bt_delete.setSizePolicy(sizePolicy1)
        self.bt_delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_delete.setStyleSheet(u"margin-top: 3px")
        icon = QIcon()
        icon.addFile(u":/icons/assets/delete-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_delete.setIcon(icon)
        self.bt_delete.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.bt_delete, 3, 0, 1, 3)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.bt_search = QPushButton(Dialog)
        self.bt_search.setObjectName(u"bt_search")
        self.bt_search.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/search-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_search.setIcon(icon1)
        self.bt_search.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.bt_search, 1, 2, 1, 1)

        self.list_suppliers = QListView(Dialog)
        self.list_suppliers.setObjectName(u"list_suppliers")
        self.list_suppliers.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.list_suppliers.setAlternatingRowColors(True)
        self.list_suppliers.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_suppliers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_suppliers.setViewMode(QListView.ListMode)

        self.gridLayout.addWidget(self.list_suppliers, 2, 0, 1, 3)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.txt_supplier)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.txt_supplier, self.bt_search)
        QWidget.setTabOrder(self.bt_search, self.list_suppliers)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"FORNECEDORES", None))
        self.bt_delete.setText(QCoreApplication.translate("Dialog", u"DELETAR", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"FORNECEDOR", None))
#if QT_CONFIG(tooltip)
        self.bt_search.setToolTip(QCoreApplication.translate("Dialog", u"PESQUISAR", None))
#endif // QT_CONFIG(tooltip)
        self.bt_search.setText("")
    # retranslateUi

