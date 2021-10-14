# Main file
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Expense import *

#Incomplete
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        pass






if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())