# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

from utils.widget import (CustomComboBox, CustomLineEdit, CustomStackedWidget)
from  . import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(846, 536)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"QWidget {background:rgba(32, 33, 36, 1.000);color:rgba(228, 231, 235,\n"
"                1.000);selection-color:rgba(228, 231, 235, 1.000);selection-background-color:rgba(95, 154, 244,\n"
"                0.400)}QWidget:disabled {color:rgba(228, 231, 235, 0.400);selection-background-color:rgba(228, 231, 235,\n"
"                0.200);selection-color:rgba(228, 231, 235, 0.400)}QWidget:focus\n"
"                {outline:none}QCheckBox:!window,QRadioButton:!window,QPushButton:!window,QLabel:!window,QLCDNumber:!window\n"
"                {background:transparent}QMdiSubWindow > QCheckBox:!window,QMdiSubWindow >\n"
"                QRadioButton:!window,QMdiSubWindow > QPushButton:!window,QMdiSubWindow >\n"
"                QLabel:!window,QMdiSubWindow > QLCDNumber:!window {background:rgba(32, 33, 36,\n"
"                1.000)}QMainWindow::separator {width:4px;height:4px;background:rgba(63, 64, 66,\n"
"                1.000)}QMainWindow::separator:hover,QMainWindow::separator:pressed {background:rgba(138, 180, 247"
                        ",\n"
"                1.000)}QToolTip {background:rgba(42, 43, 47, 1.000);color:rgba(228, 231, 235, 1.000)}QSizeGrip\n"
"                {width:0;height:0;image:none}QStatusBar {background:rgba(42, 43, 46, 1.000)}QStatusBar::item\n"
"                {border:none}QStatusBar QWidget {background:transparent;padding:3px;border-radius:4px}QStatusBar >\n"
"                .QSizeGrip {padding:0}QStatusBar QWidget:hover {background:rgba(255, 255, 255, 0.133)}QStatusBar\n"
"                QWidget:pressed,QStatusBar QWidget:checked {background:rgba(255, 255, 255, 0.204)}QCheckBox,QRadioButton\n"
"                {border-top:2px solid transparent;border-bottom:2px solid transparent}QCheckBox:hover,QRadioButton:hover\n"
"                {border-bottom:2px solid rgba(138, 180, 247, 1.000)}QGroupBox\n"
"                {font-weight:bold;margin-top:8px;padding:2px 1px 1px 1px;border-radius:4px;border:1px solid rgba(63, 64,\n"
"                66, 1.000)}QGroupBox::title {subcontrol-origin:margin;subcontrol-position:top left"
                        ";left:7px;margin:0 2px\n"
"                0 3px}QGroupBox:flat {border-color:transparent}QMenuBar {padding:2px;border-bottom:1px solid rgba(63,\n"
"                64, 66, 1.000);background:rgba(32, 33, 36, 1.000)}QMenuBar::item\n"
"                {background:transparent;padding:4px}QMenuBar::item:selected\n"
"                {padding:4px;border-radius:4px;background:rgba(255, 255, 255, 0.145)}QMenuBar::item:pressed\n"
"                {padding:4px;margin-bottom:0;padding-bottom:0}QToolBar\n"
"                {padding:1px;font-weight:bold;spacing:2px;margin:1px;background:rgba(51, 51, 51,\n"
"                1.000);border-style:none}QToolBar::handle:horizontal\n"
"                {width:20px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/drag_indicator_e1e5e9_0.svg)}QToolBar::handle:vertical\n"
"                {height:20px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/drag_indicator_e1e5e9_90.svg)}QToolBar::handle:horizontal:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2."
                        "1.0/drag_indicator_e4e7eb66_0.svg)}QToolBar::handle:vertical:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/drag_indicator_e4e7eb66_90.svg)}QToolBar::separator\n"
"                {background:rgba(63, 64, 66, 1.000)}QToolBar::separator:horizontal {width:2px;margin:0\n"
"                6px}QToolBar::separator:vertical {height:2px;margin:6px 0}QToolBar > QToolButton\n"
"                {background:transparent;padding:3px;border-radius:4px}QToolBar > QToolButton:hover,QToolBar >\n"
"                QToolButton::menu-button:hover {background:rgba(255, 255, 255, 0.133)}QToolBar >\n"
"                QToolButton::menu-button {border-top-right-radius:4px;border-bottom-right-radius:4px}QToolBar >\n"
"                QToolButton:pressed,QToolBar > QToolButton::menu-button:pressed:enabled,QToolBar >\n"
"                QToolButton:checked:enabled {background:rgba(255, 255, 255, 0.204)}QToolBar > QWidget\n"
"                {background:transparent}QMenu {background:rgba(42, 43, 47, 1.000"
                        ");padding:8px 0; }QMenu::separator\n"
"                {margin:4px 0;height:1px;background:rgba(63, 64, 66, 1.000)}QMenu::item {padding:4px\n"
"                19px}QMenu::item:selected {background:rgba(255, 255, 255, 0.133)}QMenu::icon\n"
"                {padding-left:10px;width:14px;height:14px}QMenu::right-arrow\n"
"                {margin:2px;padding-left:12px;height:20px;width:20px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e1e5e9_0.svg)}QMenu::right-arrow:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb66_0.svg)}QScrollBar\n"
"                {background:rgba(255, 255, 255, 0.063);border-radius:4px;}QScrollBar:horizontal\n"
"                {height:14px;}QScrollBar:vertical {width:14px;}QScrollBar::handle {background:rgba(255, 255, 255,\n"
"                0.188);border-radius:3px}QScrollBar::handle:hover {background:rgba(255, 255, 255,\n"
"                0.271)}QScrollBar::handle:pressed {background:rgba(255, 255, 255, 0.376)}QSc"
                        "rollBar::handle:disabled\n"
