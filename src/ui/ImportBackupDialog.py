# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportBackupDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)
from  . import resource_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(513, 188)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bt_import = QPushButton(self.frame)
        self.bt_import.setObjectName(u"bt_import")
        self.bt_import.setMinimumSize(QSize(0, 40))
        self.bt_import.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_import.setStyleSheet(u"margin-top: 3px\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/assets/backup-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_import.setIcon(icon)
        self.bt_import.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.bt_import, 6, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.progress_bar_main = QProgressBar(self.frame)
        self.progress_bar_main.setObjectName(u"progress_bar_main")
        self.progress_bar_main.setValue(24)
        self.progress_bar_main.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_bar_main.setTextVisible(True)
        self.progress_bar_main.setOrientation(Qt.Horizontal)
        self.progress_bar_main.setInvertedAppearance(False)
        self.progress_bar_main.setTextDirection(QProgressBar.TopToBottom)

        self.gridLayout_2.addWidget(self.progress_bar_main, 3, 0, 1, 3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.bt_open = QPushButton(self.frame)
        self.bt_open.setObjectName(u"bt_open")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_open.sizePolicy().hasHeightForWidth())
        self.bt_open.setSizePolicy(sizePolicy)
        self.bt_open.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/folder-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_open.setIcon(icon1)

        self.gridLayout_3.addWidget(self.bt_open, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.txt_table = QLineEdit(self.frame)
        self.txt_table.setObjectName(u"txt_table")
        sizePolicy.setHeightForWidth(self.txt_table.sizePolicy().hasHeightForWidth())
        self.txt_table.setSizePolicy(sizePolicy)
        self.txt_table.setMaximumSize(QSize(100, 16777215))
        self.txt_table.setReadOnly(True)

        self.gridLayout_3.addWidget(self.txt_table, 1, 1, 1, 1)

        self.txt_source = QLineEdit(self.frame)
        self.txt_source.setObjectName(u"txt_source")
        self.txt_source.setReadOnly(True)

        self.gridLayout_3.addWidget(self.txt_source, 0, 1, 1, 2)

        self.progress_bar_table = QProgressBar(self.frame)
        self.progress_bar_table.setObjectName(u"progress_bar_table")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progress_bar_table.sizePolicy().hasHeightForWidth())
        self.progress_bar_table.setSizePolicy(sizePolicy2)
        self.progress_bar_table.setMinimumSize(QSize(200, 0))
        self.progress_bar_table.setValue(24)
        self.progress_bar_table.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_bar_table.setTextVisible(True)
        self.progress_bar_table.setOrientation(Qt.Horizontal)
        self.progress_bar_table.setInvertedAppearance(False)
        self.progress_bar_table.setTextDirection(QProgressBar.TopToBottom)

        self.gridLayout_3.addWidget(self.progress_bar_table, 1, 2, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 3)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.txt_source)
        self.label_3.setBuddy(self.txt_source)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"IMPORTAR BACKUP", None))
        self.bt_import.setText(QCoreApplication.translate("Dialog", u"  IMPORTAR", None))
#if QT_CONFIG(shortcut)
        self.bt_import.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"FONTE", None))
#if QT_CONFIG(tooltip)
        self.bt_open.setToolTip(QCoreApplication.translate("Dialog", u"ABRIR", None))
#endif // QT_CONFIG(tooltip)
        self.bt_open.setText("")
#if QT_CONFIG(shortcut)
        self.bt_open.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"TABELA", None))
        self.txt_table.setText(QCoreApplication.translate("Dialog", u"cliente", None))
    # retranslateUi

