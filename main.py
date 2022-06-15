import math
import sys
from random import random

from PyQt6 import QtGui, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)


class about(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("about.ui", self)


app = QApplication(sys.argv)
window = UI()
window.show()

aboutDialog = about()
window.action_about.triggered.connect(lambda: aboutDialog.show())
# aboutDialog.label_email.linkActivated()
# aboutDialog.label_email.linkHovered(lambda: aboutDialog.label_email.setStyleSheet('background-color: rgb(255, 112, 87);'))

with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

# //--- Variables ---//
aboutDialog.about__icon.setStyleSheet('image: url("icon_500x500.png");')

# Main code
images = ['image: url("2 branches.png");',
          'image: url("3 branches.png");',
          'image: url("4 branches.png");']

lineEdit_weight = window.lineEdit_weight
lineEdit_H = window.lineEdit_H
lineEdit_A = window.lineEdit_A
lineEdit_C = window.lineEdit_C
lineEdit_W = window.lineEdit_W

# string.replace(QString(" "), QString(""))
# rx = "[0-9]"
# validator = QtGui.QRegularExpressionValidator(rx)

lineEdit_weight.setValidator(QtGui.QIntValidator(50, 999999))
# lineEdit_H.setValidator(QtGui.QRegularExpressionValidator(validator))
lineEdit_H.setValidator(QtGui.QIntValidator(0, 99999))
lineEdit_A.setValidator(QtGui.QIntValidator(0, 99999))
lineEdit_C.setValidator(QtGui.QIntValidator(0, 99999))
lineEdit_W.setValidator(QtGui.QIntValidator(0, 179))


def set__btnState_pressed(element):
    element.setStyleSheet('background-color: rgb(255, 112, 87);')


def set__btnState_released(element):
    element.setStyleSheet('background-color: rgb(230, 230, 230);')


window.btn_more.pressed.connect(lambda: set__btnState_pressed(window.btn_more))
window.btn_more.released.connect(lambda: set__btnState_released(window.btn_more))


def normalRound(n: float):
    return math.floor(n + 0.5)


def randomRound(n: float):
    return math.floor(n + random())


def remove__allElements(element, list):
    for element in list:
        list.remove(element)


def set__element_readOnly_true(element):
    try:
        element.setReadOnly(True)
        element.setStyleSheet('background-color: rgb(211, 211, 211);')
    except:
        print("Error! " + str(element) + " cant't be set readOnly")


def set__element_readOnly_false(element):
    try:
        element.setReadOnly(False)
        element.setStyleSheet('background-color: rgb(255, 255, 255);')
    except:
        print("Error! " + str(element) + " cant't be readOnly")


def set__element_disabled(element):
    element.setEnabled(False)
    element.setStyleSheet('background-color: rgb(211, 211, 211);')  # gray


def set__element_enabled(element):
    element.setEnabled(True)
    element.setStyleSheet('background-color: rgb(255, 255, 255);')  # white


def set__img(i):
    window.frame_Img.setStyleSheet(str(images[i]))


koef_k_dict = {'radio_2Points': 1, 'radio_3Points': 1, 'radio_4Points': 0.75}


def define__koefK(radioButton_checked):
    if radioButton_checked == "radio_2Points":
        return koef_k_dict['radio_2Points']

    elif radioButton_checked == "radio_3Points":
        return koef_k_dict['radio_3Points']

    elif radioButton_checked == "radio_4Points":
        return koef_k_dict['radio_4Points']


slingCount_dict = {'radio_2Points': 2, 'radio_3Points': 3, 'radio_4Points': 4}


def define__slingCount(radioButton_checked):
    if radioButton_checked == "radio_2Points":
        return slingCount_dict['radio_2Points']

    elif radioButton_checked == "radio_3Points":
        return slingCount_dict['radio_3Points']

    elif radioButton_checked == "radio_4Points":
        return slingCount_dict['radio_4Points']


def check__radioButton():
    if window.radio_2Points.isChecked():
        return 'radio_2Points'

    if window.radio_3Points.isChecked():
        return 'radio_3Points'

    if window.radio_4Points.isChecked():
        return 'radio_4Points'


window.btn_more.clicked.connect(lambda: clearAllInputs())


def clearAllInputs():
    for i in allInputs:
        getattr(window, i).setText('')
        set__element_enabled(
            getattr(window, i))
        set__element_readOnly_false(
            getattr(window, i))
    getattr(window, 'lineEdit_weight').setText('')
    getattr(window, 'label_tension').setText('-')
    getattr(window, 'label_gp').setText('-')
    window.statusbar.showMessage('')
    usedInputs.clear()


window.radio_2Points.clicked.connect(lambda: set__img(0))
window.radio_3Points.clicked.connect(lambda: set__img(1))
window.radio_4Points.clicked.connect(lambda: set__img(2))
window.radio_2Points.clicked.connect(lambda: calc__valuesInInputs(lineEdit_A.text(),
                                                                  lineEdit_C.text(),
                                                                  lineEdit_H.text(),
                                                                  lineEdit_W.text()))
window.radio_3Points.clicked.connect(lambda: calc__valuesInInputs(lineEdit_A.text(),
                                                                  lineEdit_C.text(),
                                                                  lineEdit_H.text(),
                                                                  lineEdit_W.text()))
window.radio_4Points.clicked.connect(lambda: calc__valuesInInputs(lineEdit_A.text(),
                                                                  lineEdit_C.text(),
                                                                  lineEdit_H.text(),
                                                                  lineEdit_W.text()))

usedInputs = []
allInputs = ['lineEdit_H',
             'lineEdit_A',
             'lineEdit_C',
             'lineEdit_W']


def add__listOfUsedInputs(sender):
    if sender.objectName() not in usedInputs:
        usedInputs.append(sender.objectName())
    return usedInputs


def check__usedInputs():
    add__listOfUsedInputs(window.sender())
    if len(usedInputs) == 2:
        unusedInput = list(set(usedInputs) ^ set(allInputs))
        for i in unusedInput:
            set__element_readOnly_true(
                getattr(window, unusedInput[unusedInput.index(i)]))

        calc__valuesInInputs(lineEdit_A.text(),
                             lineEdit_C.text(),
                             lineEdit_H.text(),
                             lineEdit_W.text())


def check__unusedInputs():
    if len(usedInputs) < 3:
        for i in allInputs:
            set__element_readOnly_false(
                getattr(window, allInputs[allInputs.index(i)]))


def show__valuesInLineEdits(element, value):
    getattr(window, element).setText(str(value))


def show__errorInLineEdits(*elements: str):
    for element in elements:
        getattr(window, element).setText('Err')


def clear__unusedLineEdits():
    unusedInput = list(set(usedInputs) ^ set(allInputs))
    if len(usedInputs) >= 2:
        for i in unusedInput:
            getattr(window, i).setText('')


def toggle__lineEdit_error(*elements):
    for element in elements:
        getattr(window, element).setStyleSheet(
            'background-color: rgb(255, 73, 60);')


def toggle__lineEdit_warning(*elements):
    for element in elements:
        getattr(window, element).setStyleSheet(
            'background-color: rgb(252, 209, 21);')


# CALCULATING -------------------------------------------------------


def calc__PhiphagorTheory(katet_1, katet_2, gipotenuza):
    if int(gipotenuza) == 0:
        gipotenuza = math.sqrt(int(katet_1) ** 2 + int(katet_2) ** 2)
        return gipotenuza

    if int(gipotenuza) ** 2 - int(katet_1) ** 2 >= 0 or int(gipotenuza) ** 2 - int(katet_2) ** 2 >= 0:
        if int(katet_1) == 0:
            katet_1 = math.sqrt(int(gipotenuza) ** 2 - int(katet_2) ** 2)
            return katet_1
        elif int(katet_2) == 0:
            katet_2 = math.sqrt(int(gipotenuza) ** 2 - int(katet_1) ** 2)
            return katet_2
    else:
        window.statusbar.showMessage("Где-то в коде затаилась ошибка :(")


def calc__carrying(weight: int, angle_w, k, slingCount, g=9.80665):
    try:
        print()
        print('weight - ', str(weight))
        print('k - ' + str(k))
        print('angle - ' + str(math.cos(math.radians(angle_w / 2))))
        print('slingCount - ' + str(slingCount))
        print()
        carrying = int(weight) / (math.cos(math.radians(angle_w / 2))
                                  * int(slingCount) * float(k))
        tension = carrying * g
        show__valuesInLineEdits('label_gp', normalRound(carrying))
        show__valuesInLineEdits('label_tension', normalRound(tension))
    except:
        print('--- Error in calculating carrying! Check data in "lineEdit_weight" ---')


def calc__valuesInInputs(itemLength_a: float, slingLength_c: float, height_h: float, angle_w: float):
    k = define__koefK(check__radioButton())
    slingCount = define__slingCount(check__radioButton())
    weight = lineEdit_weight.text()
    angle_w_calculated = 0

    if 'lineEdit_H' in usedInputs and 'lineEdit_A' in usedInputs:
        try:
            slingLength_c_calculated, angle_w_calculated = calc__C_W(
                itemLength_a, height_h)
            show__valuesInLineEdits(
                'lineEdit_C', normalRound(slingLength_c_calculated))
            show__valuesInLineEdits(
                'lineEdit_W', normalRound(angle_w_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_C', 'lineEdit_W')
            toggle__lineEdit_error('lineEdit_C', 'lineEdit_W')

    if 'lineEdit_C' in usedInputs and 'lineEdit_A' in usedInputs:
        try:
            angle_w_calculated, height_h_calculated = calc__W_H(
                itemLength_a, slingLength_c)
            show__valuesInLineEdits(
                'lineEdit_W', normalRound(angle_w_calculated))
            show__valuesInLineEdits(
                'lineEdit_H', normalRound(height_h_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_H', 'lineEdit_W')
            toggle__lineEdit_error('lineEdit_H', 'lineEdit_W')

    if 'lineEdit_C' in usedInputs and 'lineEdit_H' in usedInputs:
        try:
            itemLength_a_calculated, angle_w_calculated = calc__A_W(
                slingLength_c, height_h)
            show__valuesInLineEdits(
                'lineEdit_A', normalRound(itemLength_a_calculated))
            show__valuesInLineEdits(
                'lineEdit_W', normalRound(angle_w_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_W', 'lineEdit_A')
            toggle__lineEdit_error('lineEdit_W', 'lineEdit_A')

    if 'lineEdit_W' in usedInputs and 'lineEdit_H' in usedInputs:
        try:
            itemLength_a_calculated, slingLength_c_calculated = calc__A_C(
                height_h, angle_w)
            show__valuesInLineEdits(
                'lineEdit_A', normalRound(itemLength_a_calculated))
            show__valuesInLineEdits(
                'lineEdit_C', normalRound(slingLength_c_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_A', 'lineEdit_C')
            toggle__lineEdit_error('lineEdit_A', 'lineEdit_C')

    if 'lineEdit_W' in usedInputs and 'lineEdit_A' in usedInputs:
        try:
            slingLength_c_calculated, height_h_calculated = calc__C_H(
                itemLength_a, angle_w)
            show__valuesInLineEdits(
                'lineEdit_C', normalRound(slingLength_c_calculated))
            show__valuesInLineEdits(
                'lineEdit_H', normalRound(height_h_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_C', 'lineEdit_H')
            toggle__lineEdit_error('lineEdit_C', 'lineEdit_H')

    if 'lineEdit_W' in usedInputs and 'lineEdit_C' in usedInputs:
        try:
            itemLength_a_calculated, height_h_calculated = calc__A_H(
                slingLength_c, angle_w)
            show__valuesInLineEdits(
                'lineEdit_A', normalRound(itemLength_a_calculated))
            show__valuesInLineEdits(
                'lineEdit_H', normalRound(height_h_calculated))
        except:
            window.statusbar.showMessage('Проверьте введенные данные!')
            show__errorInLineEdits('lineEdit_A', 'lineEdit_H')
            toggle__lineEdit_error('lineEdit_A', 'lineEdit_H')

    check__angleMore90(angle_w_calculated)
    check__angleMore180(angle_w_calculated)
    calc__carrying(weight, angle_w_calculated, k, slingCount)


def check__angleMore180(angle: float):
    if angle >= 180:
        window.statusbar.showMessage(
            'Проверьте введенные данные! Значение угла не может быть равно или превышать 180°.')
        toggle__lineEdit_error('lineEdit_W')


def check__angleMore90(angle: float):
    if angle >= 90:
        window.statusbar.showMessage(
            'Проверьте введенные данные! Значение угла равно или превышает 90°.')
        toggle__lineEdit_warning('lineEdit_W')


def calc__C_W(itemLength_a, height_h):
    itemLength_a = float(itemLength_a) / 2
    A_devision_H = itemLength_a / (float(height_h))
    rezuultInRadians = math.atan(A_devision_H)
    angle_w = math.degrees(rezuultInRadians)
    angle_w *= 2
    slingLength_c = calc__PhiphagorTheory(itemLength_a, height_h, 0)
    return slingLength_c, angle_w


def calc__W_H(itemLength_a, slingLength_c):
    itemLength_a = float(itemLength_a) / 2
    A_devision_C = itemLength_a / (float(slingLength_c))
    rezuultInRadians = math.asin(A_devision_C)
    angle_w = math.degrees(rezuultInRadians)
    angle_w *= 2
    height_h = calc__PhiphagorTheory(itemLength_a, 0, slingLength_c)
    return angle_w, height_h


def calc__A_W(slingLength_c, height_h):
    H_devision_C = float(height_h) / (float(slingLength_c))
    rezuultInRadians = math.acos(H_devision_C)
    angle_w = 2 * math.degrees(rezuultInRadians)
    itemLength_a = calc__PhiphagorTheory(
        0, height_h, slingLength_c) * 2
    return itemLength_a, angle_w


def calc__A_H(slingLength_c, angle_w):
    angle_w = float(angle_w) / 2
    itemLength_a = float(slingLength_c) * math.sin(math.radians(angle_w))
    height_h = calc__PhiphagorTheory(itemLength_a, 0, slingLength_c)
    itemLength_a *= 2
    return itemLength_a, height_h


def calc__C_H(itemLength_a, angle_w):
    itemLength_a = float(itemLength_a) / 2
    angle_w = float(angle_w) / 2
    slingLength_c = itemLength_a / math.sin(math.radians(angle_w))
    height_h = calc__PhiphagorTheory(itemLength_a, 0, slingLength_c)
    return slingLength_c, height_h


def calc__A_C(height_h, angle_w):
    angle_w = float(angle_w) / 2
    slingLength_c = float(height_h) / \
                    math.cos(math.radians(float(angle_w)))
    itemLength_a = calc__PhiphagorTheory(0, height_h, slingLength_c) * 2
    return itemLength_a, slingLength_c


def init__calcOnEditValue():
    if window.sender().text() != "":
        if window.sender().text()[0] != "0":
            window.statusbar.showMessage("")

            if window.sender() == lineEdit_W and type(lineEdit_W.text()) == str:
                check__angleMore90(float(lineEdit_W.text()))
                check__angleMore180(float(lineEdit_W.text()))

            clear__unusedLineEdits()
            check__usedInputs()
        else:
            window.statusbar.showMessage(
                'Проверьте введенные данные! Значения не могут начинаться или равняться 0')
            toggle__lineEdit_error(window.sender().objectName())

    else:
        window.statusbar.showMessage("")
        clear__unusedLineEdits()
        if len(usedInputs) <= 1:
            usedInputs.clear()
        else:
            if window.sender().objectName() in usedInputs:
                usedInputs.remove(window.sender().objectName())
        check__unusedInputs()


def init__calcOnEditWeight():
    if window.sender().text() != "":
        if window.sender().text()[0] != "0":
            window.statusbar.showMessage("")
            if lineEdit_A.text() != '' and lineEdit_C.text() != '' and lineEdit_H.text() != '' and lineEdit_W.text():
                calc__valuesInInputs(lineEdit_A.text(),
                                     lineEdit_C.text(),
                                     lineEdit_H.text(),
                                     lineEdit_W.text())

        else:
            window.statusbar.showMessage(
                'Проверьте введенные данные! Значения не могут начинаться или равняться 0')
            toggle__lineEdit_error(window.sender().objectName())

    else:
        window.statusbar.showMessage("")
        show__valuesInLineEdits('label_gp', '-')


lineEdit_H.textEdited.connect(lambda: init__calcOnEditValue())
lineEdit_A.textEdited.connect(lambda: init__calcOnEditValue())
lineEdit_C.textEdited.connect(lambda: init__calcOnEditValue())
lineEdit_W.textEdited.connect(lambda: init__calcOnEditValue())
# Переписать на вычисление только carrying
lineEdit_weight.textEdited.connect(lambda: init__calcOnEditWeight())

sys.exit(app.exec())