"                {background:rgba(255, 255, 255, 0.082)}QScrollBar::handle:horizontal {min-width:8px;margin:4px\n"
"                14px;}QScrollBar::handle:horizontal:hover {margin:2px 14px;}QScrollBar::handle:vertical\n"
"                {min-height:8px;margin:14px 4px;}QScrollBar::handle:vertical:hover {margin:14px\n"
"                2px;}QScrollBar::sub-page,QScrollBar::add-page\n"
"                {background:transparent}QScrollBar::sub-line,QScrollBar::add-line\n"
"                {background:transparent;}QScrollBar::up-arrow:enabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff2f_0.svg)}QScrollBar::right-arrow:enabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff2f_90.svg)}QScrollBar::down-arrow:enabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff2f_180.svg)}QScrollBar::left-arrow:enabled\n"
"                {image:url(C:/Users/Kamua/.cac"
                        "he/qdarktheme/v2.1.0/arrow_drop_up_ffffff2f_270.svg)}QScrollBar::up-arrow:hover\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff5f_0.svg)}QScrollBar::right-arrow:hover\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff5f_90.svg)}QScrollBar::down-arrow:hover\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff5f_180.svg)}QScrollBar::left-arrow:hover\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_ffffff5f_270.svg)}QProgressBar\n"
"                {text-align:center;border:1px solid rgba(63, 64, 66, 1.000);border-radius:4px}QProgressBar::chunk\n"
"                {background:rgba(102, 159, 245, 1.000);border-radius:3px}QProgressBar::chunk:disabled\n"
"                {background:rgba(228, 231, 235, 0.200)}QPushButton {color:rgba(138, 180, 247, 1.000);border:1px solid\n"
"                rgba(63, 64, 66, 1.000);padding:4px 8px;border-radius:4px}QPushButton"
                        ":flat,QPushButton:default\n"
"                {border:none;padding:5px 9px}QPushButton:default {color:rgba(32, 33, 36, 1.000);background:rgba(138,\n"
"                180, 247, 1.000)}QPushButton:hover {background:rgba(102, 159, 245, 0.110)}QPushButton:pressed\n"
"                {background:rgba(87, 150, 244, 0.230)}QPushButton:checked:enabled {background:rgba(87, 150, 244,\n"
"                0.230)}QPushButton:default:hover {background:rgba(117, 168, 246,\n"
"                1.000)}QPushButton:default:pressed,QPushButton:default:checked {background:rgba(95, 154, 244,\n"
"                1.000)}QPushButton:default:disabled,QPushButton:default:checked:disabled {background:rgba(228, 231, 235,\n"
"                0.200)}QDialogButtonBox {dialogbuttonbox-buttons-have-icons:0}QDialogButtonBox QPushButton\n"
"                {min-width:65px}QToolButton\n"
"                {background:transparent;padding:5px;spacing:2px;border-radius:2px}QToolButton:hover,QToolButton::menu-button:hover\n"
"                {backgrou"
                        "nd:rgba(102, 159, 245,\n"
"                0.110)}QToolButton:pressed,QToolButton:checked:pressed,QToolButton::menu-button:pressed:enabled\n"
"                {background:rgba(87, 150, 244, 0.230)}QToolButton:selected:enabled,QToolButton:checked:enabled\n"
"                {background:rgba(87, 150, 244, 0.230)}QToolButton::menu-indicator\n"
"                {height:18px;width:18px;top:6px;left:3px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_180.svg)}QToolButton::menu-indicator:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_180.svg)}QToolButton::menu-arrow\n"
"                {image:unset}QToolButton::menu-button\n"
"                {subcontrol-origin:margin;width:17px;border-top-right-radius:2px;border-bottom-right-radius:2px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_180.svg)}QToolButton::menu-button:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_180.sv"
                        "g)}QToolButton[popupMode=MenuButtonPopup]\n"
"                {padding-right:1px;margin-right:18px;border-top-right-radius:0;border-bottom-right-radius:0}QComboBox\n"
"                {min-height:1.5em;padding:0 8px 0 4px;background:rgba(63, 64, 66, 1.000);border:1px solid rgba(63, 64,\n"
"                66, 1.000);border-radius:4px}QComboBox:focus,QComboBox:open {border-color:rgba(138, 180, 247,\n"
"                1.000)}QComboBox::drop-down {margin:2px 2px 2px -6px;border-radius:4}QComboBox::drop-down:editable:hover\n"
"                {background:rgba(255, 255, 255, 0.145)}QComboBox::down-arrow\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_180.svg)}QComboBox::down-arrow:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_180.svg)}QComboBox::down-arrow:editable:open\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_0.svg)}QComboBox::down-arrow:editable:open:disabled\n"
"     "
                        "           {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_0.svg)}QComboBox::item:selected\n"
"                {border:none;background:rgba(66, 136, 242, 0.400);border-radius:4px}QComboBox\n"
"                QListView[frameShape=NoFrame] {margin:0;padding:4px;background:rgba(42, 43, 47, 1.000); border-radius:0;\n"
"                }QComboBox QListView::item {border-radius:4px}QSlider {padding:2px 0}QSlider::groove\n"
"                {border-radius:2px}QSlider::groove:horizontal {height:4px}QSlider::groove:vertical\n"
"                {width:4px}QSlider::sub-page:horizontal,QSlider::add-page:vertical,QSlider::handle {background:rgba(138,\n"
"                180, 247,\n"
"                1.000)}QSlider::sub-page:horizontal:disabled,QSlider::add-page:vertical:disabled,QSlider::handle:disabled\n"
"                {background:rgba(228, 231, 235, 0.200)}QSlider::add-page:horizontal,QSlider::sub-page:vertical\n"
"                {background:rgba(228, 231, 235, 0.100)}QSlider::handle:hover,QS"
                        "lider::handle:pressed\n"
"                {background:rgba(106, 161, 245, 1.000)}QSlider::handle:horizontal {width:16px;height:8px;margin:-6px\n"
"                0;border-radius:8px}QSlider::handle:vertical {width:8px;height:16px;margin:0\n"
"                -6px;border-radius:8px}QTabWidget::pane {border:1px solid rgba(63, 64, 66,\n"
"                1.000);border-radius:4px}QTabBar {qproperty-drawBase:0}QTabBar::close-button\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/close_e1e5e9_0.svg)}QTabBar::close-button:hover\n"
"                {background:rgba(255, 255, 255, 0.145);border-radius:4px}QTabBar::close-button:!selected\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/close_e4e7eb99_0.svg)}QTabBar::close-button:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/close_e4e7eb66_0.svg)}QTabBar::tab\n"
"                {padding:3px;border-style:solid}QTabBar::tab:hover,QTabBar::tab:selected:hover:enabled\n"
"                {backgro"
                        "und:rgba(255, 255, 255, 0.094)}QTabBar::tab:selected:enabled {color:rgba(138, 180, 247,\n"
