# Form implementation generated from reading ui file 'question_widget.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_question_widget(object):
    def setupUi(self, question_widget):
        question_widget.setObjectName("question_widget")
        question_widget.resize(859, 816)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(question_widget.sizePolicy().hasHeightForWidth())
        question_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(question_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_question = QtWidgets.QLabel(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.label_question.setFont(font)
        self.label_question.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_question.setWordWrap(True)
        self.label_question.setObjectName("label_question")
        self.verticalLayout_2.addWidget(self.label_question)
        spacerItem = QtWidgets.QSpacerItem(20, 66, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_answer_A = QtWidgets.QHBoxLayout()
        self.horizontalLayout_answer_A.setObjectName("horizontalLayout_answer_A")
        self.radioButton_answer_A = QtWidgets.QRadioButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_answer_A.sizePolicy().hasHeightForWidth())
        self.radioButton_answer_A.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radioButton_answer_A.setFont(font)
        self.radioButton_answer_A.setText("")
        self.radioButton_answer_A.setIconSize(QtCore.QSize(16, 16))
        self.radioButton_answer_A.setObjectName("radioButton_answer_A")
        self.horizontalLayout_answer_A.addWidget(self.radioButton_answer_A)
        self.label_answer_A = ClickableLabel(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_answer_A.setFont(font)
        self.label_answer_A.setWordWrap(True)
        self.label_answer_A.setObjectName("label_answer_A")
        self.horizontalLayout_answer_A.addWidget(self.label_answer_A)
        self.verticalLayout.addLayout(self.horizontalLayout_answer_A)
        spacerItem2 = QtWidgets.QSpacerItem(20, 111, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_answer_B = QtWidgets.QHBoxLayout()
        self.horizontalLayout_answer_B.setObjectName("horizontalLayout_answer_B")
        self.radioButton_answer_B = QtWidgets.QRadioButton(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radioButton_answer_B.setFont(font)
        self.radioButton_answer_B.setText("")
        self.radioButton_answer_B.setObjectName("radioButton_answer_B")
        self.horizontalLayout_answer_B.addWidget(self.radioButton_answer_B)
        self.label_answer_B = ClickableLabel(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_answer_B.setFont(font)
        self.label_answer_B.setWordWrap(True)
        self.label_answer_B.setObjectName("label_answer_B")
        self.horizontalLayout_answer_B.addWidget(self.label_answer_B)
        self.verticalLayout.addLayout(self.horizontalLayout_answer_B)
        spacerItem3 = QtWidgets.QSpacerItem(20, 111, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_answer_C = QtWidgets.QHBoxLayout()
        self.horizontalLayout_answer_C.setObjectName("horizontalLayout_answer_C")
        self.radioButton_answer_C = QtWidgets.QRadioButton(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radioButton_answer_C.setFont(font)
        self.radioButton_answer_C.setText("")
        self.radioButton_answer_C.setObjectName("radioButton_answer_C")
        self.horizontalLayout_answer_C.addWidget(self.radioButton_answer_C)
        self.label_answer_C = ClickableLabel(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_answer_C.setFont(font)
        self.label_answer_C.setWordWrap(True)
        self.label_answer_C.setObjectName("label_answer_C")
        self.horizontalLayout_answer_C.addWidget(self.label_answer_C)
        self.verticalLayout.addLayout(self.horizontalLayout_answer_C)
        spacerItem4 = QtWidgets.QSpacerItem(20, 111, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_answer_D = QtWidgets.QHBoxLayout()
        self.horizontalLayout_answer_D.setObjectName("horizontalLayout_answer_D")
        self.radioButton_answer_D = QtWidgets.QRadioButton(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.radioButton_answer_D.setFont(font)
        self.radioButton_answer_D.setText("")
        self.radioButton_answer_D.setObjectName("radioButton_answer_D")
        self.horizontalLayout_answer_D.addWidget(self.radioButton_answer_D)
        self.label_answer_D = ClickableLabel(parent=question_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_answer_D.setFont(font)
        self.label_answer_D.setWordWrap(True)
        self.label_answer_D.setObjectName("label_answer_D")
        self.horizontalLayout_answer_D.addWidget(self.label_answer_D)
        self.verticalLayout.addLayout(self.horizontalLayout_answer_D)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem7 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.button_submit = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_submit.sizePolicy().hasHeightForWidth())
        self.button_submit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.button_submit.setFont(font)
        self.button_submit.setObjectName("button_submit")
        self.horizontalLayout_5.addWidget(self.button_submit)
        spacerItem8 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        spacerItem9 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout_2.addItem(spacerItem9)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.button_done = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_done.sizePolicy().hasHeightForWidth())
        self.button_done.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_done.setFont(font)
        self.button_done.setObjectName("button_done")
        self.horizontalLayout_6.addWidget(self.button_done)
        self.button_previous = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_previous.sizePolicy().hasHeightForWidth())
        self.button_previous.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_previous.setFont(font)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout_6.addWidget(self.button_previous)
        self.button_next = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_next.sizePolicy().hasHeightForWidth())
        self.button_next.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_next.setFont(font)
        self.button_next.setObjectName("button_next")
        self.horizontalLayout_6.addWidget(self.button_next)
        self.button_watch = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_watch.sizePolicy().hasHeightForWidth())
        self.button_watch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_watch.setFont(font)
        self.button_watch.setObjectName("button_watch")
        self.horizontalLayout_6.addWidget(self.button_watch)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem10 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.verticalLayout_2.addItem(spacerItem10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.button_home = QtWidgets.QPushButton(parent=question_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_home.sizePolicy().hasHeightForWidth())
        self.button_home.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_home.setFont(font)
        self.button_home.setObjectName("button_home")
        self.horizontalLayout_7.addWidget(self.button_home)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.retranslateUi(question_widget)
        QtCore.QMetaObject.connectSlotsByName(question_widget)

    def retranslateUi(self, question_widget):
        _translate = QtCore.QCoreApplication.translate
        question_widget.setWindowTitle(_translate("question_widget", "Form"))
        self.label_question.setText(_translate("question_widget", "Question Text"))
        self.label_answer_A.setText(_translate("question_widget", "Answer A"))
        self.label_answer_B.setText(_translate("question_widget", "Answer B"))
        self.label_answer_C.setText(_translate("question_widget", "Answer C"))
        self.label_answer_D.setText(_translate("question_widget", "Answer D"))
        self.button_submit.setText(_translate("question_widget", "Submit"))
        self.button_done.setText(_translate("question_widget", "Mark as \"Done\""))
        self.button_previous.setText(_translate("question_widget", "Previous"))
        self.button_next.setText(_translate("question_widget", "Next"))
        self.button_watch.setText(_translate("question_widget", "Watch this question"))
        self.button_home.setText(_translate("question_widget", "Stop Training"))
from pilot_utils.azf_trainer.ui.clickable_label import ClickableLabel
