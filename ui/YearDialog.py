# Form implementation generated from reading ui file '.\ui\YearDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(181, 107)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.cb_years = QtWidgets.QComboBox(parent=Dialog)
        self.cb_years.setObjectName("cb_years")
        self.gridLayout.addWidget(self.cb_years, 0, 3, 1, 1)
        self.bt_delete = QtWidgets.QPushButton(parent=Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\ui\\../assets/delete-48.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.bt_delete.setIcon(icon)
        self.bt_delete.setIconSize(QtCore.QSize(32, 32))
        self.bt_delete.setObjectName("bt_delete")
        self.gridLayout.addWidget(self.bt_delete, 1, 2, 1, 2)
        self.label.setBuddy(self.cb_years)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Anos"))
        self.label.setText(_translate("Dialog", "ANO"))
        self.bt_delete.setText(_translate("Dialog", "DELETAR"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())