"                1.000);background:rgba(255, 255, 255, 0.000);border-color:rgba(138, 180, 247,\n"
"                1.000)}QTabBar::tab:selected:disabled,QTabBar::tab:only-one:selected:enabled {border-color:rgba(63, 64,\n"
"                66, 1.000)}QTabBar::tab:top {border-bottom-width:2px;margin:3px 6px 0\n"
"                0;border-top-left-radius:2px;border-top-right-radius:2px}QTabBar::tab:bottom\n"
"                {border-top-width:2px;margin:0 6px 3px\n"
"                0;border-bottom-left-radius:2px;border-bottom-right-radius:2px}QTabBar::tab:left\n"
"                {border-right-width:2px;margin:0 0 6px\n"
"                3px;border-top-left-radius:2px;border-bottom-left-radius:2px}QTabBar::tab:right\n"
"                {border-left-width:2px;margin-bottom:6px;margin:0 3px 6px\n"
"                0;border-top-right-radius:2px;border-bottom-right-radius:2px}QTabBar::tab:top:first,QTabBar::tab:top:only-one,Q"
                        "TabBar::tab:bottom:first,QTabBar::tab:bottom:only-one\n"
"                {margin-left:2px}QTabBar::tab:top:last,QTabBar::tab:top:only-one,QTabBar::tab:bottom:last,QTabBar::tab:bottom:only-one\n"
"                {margin-right:2px}QTabBar::tab:left:first,QTabBar::tab:left:only-one,QTabBar::tab:right:first,QTabBar::tab:right:only-one\n"
"                {margin-top:2px}QTabBar::tab:left:last,QTabBar::tab:left:only-one,QTabBar::tab:right:last,QTabBar::tab:right:only-one\n"
"                {margin-bottom:2px}QDockWidget {border:1px solid rgba(63, 64, 66,\n"
"                1.000);border-radius:4px}QDockWidget::title {padding:3px;spacing:4px;background:rgba(22, 23, 25,\n"
"                1.000)}QDockWidget::close-button,QDockWidget::float-button\n"
"                {border-radius:2px}QDockWidget::close-button:hover,QDockWidget::float-button:hover {background:rgba(102,\n"
"                159, 245, 0.110)}QDockWidget::close-button:pressed,QDockWidget::float-button:pressed\n"
"                {background:rgba(87,"
                        " 150, 244, 0.230)}QFrame {border:1px solid rgba(63, 64, 66,\n"
"                1.000);padding:1px;border-radius:4px}.QFrame {padding:0}QFrame[frameShape=NoFrame]\n"
"                {border-color:transparent;padding:0}.QFrame[frameShape=NoFrame] {border:none}QFrame[frameShape=Panel]\n"
"                {border-color:rgba(22, 23, 25, 1.000);background:rgba(22, 23, 25, 1.000)}QFrame[frameShape=HLine]\n"
"                {max-height:2px;border:none;background:rgba(63, 64, 66, 1.000)}QFrame[frameShape=VLine]\n"
"                {max-width:2px;border:none;background:rgba(63, 64, 66, 1.000)}QLCDNumber\n"
"                {min-width:2em;margin:2px}QToolBox::tab {background:rgba(22, 23, 25, 1.000);border-bottom:2px solid\n"
"                rgba(63, 64, 66,\n"
"                1.000);border-top-left-radius:4px;border-top-right-radius:4px}QToolBox::tab:selected:enabled\n"
"                {border-bottom-color:rgba(138, 180, 247, 1.000)}QSplitter::handle {background:rgba(63, 64, 66,\n"
"                1.000);margin:1p"
                        "x 3px}QSplitter::handle:hover {background:rgba(138, 180, 247,\n"
"                1.000)}QSplitter::handle:horizontal\n"
"                {width:5px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/horizontal_rule_e1e5e9_90.svg)}QSplitter::handle:horizontal:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/horizontal_rule_e4e7eb66_90.svg)}QSplitter::handle:vertical\n"
"                {height:5px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/horizontal_rule_e1e5e9_0.svg)}QSplitter::handle:vertical:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/horizontal_rule_e4e7eb66_0.svg)}QSplitterHandle::item:hover\n"
"                {}QAbstractScrollArea {margin:1px}QAbstractScrollArea::corner\n"
"                {background:transparent}QAbstractScrollArea > .QWidget {background:transparent}QAbstractScrollArea\n"
"                > .QWidget > .QWidget {background:transparent}QMdiArea {qproperty-background:rgba(22, 23, 25,\n"
"                1.000);borde"
                        "r-radius:0}QMdiSubWindow {background:rgba(32, 33, 36, 1.000);border:1px solid;padding:0\n"
"                3px}QMdiSubWindow > QWidget {border:1px solid rgba(63, 64, 66, 1.000)}QTextEdit, QPlainTextEdit\n"
"                {background:rgba(28, 29, 31,\n"
"                1.000)}QTextEdit:focus,QTextEdit:selected,QPlainTextEdit:focus,QPlainTextEdit:selected {border:1px solid\n"
"                rgba(138, 180, 247, 1.000);selection-background-color:rgba(95, 154, 244,\n"
"                0.400)}QTextEdit:!focus,QPlainTextEdit:!focus { selection-background-color:rgba(255, 255, 255,\n"
"                0.125)}QTextEdit:!active,QPlainTextEdit:!active { }QAbstractItemView\n"
"                {padding:0;alternate-background-color:transparent;selection-background-color:transparent}QAbstractItemView:disabled\n"
"                {selection-background-color:transparent}QAbstractItemView::item:alternate,QAbstractItemView::branch:alternate\n"
"                {background:rgba(255, 255, 255,\n"
"                0.047)}QAbst"
                        "ractItemView::item:selected,QAbstractItemView::branch:selected {background:rgba(66, 136,\n"
