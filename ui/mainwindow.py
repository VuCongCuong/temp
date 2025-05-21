# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowAHfnKt.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QProgressBar, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(867, 624)
        self.actionLoad_mesh = QAction(MainWindow)
        self.actionLoad_mesh.setObjectName(u"actionLoad_mesh")
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        self.actionRe_start = QAction(MainWindow)
        self.actionRe_start.setObjectName(u"actionRe_start")
        self.actionLoad_gcode = QAction(MainWindow)
        self.actionLoad_gcode.setObjectName(u"actionLoad_gcode")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 622, 452))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.horizontalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(620, 450))
        self.tab_workpiece = QWidget()
        self.tab_workpiece.setObjectName(u"tab_workpiece")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_workpiece.sizePolicy().hasHeightForWidth())
        self.tab_workpiece.setSizePolicy(sizePolicy)
        self.tab_workpiece.setBaseSize(QSize(10, 10))
        self.tab_workpiece.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.tabWidget.addTab(self.tab_workpiece, "")
        self.tab_par_result = QWidget()
        self.tab_par_result.setObjectName(u"tab_par_result")
        self.tabWidget.addTab(self.tab_par_result, "")
        self.tab_comb_result = QWidget()
        self.tab_comb_result.setObjectName(u"tab_comb_result")
        self.tabWidget.addTab(self.tab_comb_result, "")
        self.tab_temp = QWidget()
        self.tab_temp.setObjectName(u"tab_temp")
        self.tabWidget.addTab(self.tab_temp, "")
        self.tab_force = QWidget()
        self.tab_force.setObjectName(u"tab_force")
        self.tabWidget.addTab(self.tab_force, "")
        self.tab_roughness = QWidget()
        self.tab_roughness.setObjectName(u"tab_roughness")
        self.tabWidget.addTab(self.tab_roughness, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(640, 10, 201, 384))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(170, 100))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -270, 192, 724))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(192, 0))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(0, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.label_2)

        self.wp_mat = QComboBox(self.scrollAreaWidgetContents)
        self.wp_mat.setObjectName(u"wp_mat")
        self.wp_mat.setMinimumSize(QSize(0, 22))

        self.verticalLayout.addWidget(self.wp_mat)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setMinimumSize(QSize(50, 20))

        self.horizontalLayout_8.addWidget(self.label_7)

        self.workpiece_scale = QSpinBox(self.scrollAreaWidgetContents)
        self.workpiece_scale.setObjectName(u"workpiece_scale")
        self.workpiece_scale.setMinimumSize(QSize(0, 20))
        self.workpiece_scale.setMaximum(1000)
        self.workpiece_scale.setValue(100)

        self.horizontalLayout_8.addWidget(self.workpiece_scale)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMinimumSize(QSize(50, 20))

        self.horizontalLayout_12.addWidget(self.label_10)

        self.workpiece_scale_2 = QSpinBox(self.scrollAreaWidgetContents)
        self.workpiece_scale_2.setObjectName(u"workpiece_scale_2")
        self.workpiece_scale_2.setMinimumSize(QSize(0, 20))
        self.workpiece_scale_2.setMaximum(1000)
        self.workpiece_scale_2.setValue(293)

        self.horizontalLayout_12.addWidget(self.workpiece_scale_2)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(0, 20))
        self.label_5.setFont(font)

        self.verticalLayout.addWidget(self.label_5)

        self.tool_mode = QComboBox(self.scrollAreaWidgetContents)
        self.tool_mode.setObjectName(u"tool_mode")
        self.tool_mode.setMinimumSize(QSize(0, 22))

        self.verticalLayout.addWidget(self.tool_mode)

        self.tool_mat = QComboBox(self.scrollAreaWidgetContents)
        self.tool_mat.setObjectName(u"tool_mat")
        self.tool_mat.setMinimumSize(QSize(0, 22))

        self.verticalLayout.addWidget(self.tool_mat)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)
        self.label_16.setMinimumSize(QSize(70, 20))
        font1 = QFont()
        font1.setBold(True)
        self.label_16.setFont(font1)

        self.verticalLayout.addWidget(self.label_16)

        self.tool_distrubution = QComboBox(self.scrollAreaWidgetContents)
        self.tool_distrubution.setObjectName(u"tool_distrubution")
        self.tool_distrubution.setMinimumSize(QSize(0, 22))

        self.verticalLayout.addWidget(self.tool_distrubution)

        self.grain_redistribution = QRadioButton(self.scrollAreaWidgetContents)
        self.grain_redistribution.setObjectName(u"grain_redistribution")

        self.verticalLayout.addWidget(self.grain_redistribution)

        self.rigid_flexible = QRadioButton(self.scrollAreaWidgetContents)
        self.rigid_flexible.setObjectName(u"rigid_flexible")

        self.verticalLayout.addWidget(self.rigid_flexible)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_11.addWidget(self.label_11)

        self.num_step = QSpinBox(self.scrollAreaWidgetContents)
        self.num_step.setObjectName(u"num_step")
        self.num_step.setMinimumSize(QSize(0, 20))
        self.num_step.setMaximum(1000)
        self.num_step.setValue(10)

        self.horizontalLayout_11.addWidget(self.num_step)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)
        self.label_12.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_13.addWidget(self.label_12)

        self.num_grains = QSpinBox(self.scrollAreaWidgetContents)
        self.num_grains.setObjectName(u"num_grains")
        self.num_grains.setMinimumSize(QSize(0, 20))
        self.num_grains.setMaximum(1000)
        self.num_grains.setValue(1)

        self.horizontalLayout_13.addWidget(self.num_grains)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")
        sizePolicy2.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy2)
        self.label_15.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_16.addWidget(self.label_15)

        self.num_vertices = QSpinBox(self.scrollAreaWidgetContents)
        self.num_vertices.setObjectName(u"num_vertices")
        self.num_vertices.setMinimumSize(QSize(0, 20))
        self.num_vertices.setMinimum(4)
        self.num_vertices.setMaximum(1000)
        self.num_vertices.setValue(10)

        self.horizontalLayout_16.addWidget(self.num_vertices)


        self.verticalLayout.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")
        sizePolicy2.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy2)
        self.label_20.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_19.addWidget(self.label_20)

        self.grain_size = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.grain_size.setObjectName(u"grain_size")
        self.grain_size.setMinimumSize(QSize(0, 20))
        self.grain_size.setValue(0.050000000000000)

        self.horizontalLayout_19.addWidget(self.grain_size)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        sizePolicy2.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy2)
        self.label_21.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_20.addWidget(self.label_21)

        self.spacing = QSpinBox(self.scrollAreaWidgetContents)
        self.spacing.setObjectName(u"spacing")
        self.spacing.setMinimumSize(QSize(0, 20))
        self.spacing.setMinimum(4)
        self.spacing.setMaximum(1000)
        self.spacing.setValue(200)

        self.horizontalLayout_20.addWidget(self.spacing)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_10.addWidget(self.label_9)

        self.velocity = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.velocity.setObjectName(u"velocity")
        self.velocity.setMinimumSize(QSize(0, 20))
        self.velocity.setValue(30.000000000000000)

        self.horizontalLayout_10.addWidget(self.velocity)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        sizePolicy2.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy2)
        self.label_18.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_17.addWidget(self.label_18)

        self.initial_depth = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.initial_depth.setObjectName(u"initial_depth")
        self.initial_depth.setMinimumSize(QSize(0, 20))
        self.initial_depth.setMinimum(-100.000000000000000)

        self.horizontalLayout_17.addWidget(self.initial_depth)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")
        sizePolicy2.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy2)
        self.label_19.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_18.addWidget(self.label_19)

        self.depth_increase = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.depth_increase.setObjectName(u"depth_increase")
        self.depth_increase.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_18.addWidget(self.depth_increase)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.label_17 = QLabel(self.scrollAreaWidgetContents)
        self.label_17.setObjectName(u"label_17")
        sizePolicy2.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy2)
        self.label_17.setMinimumSize(QSize(70, 20))
        self.label_17.setFont(font1)

        self.verticalLayout.addWidget(self.label_17)

        self.tool_type = QComboBox(self.scrollAreaWidgetContents)
        self.tool_type.setObjectName(u"tool_type")
        self.tool_type.setMinimumSize(QSize(0, 22))

        self.verticalLayout.addWidget(self.tool_type)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)
        self.label_8.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_9.addWidget(self.label_8)

        self.tool_radius = QSpinBox(self.scrollAreaWidgetContents)
        self.tool_radius.setObjectName(u"tool_radius")
        self.tool_radius.setMinimumSize(QSize(0, 20))
        self.tool_radius.setMaximum(1000)
        self.tool_radius.setValue(100)

        self.horizontalLayout_9.addWidget(self.tool_radius)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)
        self.label_13.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_14.addWidget(self.label_13)

        self.depth = QSpinBox(self.scrollAreaWidgetContents)
        self.depth.setObjectName(u"depth")
        self.depth.setMinimumSize(QSize(0, 20))
        self.depth.setMaximum(1000)
        self.depth.setValue(100)

        self.horizontalLayout_14.addWidget(self.depth)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)
        self.label_14.setMinimumSize(QSize(70, 20))

        self.horizontalLayout_15.addWidget(self.label_14)

        self.grain_scale = QSpinBox(self.scrollAreaWidgetContents)
        self.grain_scale.setObjectName(u"grain_scale")
        self.grain_scale.setMinimumSize(QSize(0, 20))
        self.grain_scale.setMaximum(1000)
        self.grain_scale.setValue(1)

        self.horizontalLayout_15.addWidget(self.grain_scale)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.bStart = QPushButton(self.centralwidget)
        self.bStart.setObjectName(u"bStart")
        self.bStart.setGeometry(QRect(640, 420, 201, 31))
        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        self.bStop.setGeometry(QRect(640, 450, 201, 31))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 480, 831, 23))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy3)
        self.progressBar.setValue(24)
        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(10, 509, 811, 71))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 809, 69))
        self.log_output = QPlainTextEdit(self.scrollAreaWidgetContents_2)
        self.log_output.setObjectName(u"log_output")
        self.log_output.setGeometry(QRect(-5, 1, 811, 201))
        self.log_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.log_output.setCenterOnScroll(True)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.bGenerate = QPushButton(self.centralwidget)
        self.bGenerate.setObjectName(u"bGenerate")
        self.bGenerate.setGeometry(QRect(640, 390, 201, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 867, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTool = QMenu(self.menubar)
        self.menuTool.setObjectName(u"menuTool")
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuFile.addAction(self.actionLoad_mesh)
        self.menuFile.addAction(self.actionLoad_gcode)
        self.menuTool.addAction(self.actionRun)
        self.menuTool.addAction(self.actionStop)
        self.menuTool.addAction(self.actionRe_start)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_mesh.setText(QCoreApplication.translate("MainWindow", u"Load mesh", None))
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.actionRe_start.setText(QCoreApplication.translate("MainWindow", u"Re start", None))
        self.actionLoad_gcode.setText(QCoreApplication.translate("MainWindow", u"Load gcode", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_workpiece), QCoreApplication.translate("MainWindow", u"Workpiece", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_par_result), QCoreApplication.translate("MainWindow", u"Partical results", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_comb_result), QCoreApplication.translate("MainWindow", u"Combine result", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_temp), QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_force), QCoreApplication.translate("MainWindow", u"Force", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_roughness), QCoreApplication.translate("MainWindow", u"Roughness", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Workpiece", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Material", None))
        self.wp_mat.setCurrentText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ini temp", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Tool", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Single mode", None))
        self.grain_redistribution.setText(QCoreApplication.translate("MainWindow", u"Redistribution (Y/N)", None))
        self.rigid_flexible.setText(QCoreApplication.translate("MainWindow", u"Rigid/Fexible", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Steps", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"nGrains", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"nVertice", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Size: mm", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Space: um", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Vel (m/s)", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Init dep: mm", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"DepInc: mm", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Multiple mode", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Radius", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Depth", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"GrainSc", None))
        self.bStart.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.bStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.bGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTool.setTitle(QCoreApplication.translate("MainWindow", u"Tool", None))
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
    # retranslateUi

