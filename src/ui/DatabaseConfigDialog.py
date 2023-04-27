# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatabaseConfigDialog.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
from  . import resource_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(566, 276)
        Dialog.setStyleSheet(u"QGroupBox {\n"
"	border: none;\n"
"	padding: 15px 0\n"
"}")
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_2, 3, 1, 1, 1)

        self.txt_source = QLineEdit(self.frame)
        self.txt_source.setObjectName(u"txt_source")
        self.txt_source.setReadOnly(True)

        self.gridLayout_2.addWidget(self.txt_source, 2, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 316, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 4, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bt_new = QPushButton(self.frame)
        self.bt_new.setObjectName(u"bt_new")
        font1 = QFont()
        font1.setBold(False)
        self.bt_new.setFont(font1)
        self.bt_new.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/assets/db.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_new.setIcon(icon)
        self.bt_new.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.bt_new)

        self.bt_open = QPushButton(self.frame)
        self.bt_open.setObjectName(u"bt_open")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_open.sizePolicy().hasHeightForWidth())
        self.bt_open.setSizePolicy(sizePolicy)
        self.bt_open.setFont(font1)
        self.bt_open.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_open.setIcon(icon1)
        self.bt_open.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.bt_open)


        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 1, 1, 2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1)

        self.frame_backup = QFrame(self.frame)
        self.frame_backup.setObjectName(u"frame_backup")
        self.frame_backup.setMinimumSize(QSize(0, 0))
        self.frame_backup.setFrameShape(QFrame.StyledPanel)
        self.frame_backup.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_backup)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.group_frequency = QGroupBox(self.frame_backup)
        self.group_frequency.setObjectName(u"group_frequency")
        self.group_frequency.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.group_frequency.setFlat(False)
        self.group_frequency.setCheckable(False)
        self.verticalLayout_2 = QVBoxLayout(self.group_frequency)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radio_no_backup = QRadioButton(self.group_frequency)
        self.radio_no_backup.setObjectName(u"radio_no_backup")
        self.radio_no_backup.setChecked(True)

        self.verticalLayout_2.addWidget(self.radio_no_backup)

        self.radio_diary = QRadioButton(self.group_frequency)
        self.radio_diary.setObjectName(u"radio_diary")

        self.verticalLayout_2.addWidget(self.radio_diary)

        self.radio_weekly = QRadioButton(self.group_frequency)
        self.radio_weekly.setObjectName(u"radio_weekly")

        self.verticalLayout_2.addWidget(self.radio_weekly)

        self.radio_monthly = QRadioButton(self.group_frequency)
        self.radio_monthly.setObjectName(u"radio_monthly")

        self.verticalLayout_2.addWidget(self.radio_monthly)


        self.horizontalLayout_2.addWidget(self.group_frequency)

        self.group_max_backup = QGroupBox(self.frame_backup)
        self.group_max_backup.setObjectName(u"group_max_backup")
        self.group_max_backup.setFlat(False)
        self.verticalLayout_3 = QVBoxLayout(self.group_max_backup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radio_3 = QRadioButton(self.group_max_backup)
        self.radio_3.setObjectName(u"radio_3")
        self.radio_3.setChecked(True)

        self.verticalLayout_3.addWidget(self.radio_3)

        self.radio_5 = QRadioButton(self.group_max_backup)
        self.radio_5.setObjectName(u"radio_5")

        self.verticalLayout_3.addWidget(self.radio_5)

        self.radio_10 = QRadioButton(self.group_max_backup)
        self.radio_10.setObjectName(u"radio_10")

        self.verticalLayout_3.addWidget(self.radio_10)


        self.horizontalLayout_2.addWidget(self.group_max_backup)


        self.gridLayout_2.addWidget(self.frame_backup, 3, 2, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.radio_no_backup)
        self.label.setBuddy(self.txt_source)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.txt_source, self.radio_no_backup)
        QWidget.setTabOrder(self.radio_no_backup, self.radio_diary)
        QWidget.setTabOrder(self.radio_diary, self.radio_weekly)
        QWidget.setTabOrder(self.radio_weekly, self.radio_monthly)
        QWidget.setTabOrder(self.radio_monthly, self.radio_3)
        QWidget.setTabOrder(self.radio_3, self.radio_5)
        QWidget.setTabOrder(self.radio_5, self.radio_10)
        QWidget.setTabOrder(self.radio_10, self.bt_new)
        QWidget.setTabOrder(self.bt_new, self.bt_open)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"CONFIGURAR BANCO DE DADOS", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"BACKUP", None))
        self.bt_new.setText(QCoreApplication.translate("Dialog", u" NOVO BANCO", None))
#if QT_CONFIG(shortcut)
        self.bt_new.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.bt_open.setText(QCoreApplication.translate("Dialog", u" BANCO EXISTENTE", None))
#if QT_CONFIG(shortcut)
        self.bt_open.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("Dialog", u"BANCO DE DADOS", None))
        self.group_frequency.setTitle(QCoreApplication.translate("Dialog", u"FREQU\u00caNCIA", None))
        self.radio_no_backup.setText(QCoreApplication.translate("Dialog", u"SEM BACKUP", None))
        self.radio_diary.setText(QCoreApplication.translate("Dialog", u"DI\u00c1RIO", None))
        self.radio_weekly.setText(QCoreApplication.translate("Dialog", u"SEMANAL", None))
        self.radio_monthly.setText(QCoreApplication.translate("Dialog", u"MENSAL", None))
#if QT_CONFIG(tooltip)
        self.group_max_backup.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.group_max_backup.setTitle(QCoreApplication.translate("Dialog", u"QUANTIDADE MAX\u00cdMA", None))
        self.radio_3.setText(QCoreApplication.translate("Dialog", u"3", None))
        self.radio_5.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.radio_10.setText(QCoreApplication.translate("Dialog", u"10", None))
    # retranslateUi