"                242, 0.400)}QAbstractItemView::item:selected:!active,QAbstractItemView::branch:selected:!active\n"
"                {background:rgba(210, 227, 252, 0.150)}QAbstractItemView QLineEdit,QAbstractItemView\n"
"                QAbstractSpinBox,QAbstractItemView QAbstractButton {padding:0;margin:1px}QListView\n"
"                {padding:1px}QListView,QTreeView {background:rgba(32, 33, 36,\n"
"                1.000)}QListView::item:!selected:hover,QTreeView::item:!selected:hover,QTreeView::branch:!selected:hover\n"
"                {background:rgba(255, 255, 255,\n"
"                0.075)}QTreeView::branch:!selected:hover,QTreeView::branch:alternate,QTreeView::branch:selected,QTreeView::branch:selected:!active\n"
"                { background:transparent;}QTreeView::branch\n"
"                {border-image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/vertical_line_ffffff35_0.svg)\n"
"                0}QTreeVie"
                        "w::branch:active\n"
"                {border-image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/vertical_line_ffffff5f_0.svg)\n"
"                0}QTreeView::branch:has-siblings:adjoins-item,QTreeView::branch:!has-children:!has-siblings:adjoins-item\n"
"                {border-image:unset}QTreeView::branch:has-children:!has-siblings:closed,QTreeView::branch:closed:has-children:has-siblings\n"
"                {border-image:unset;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e1e5e9_0.svg)}QTreeView::branch:has-children:!has-siblings:closed:disabled,QTreeView::branch:closed:has-children:has-siblings:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb66_0.svg)}QTreeView::branch:open:has-children:!has-siblings,QTreeView::branch:open:has-children:has-siblings\n"
"                {border-image:unset;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_180.svg)}QTreeView::branch:open:has-children:!has-siblings:disabled,QTreeView::branc"
                        "h:open:has-children:has-siblings:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_180.svg)}QTreeView >\n"
"                QHeaderView {background:rgba(32, 33, 36, 1.000)}QTreeView > QHeaderView::section {background:rgba(63,\n"
"                64, 66, 1.000)}QListView::left-arrow\n"
"                {margin:-2px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb99_180.svg)}QListView::right-arrow\n"
"                {margin:-2px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb99_0.svg)}QListView::left-arrow:selected:enabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e1e5e9_180.svg)}QListView::right-arrow:selected:enabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e1e5e9_0.svg)}QListView::left-arrow:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb66_180.svg)}QListView::right-arrow:disa"
                        "bled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/chevron_right_e4e7eb66_0.svg)}QColumnView\n"
"                {background:rgba(32, 33, 36, 1.000)}QColumnViewGrip {margin:-4px;background:rgba(32, 33, 36,\n"
"                1.000);image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/drag_handle_e1e5e9_90.svg)}QColumnViewGrip:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/drag_handle_e4e7eb66_90.svg)}QTableView\n"
"                {gridline-color:rgba(63, 64, 66, 1.000);background:rgba(16, 16, 18,\n"
"                1.000);selection-background-color:rgba(66, 136, 242, 0.550); alternate-background-color:rgba(255, 255,\n"
"                255, 0.082);}QTableView:!active { }QTableView::item:alternate { }QTableView::item:selected { }QTableView\n"
"                QTableCornerButton::section {margin:0 1px 1px 0;background:rgba(63, 64, 66,\n"
"                1.000);border-top-left-radius:2px}QTableView QTableCornerButton::section:pressed {background:rgba(66,\n"
""
                        "                136, 242, 0.550)}QTableView > QHeaderView {background:rgba(16, 16, 18,\n"
"                1.000);border-radius:3}QTableView > QHeaderView::section {background:rgba(63, 64, 66,\n"
"                1.000)}QHeaderView {margin:0;border:none}QHeaderView::section {border:none;background:rgba(63, 64, 66,\n"
"                1.000);padding-left:4px}QHeaderView::section:horizontal {margin-right:1px}QHeaderView::section:vertical\n"
"                {margin-bottom:1px}QHeaderView::section:on:enabled,QHeaderView::section:on:pressed {color:rgba(138, 180,\n"
"                247, 1.000)}QHeaderView::section:last,QHeaderView::section:only-one\n"
"                {margin:0}QHeaderView::down-arrow:horizontal {margin-left:-19px;subcontrol-position:center\n"
"                right;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_180.svg)}QHeaderView::down-arrow:horizontal:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_180.svg)}QHeaderView:"
                        ":up-arrow:horizontal\n"
"                {margin-left:-19px;subcontrol-position:center\n"
"                right;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e1e5e9_0.svg)}QHeaderView::up-arrow:horizontal:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/expand_less_e4e7eb66_0.svg)}QHeaderView::down-arrow:vertical,QHeaderView::up-arrow:vertical\n"
"                {width:0;height:0}QCalendarWidget > .QWidget {background:rgba(16, 16, 18, 1.000);border-bottom:1px\n"
"                solid rgba(63, 64, 66, 1.000);border-top-left-radius:4px;border-top-right-radius:4px}QCalendarWidget\n"
"                > .QWidget > QWidget {padding:1px}QCalendarWidget .QWidget > QToolButton\n"
"                {border-radius:4px}QCalendarWidget > QTableView\n"
"                {margin:0;border:none;border-radius:4px;border-top-left-radius:0;border-top-right-radius:0;alternate-background-color:rgba(255,\n"
"                255, 255, 0.082); }QLineEdit,QAbstractSpinBox {padding:3px 4px"
                        ";min-height:1em;border:1px solid rgba(63,\n"
"                64, 66, 1.000);background:rgba(63, 64, 66,\n"
"                1.000);border-radius:4px}QLineEdit:focus,QAbstractSpinBox:focus {border-color:rgba(138, 180, 247,\n"
"                1.000)}QAbstractSpinBox::up-button,QAbstractSpinBox::down-button {subcontrol-position:center\n"
"                right;border-radius:4px}QAbstractSpinBox::up-button:hover:on,QAbstractSpinBox::down-button:hover:on\n"
"                {background:rgba(255, 255, 255, 0.145)}QAbstractSpinBox::up-button\n"
"                {bottom:5px;right:4px}QAbstractSpinBox::up-arrow:on\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_e1e5e9_0.svg)}QAbstractSpinBox::up-arrow:disabled,QAbstractSpinBox::up-arrow:off\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_e4e7eb66_0.svg)}QAbstractSpinBox::down-button\n"
"                {top:5px;right:4px}QAbstractSpinBox::down-arrow:on\n"
"                {image:url(C:/Users/Ka"
                        "mua/.cache/qdarktheme/v2.1.0/arrow_drop_up_e1e5e9_180.svg)}QAbstractSpinBox::down-arrow:disabled,QAbstractSpinBox::down-arrow:off\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/arrow_drop_up_e4e7eb66_180.svg)}QDateTimeEdit::drop-down\n"
