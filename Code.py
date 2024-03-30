from math import pow, sqrt, log, sin, cos, tan
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets, QtGui, QtCore

Form, _ = uic.loadUiType("mpc.ui")


string = []

p = 0

def ipf(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 1/x



def is_number(stroka: str):
    try:
        float(stroka)
        return True
    except ValueError:
        return False
                
def get_value(x):
    global string
    string1 = string
    for k, i in enumerate(string1):

        if i == '/' and string1[k+1] == 'x':
            string1[k] = '*(ipf(x))'
            string1[k+1] = ''

    s = ''.join(string1).replace('y=', '')
    
    try:
        code = compile(''.join(s.split(';')[0].replace('x', str(x))), "<string>", "eval")
        return eval(code)
    except Exception:
        return None



def dof(s):
    global p
    l_b = -2048
    r_b = 2047
    step = 0.1
    if s.count('/') > s.count('tan'):
        p = 1
        step = 1
    else:
        p = 0
        step = 0.1
    stroka = s.split(';')
    if len(stroka) > 1:
        splt = s.split(';')[1]
        try:
            if '>' in splt or '≥' in splt:
                l_b = int(splt[splt.index('x')+2:])

            if '<' in splt or '≤' in splt:
                r_b = int(splt[splt.index('x')+2:])

            if splt.count('<') == 2 or splt.count('≤') == 2 or ('<' in splt and '≤' in splt):
                l_b = int(splt[:splt.index('x')-1])
                r_b = int(splt[splt.index('x')+2:])
        except Exception:
            return None
    return l_b, r_b, step



class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.build_plot.clicked.connect(lambda: self.build_the_plot(dof(''.join(string))[0], dof(''.join(string))[1], dof(''.join(string))[2]))
        self.del_func.clicked.connect(lambda: self.del_the_func())
        self.button_0.clicked.connect(lambda: self.add_num('0'))
        self.button_1.clicked.connect(lambda: self.add_num('1'))
        self.button_2.clicked.connect(lambda: self.add_num('2'))
        self.button_3.clicked.connect(lambda: self.add_num('3'))
        self.button_4.clicked.connect(lambda: self.add_num('4'))
        self.button_5.clicked.connect(lambda: self.add_num('5'))
        self.button_6.clicked.connect(lambda: self.add_num('6'))
        self.button_7.clicked.connect(lambda: self.add_num('7'))
        self.button_8.clicked.connect(lambda: self.add_num('8'))
        self.button_9.clicked.connect(lambda: self.add_num('9'))
        self.button_point.clicked.connect(lambda: self.add_num('.'))
        self.button_sin.clicked.connect(lambda: self.add_s('sin'))
        self.button_cos.clicked.connect(lambda: self.add_s('cos'))
        self.button_tg.clicked.connect(lambda: self.add_s('tan'))
        self.button_ctg.clicked.connect(lambda: self.add_s('1/tan'))
        self.button_moe.clicked.connect(lambda: self.add_s('≥'))
        self.button_loe.clicked.connect(lambda: self.add_s('≤'))
        self.button_more.clicked.connect(lambda: self.add_s('>'))
        self.button_less.clicked.connect(lambda: self.add_s('<'))
        self.button_minus.clicked.connect(lambda: self.add_s('-'))
        self.button_division.clicked.connect(lambda: self.add_s('/'))
        self.button_power.clicked.connect(lambda: self.add_s('**'))
        self.button_equals.clicked.connect(lambda: self.add_s('='))
        self.button_plus.clicked.connect(lambda: self.add_s('+'))
        self.button_mult.clicked.connect(lambda: self.add_s('*'))
        self.button_sqrt.clicked.connect(lambda: self.add_s('sqrt'))
        self.button_log.clicked.connect(lambda: self.add_s('log'))
        self.button_cp.clicked.connect(lambda: self.add_s(')'))
        self.button_comma.clicked.connect(lambda: self.add_s(', '))
        self.button_y.clicked.connect(lambda: self.add_s('y'))
        self.button_op.clicked.connect(lambda: self.add_s('('))
        self.button_abs.clicked.connect(lambda: self.add_s('abs'))
        self.button_x.clicked.connect(lambda: self.add_s('x'))
        self.button_csb.clicked.connect(lambda: self.add_s(';'))
        self.button_backspace.clicked.connect(lambda: self.delete())
        


    def view_func(self, s):
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setItalic(True)
        self.now_func.setFont(font)
        self.now_func.setAlignment(QtCore.Qt.AlignCenter)
        self.now_func.setText(
            ' '.join(s).replace('**', '^').replace('1/tan', 'ctg').replace('tan', 'tg').replace('sqrt','√'))

    def add_s(self, s):
        global string
        string.append(s)
        self.view_func(string)

    def add_num(self, s):
        global string
        if len(string) > 0 and len(string[-1]) > 0 and(string[-1].isdigit() or is_number(string[-1]) or string[-1][-1] == '.'):
            string[-1] += s
        else:
            string.append(s)
        self.view_func(string)

    def delete(self):
        global string
        if len(string) > 0:
            if is_number(string[-1]) and len(string[-1]) != 1:
                string[-1] = string[-1][:-1]
            else:
                string = string[:-1]
        self.view_func(string)


    def del_the_func(self):
        global string
        string = []
        self.view_func(string)


    def build_the_plot(self, l_b, r_b, step):
        plt.style.use('seaborn-v0_8')
        ax = plt.gca()
        ax.axhline(y=0, color='gray', linewidth = 1)    
        ax.axvline(x=0, color='gray', linewidth = 1)
        x = np.arange(l_b, r_b+step, step)
        y = np.array([get_value(y) for y in x])
        if p == 0:
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
        plt.plot(x, y)
        plt.grid(True)
        plt.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName('MathFunc Creator')
    w = Ui()
    w.show()
    sys.exit(app.exec_())