"                {padding-right:4px;width:16px;image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/calendar_today_e1e5e9_0.svg)}QDateTimeEdit::drop-down:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/calendar_today_e4e7eb66_0.svg)}QDateTimeEdit::down-arrow[calendarPopup=true]\n"
"                {image:none}QFileDialog QFrame {border:none}QFontDialog QListView\n"
"                {min-height:60px}QComboBox::indicator,QMenu::indicator {width:18px;height:18px}QMenu::indicator\n"
"                {background:rgba(255, 255, 255,\n"
"                0.098);margin-left:3px;border-radius:4px}QComboBox::indicator:checked,QMenu::indicator:checked\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/check_e1e5e9_0.s"
                        "vg)}QCheckBox,QRadioButton\n"
"                {spacing:8px}QGroupBox::title,QAbstractItemView::item\n"
"                {spacing:6px}QCheckBox::indicator,QGroupBox::indicator,QAbstractItemView::indicator,QRadioButton::indicator\n"
"                {height:18px;width:18px}QCheckBox::indicator,QGroupBox::indicator,QAbstractItemView::indicator\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/check_box_outline_blank_e1e5e9_0.svg)}QCheckBox::indicator:unchecked:disabled,QGroupBox::indicator:unchecked:disabled,QAbstractItemView::indicator:unchecked:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/check_box_outline_blank_e4e7eb66_0.svg)}QCheckBox::indicator:checked,QGroupBox::indicator:checked,QAbstractItemView::indicator:checked\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/check_box_8ab4f7_0.svg)}QCheckBox::indicator:checked:disabled,QGroupBox::indicator:checked:disabled,QAbstractItemView::indicator:checked:disabled\n"
"                {"
                        "image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/check_box_e4e7eb66_0.svg)}QCheckBox::indicator:indeterminate,QAbstractItemView::indicator:indeterminate\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/indeterminate_check_box_8ab4f7_0.svg)}QCheckBox::indicator:indeterminate:disabled,QAbstractItemView::indicator:indeterminate:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/indeterminate_check_box_e4e7eb66_0.svg)}QRadioButton::indicator:unchecked\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/radio_button_unchecked_e1e5e9_0.svg)}QRadioButton::indicator:unchecked:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/radio_button_unchecked_e4e7eb66_0.svg)}QRadioButton::indicator:checked\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/radio_button_checked_8ab4f7_0.svg)}QRadioButton::indicator:checked:disabled\n"
"                {image:url(C:/Users/Kamua/.cache/qdarktheme/v2.1.0/radio_butt"
                        "on_checked_e4e7eb66_0.svg)}PlotWidget\n"
"                {padding:0}ParameterTree > .QWidget > .QWidget > .QWidget >\n"
"                QComboBox{min-height:1.2em}ParameterTree::item,ParameterTree > .QWidget {background:rgba(32, 33, 36,\n"
"                1.000)}\n"
"            ")
        MainWindow.setAnimated(True)
        self.action_suppliers = QAction(MainWindow)
        self.action_suppliers.setObjectName(u"action_suppliers")
        icon = QIcon()
        icon.addFile(u":/icons/assets/supplier-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_suppliers.setIcon(icon)
        self.actionBackup = QAction(MainWindow)
        self.actionBackup.setObjectName(u"actionBackup")
        self.action_years = QAction(MainWindow)
        self.action_years.setObjectName(u"action_years")
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/data-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_years.setIcon(icon1)
        self.action_config = QAction(MainWindow)
        self.action_config.setObjectName(u"action_config")
        icon2 = QIcon()
        icon2.addFile(u":/icons/assets/db-config-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_config.setIcon(icon2)
        self.action_dark_theme = QAction(MainWindow)
        self.action_dark_theme.setObjectName(u"action_dark_theme")
        icon3 = QIcon()
        icon3.addFile(u":/icons/assets/dark-mode-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_dark_theme.setIcon(icon3)
        self.action_light_theme = QAction(MainWindow)
        self.action_light_theme.setObjectName(u"action_light_theme")
        icon4 = QIcon()
        icon4.addFile(u":/icons/assets/light-mode-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_light_theme.setIcon(icon4)
        self.action_import_backup = QAction(MainWindow)
        self.action_import_backup.setObjectName(u"action_import_backup")
        icon5 = QIcon()
        icon5.addFile(u":/icons/assets/backup-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_import_backup.setIcon(icon5)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mp_main = CustomStackedWidget(self.centralwidget)
        self.mp_main.setObjectName(u"mp_main")
        sizePolicy.setHeightForWidth(self.mp_main.sizePolicy().hasHeightForWidth())
        self.mp_main.setSizePolicy(sizePolicy)
        self.mp_main.setLayoutDirection(Qt.LeftToRight)
        self.mp_main.setFrameShape(QFrame.Box)
        self.mp_main.setFrameShadow(QFrame.Raised)
        self.pg_register = QWidget()
        self.pg_register.setObjectName(u"pg_register")
        self.gridLayout_2 = QGridLayout(self.pg_register)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.bt_new = QPushButton(self.pg_register)
        self.bt_new.setObjectName(u"bt_new")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bt_new.sizePolicy().hasHeightForWidth())
        self.bt_new.setSizePolicy(sizePolicy1)
        self.bt_new.setMinimumSize(QSize(70, 70))
        self.bt_new.setCursor(QCursor(Qt.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(u":/icons/assets/new-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_new.setIcon(icon6)
        self.bt_new.setIconSize(QSize(48, 48))

        self.horizontalLayout_2.addWidget(self.bt_new)

        self.bt_save = QPushButton(self.pg_register)
        self.bt_save.setObjectName(u"bt_save")
        sizePolicy1.setHeightForWidth(self.bt_save.sizePolicy().hasHeightForWidth())
        self.bt_save.setSizePolicy(sizePolicy1)
        self.bt_save.setMinimumSize(QSize(70, 70))
        self.bt_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_save.setLayoutDirection(Qt.LeftToRight)
        icon7 = QIcon()
        icon7.addFile(u":/icons/assets/save-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_save.setIcon(icon7)
        self.bt_save.setIconSize(QSize(48, 48))

        self.horizontalLayout_2.addWidget(self.bt_save)

        self.bt_delete = QPushButton(self.pg_register)
        self.bt_delete.setObjectName(u"bt_delete")
        sizePolicy1.setHeightForWidth(self.bt_delete.sizePolicy().hasHeightForWidth())
        self.bt_delete.setSizePolicy(sizePolicy1)
        self.bt_delete.setMinimumSize(QSize(70, 70))
        self.bt_delete.setCursor(QCursor(Qt.PointingHandCursor))
        icon8 = QIcon()
        icon8.addFile(u":/icons/assets/delete-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_delete.setIcon(icon8)
        self.bt_delete.setIconSize(QSize(48, 48))

        self.horizontalLayout_2.addWidget(self.bt_delete)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 2, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 5, 2, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setVerticalSpacing(40)
        self.gridLayout_3.setContentsMargins(5, 20, 5, 20)
        self.txt_nfe = QLineEdit(self.pg_register)
        self.txt_nfe.setObjectName(u"txt_nfe")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.txt_nfe.sizePolicy().hasHeightForWidth())
        self.txt_nfe.setSizePolicy(sizePolicy2)
        self.txt_nfe.setMinimumSize(QSize(225, 24))
        self.txt_nfe.setAlignment(Qt.AlignCenter)
        self.txt_nfe.setClearButtonEnabled(False)

        self.gridLayout_3.addWidget(self.txt_nfe, 0, 2, 1, 1)

        self.label = QLabel(self.pg_register)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)

        self.txt_value = CustomLineEdit(self.pg_register)
        self.txt_value.setObjectName(u"txt_value")
        self.txt_value.setAlignment(Qt.AlignCenter)
        self.txt_value.setClearButtonEnabled(False)

        self.gridLayout_3.addWidget(self.txt_value, 5, 2, 1, 1)

        self.label_5 = QLabel(self.pg_register)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 4, 1, 1, 1)

        self.cb_supplier = QComboBox(self.pg_register)
        self.cb_supplier.setObjectName(u"cb_supplier")
        self.cb_supplier.setEditable(True)
        self.cb_supplier.setFrame(True)

        self.gridLayout_3.addWidget(self.cb_supplier, 4, 2, 1, 1)

        self.label_2 = QLabel(self.pg_register)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_3 = QLabel(self.pg_register)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 5, 1, 1, 1)

        self.cb_date = CustomComboBox(self.pg_register)
        self.cb_date.setObjectName(u"cb_date")
        self.cb_date.setEditable(True)

        self.gridLayout_3.addWidget(self.cb_date, 2, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 4, 1, 1)

        self.mp_main.addWidget(self.pg_register)
        self.pg_search = QWidget()
        self.pg_search.setObjectName(u"pg_search")
        self.gridLayout_5 = QGridLayout(self.pg_search)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(15, 15, 15, 15)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(8)
        self.gridLayout_4.setVerticalSpacing(6)
        self.gridLayout_4.setContentsMargins(-1, -1, 10, -1)
        self.txt_supplier_search = QLineEdit(self.pg_search)
        self.txt_supplier_search.setObjectName(u"txt_supplier_search")
        self.txt_supplier_search.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.txt_supplier_search, 1, 1, 1, 1)

        self.label_4 = QLabel(self.pg_search)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_6 = QLabel(self.pg_search)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)

        self.txt_nfe_search = QLineEdit(self.pg_search)
        self.txt_nfe_search.setObjectName(u"txt_nfe_search")
        self.txt_nfe_search.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.txt_nfe_search, 0, 1, 1, 1)

        self.label_8 = QLabel(self.pg_search)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 2, 1, 1)

        self.label_7 = QLabel(self.pg_search)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 0, 2, 1, 1)

        self.cb_start_date = CustomComboBox(self.pg_search)
        self.cb_start_date.setObjectName(u"cb_start_date")
        self.cb_start_date.setEditable(True)

        self.gridLayout_4.addWidget(self.cb_start_date, 0, 3, 1, 1)

        self.cb_end_date = CustomComboBox(self.pg_search)
        self.cb_end_date.setObjectName(u"cb_end_date")
        self.cb_end_date.setEditable(True)

        self.gridLayout_4.addWidget(self.cb_end_date, 1, 3, 1, 1)

        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_4.setColumnStretch(3, 1)

        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, 4, -1, 4)
        self.bt_clear_search = QPushButton(self.pg_search)
        self.bt_clear_search.setObjectName(u"bt_clear_search")
        sizePolicy1.setHeightForWidth(self.bt_clear_search.sizePolicy().hasHeightForWidth())
        self.bt_clear_search.setSizePolicy(sizePolicy1)
        self.bt_clear_search.setMinimumSize(QSize(40, 40))
        self.bt_clear_search.setCursor(QCursor(Qt.PointingHandCursor))
        icon9 = QIcon()
        icon9.addFile(u":/icons/assets/erase-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_clear_search.setIcon(icon9)
        self.bt_clear_search.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.bt_clear_search)

        self.bt_search = QPushButton(self.pg_search)
        self.bt_search.setObjectName(u"bt_search")
        sizePolicy1.setHeightForWidth(self.bt_search.sizePolicy().hasHeightForWidth())
        self.bt_search.setSizePolicy(sizePolicy1)
        self.bt_search.setMinimumSize(QSize(40, 40))
        self.bt_search.setCursor(QCursor(Qt.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(u":/icons/assets/search-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_search.setIcon(icon10)
        self.bt_search.setIconSize(QSize(32, 32))
        self.bt_search.setFlat(False)

        self.verticalLayout.addWidget(self.bt_search)


        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.table_search = QTableView(self.pg_search)
        self.table_search.setObjectName(u"table_search")
        self.table_search.setAlternatingRowColors(True)
        self.table_search.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_5.addWidget(self.table_search, 2, 0, 1, 2)

        self.mp_main.addWidget(self.pg_search)
        self.pg_export = QWidget()
        self.pg_export.setObjectName(u"pg_export")
        self.gridLayout_7 = QGridLayout(self.pg_export)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(15, 15, 15, 15)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_6.setHorizontalSpacing(15)
        self.gridLayout_6.setVerticalSpacing(20)
        self.gridLayout_6.setContentsMargins(5, 20, 5, 60)
        self.label_10 = QLabel(self.pg_export)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_6.addWidget(self.label_10, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.bt_pdf = QPushButton(self.pg_export)
        self.bt_pdf.setObjectName(u"bt_pdf")
        sizePolicy1.setHeightForWidth(self.bt_pdf.sizePolicy().hasHeightForWidth())
        self.bt_pdf.setSizePolicy(sizePolicy1)
        self.bt_pdf.setMinimumSize(QSize(80, 80))
        self.bt_pdf.setCursor(QCursor(Qt.PointingHandCursor))
        icon11 = QIcon()
        icon11.addFile(u":/icons/assets/pdf-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_pdf.setIcon(icon11)
        self.bt_pdf.setIconSize(QSize(48, 48))

        self.horizontalLayout_3.addWidget(self.bt_pdf)

        self.bt_print = QPushButton(self.pg_export)
        self.bt_print.setObjectName(u"bt_print")
        sizePolicy1.setHeightForWidth(self.bt_print.sizePolicy().hasHeightForWidth())
        self.bt_print.setSizePolicy(sizePolicy1)
        self.bt_print.setMinimumSize(QSize(80, 80))
        self.bt_print.setCursor(QCursor(Qt.PointingHandCursor))
        icon12 = QIcon()
        icon12.addFile(u":/icons/assets/print-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_print.setIcon(icon12)
        self.bt_print.setIconSize(QSize(48, 48))

        self.horizontalLayout_3.addWidget(self.bt_print)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.gridLayout_6.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)

        self.label_9 = QLabel(self.pg_export)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.cb_year = QComboBox(self.pg_export)
        self.cb_year.setObjectName(u"cb_year")
        sizePolicy2.setHeightForWidth(self.cb_year.sizePolicy().hasHeightForWidth())
        self.cb_year.setSizePolicy(sizePolicy2)
        self.cb_year.setAutoFillBackground(False)
        self.cb_year.setStyleSheet(u"")
        self.cb_year.setEditable(False)

        self.gridLayout_6.addWidget(self.cb_year, 0, 1, 1, 1)

        self.cb_month = QComboBox(self.pg_export)
        self.cb_month.setObjectName(u"cb_month")
        sizePolicy2.setHeightForWidth(self.cb_month.sizePolicy().hasHeightForWidth())
        self.cb_month.setSizePolicy(sizePolicy2)
        self.cb_month.setAutoFillBackground(False)
        self.cb_month.setStyleSheet(u"")
        self.cb_month.setEditable(False)

        self.gridLayout_6.addWidget(self.cb_month, 1, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 3, 1, 1)

        self.web_container = QWidget(self.pg_export)
        self.web_container.setObjectName(u"web_container")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.web_container.sizePolicy().hasHeightForWidth())
        self.web_container.setSizePolicy(sizePolicy3)
        self.web_container.setMinimumSize(QSize(0, 0))
        self.web_container.setStyleSheet(u"border:1px solid gray;")
        self.horizontalLayout_4 = QHBoxLayout(self.web_container)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.web_view = QWebEngineView(self.web_container)
        self.web_view.setObjectName(u"web_view")
        sizePolicy3.setHeightForWidth(self.web_view.sizePolicy().hasHeightForWidth())
        self.web_view.setSizePolicy(sizePolicy3)
        self.web_view.setMinimumSize(QSize(500, 0))
        self.web_view.setStyleSheet(u"border:1px solid black;")

        self.horizontalLayout_4.addWidget(self.web_view)


        self.gridLayout_7.addWidget(self.web_container, 0, 0, 1, 1)

        self.mp_main.addWidget(self.pg_export)

        self.gridLayout.addWidget(self.mp_main, 2, 0, 1, 1)

        self.fr_header = QFrame(self.centralwidget)
        self.fr_header.setObjectName(u"fr_header")
        sizePolicy.setHeightForWidth(self.fr_header.sizePolicy().hasHeightForWidth())
        self.fr_header.setSizePolicy(sizePolicy)
        self.fr_header.setMinimumSize(QSize(0, 100))
        self.fr_header.setSizeIncrement(QSize(0, 0))
        self.fr_header.setFrameShape(QFrame.Box)
        self.fr_header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.fr_header)
        self.horizontalLayout.setSpacing(31)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bt_register_menu = QPushButton(self.fr_header)
        self.bt_register_menu.setObjectName(u"bt_register_menu")
        self.bt_register_menu.setMinimumSize(QSize(0, 50))
        self.bt_register_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_register_menu.setLayoutDirection(Qt.LeftToRight)
        icon13 = QIcon()
        icon13.addFile(u":/icons/assets/registry-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_register_menu.setIcon(icon13)
        self.bt_register_menu.setIconSize(QSize(48, 48))

        self.horizontalLayout.addWidget(self.bt_register_menu)

        self.bt_search_menu = QPushButton(self.fr_header)
        self.bt_search_menu.setObjectName(u"bt_search_menu")
        self.bt_search_menu.setMinimumSize(QSize(0, 50))
        self.bt_search_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.bt_search_menu.setIcon(icon10)
        self.bt_search_menu.setIconSize(QSize(48, 48))

        self.horizontalLayout.addWidget(self.bt_search_menu)

        self.bt_export_menu = QPushButton(self.fr_header)
        self.bt_export_menu.setObjectName(u"bt_export_menu")
        self.bt_export_menu.setMinimumSize(QSize(0, 50))
        self.bt_export_menu.setCursor(QCursor(Qt.PointingHandCursor))
        icon14 = QIcon()
        icon14.addFile(u":/icons/assets/export-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_export_menu.setIcon(icon14)
        self.bt_export_menu.setIconSize(QSize(48, 48))

        self.horizontalLayout.addWidget(self.bt_export_menu)


        self.gridLayout.addWidget(self.fr_header, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 846, 29))
        self.menu_config = QMenu(self.menubar)
        self.menu_config.setObjectName(u"menu_config")
        self.menu_config.setTearOffEnabled(False)
        self.menu_config.setSeparatorsCollapsible(False)
        self.menu_config.setToolTipsVisible(False)
        self.menu_db = QMenu(self.menu_config)
        self.menu_db.setObjectName(u"menu_db")
        icon15 = QIcon()
        icon15.addFile(u":/icons/assets/db.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_db.setIcon(icon15)
        self.menu_theme = QMenu(self.menu_config)
        self.menu_theme.setObjectName(u"menu_theme")
        sizePolicy.setHeightForWidth(self.menu_theme.sizePolicy().hasHeightForWidth())
        self.menu_theme.setSizePolicy(sizePolicy)
        icon16 = QIcon()
        icon16.addFile(u":/icons/assets/themes-32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_theme.setIcon(icon16)
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.txt_nfe)
        self.label_5.setBuddy(self.cb_supplier)
        self.label_3.setBuddy(self.txt_value)
        self.label_4.setBuddy(self.txt_nfe_search)
        self.label_6.setBuddy(self.txt_supplier_search)
        self.label_10.setBuddy(self.cb_year)
        self.label_9.setBuddy(self.cb_month)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.bt_register_menu, self.bt_search_menu)
        QWidget.setTabOrder(self.bt_search_menu, self.bt_export_menu)
        QWidget.setTabOrder(self.bt_export_menu, self.txt_nfe)
        QWidget.setTabOrder(self.txt_nfe, self.cb_date)
        QWidget.setTabOrder(self.cb_date, self.cb_supplier)
        QWidget.setTabOrder(self.cb_supplier, self.txt_value)
        QWidget.setTabOrder(self.txt_value, self.bt_save)
        QWidget.setTabOrder(self.bt_save, self.bt_delete)
        QWidget.setTabOrder(self.bt_delete, self.txt_nfe_search)
        QWidget.setTabOrder(self.txt_nfe_search, self.txt_supplier_search)
        QWidget.setTabOrder(self.txt_supplier_search, self.cb_start_date)
        QWidget.setTabOrder(self.cb_start_date, self.cb_end_date)
        QWidget.setTabOrder(self.cb_end_date, self.bt_clear_search)
        QWidget.setTabOrder(self.bt_clear_search, self.bt_search)
        QWidget.setTabOrder(self.bt_search, self.table_search)
        QWidget.setTabOrder(self.table_search, self.cb_year)
        QWidget.setTabOrder(self.cb_year, self.cb_month)
        QWidget.setTabOrder(self.cb_month, self.bt_pdf)
        QWidget.setTabOrder(self.bt_pdf, self.bt_print)

        self.menubar.addAction(self.menu_config.menuAction())
        self.menu_config.addAction(self.menu_db.menuAction())
        self.menu_config.addSeparator()
        self.menu_config.addAction(self.action_years)
        self.menu_config.addAction(self.action_suppliers)
        self.menu_config.addSeparator()
        self.menu_config.addAction(self.menu_theme.menuAction())
        self.menu_db.addAction(self.action_config)
        self.menu_db.addAction(self.action_import_backup)
        self.menu_theme.addAction(self.action_dark_theme)
        self.menu_theme.addAction(self.action_light_theme)

        self.retranslateUi(MainWindow)

        self.mp_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_suppliers.setText(QCoreApplication.translate("MainWindow", u"Fornecedores", None))
        self.actionBackup.setText(QCoreApplication.translate("MainWindow", u"Backup", None))
        self.action_years.setText(QCoreApplication.translate("MainWindow", u"Anos", None))
        self.action_config.setText(QCoreApplication.translate("MainWindow", u"Configurar", None))
        self.action_dark_theme.setText(QCoreApplication.translate("MainWindow", u"Dark", None))
        self.action_light_theme.setText(QCoreApplication.translate("MainWindow", u"Light", None))
        self.action_import_backup.setText(QCoreApplication.translate("MainWindow", u"Importar Backup", None))
#if QT_CONFIG(tooltip)
        self.bt_new.setToolTip(QCoreApplication.translate("MainWindow", u"NOVO", None))
#endif // QT_CONFIG(tooltip)
        self.bt_new.setText("")
#if QT_CONFIG(shortcut)
        self.bt_new.setShortcut("")
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.bt_save.setToolTip(QCoreApplication.translate("MainWindow", u"SALVAR", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.bt_save.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.bt_save.setText("")
#if QT_CONFIG(tooltip)
        self.bt_delete.setToolTip(QCoreApplication.translate("MainWindow", u"DELETAR", None))
#endif // QT_CONFIG(tooltip)
        self.bt_delete.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"NFE", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"FORNECEDOR", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"VALOR", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"NFE", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"FORNECEDOR", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"DATA FINAL", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"DATA INICIAL", None))
#if QT_CONFIG(tooltip)
        self.bt_clear_search.setToolTip(QCoreApplication.translate("MainWindow", u"LIMPAR", None))
#endif // QT_CONFIG(tooltip)
        self.bt_clear_search.setText("")
#if QT_CONFIG(tooltip)
        self.bt_search.setToolTip(QCoreApplication.translate("MainWindow", u"PESQUISAR", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.bt_search.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.bt_search.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"ANO", None))
#if QT_CONFIG(tooltip)
        self.bt_pdf.setToolTip(QCoreApplication.translate("MainWindow", u"EXPORTAR PDF", None))
#endif // QT_CONFIG(tooltip)
        self.bt_pdf.setText("")
#if QT_CONFIG(tooltip)
        self.bt_print.setToolTip(QCoreApplication.translate("MainWindow", u"IMPRIMIR", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.bt_print.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.bt_print.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"M\u00caS", None))
        self.bt_register_menu.setText(QCoreApplication.translate("MainWindow", u"REGISTRAR", None))
        self.bt_search_menu.setText(QCoreApplication.translate("MainWindow", u"PESQUISAR", None))
        self.bt_export_menu.setText(QCoreApplication.translate("MainWindow", u"EXPORTAR", None))
        self.menu_config.setTitle(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00f5es", None))
        self.menu_db.setTitle(QCoreApplication.translate("MainWindow", u"Banco de dados", None))
        self.menu_theme.setTitle(QCoreApplication.translate("MainWindow", u"Tema", None))
    # retranslateUi

