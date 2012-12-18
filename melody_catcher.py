#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月11日 火曜日 16時34分17秒 JST
Note:
"""

from PyQt4 import QtCore,QtGui
import sys
import numpy as np
import os.path
import os
from gui.MainWindow import*


display_width = 1400
display_height =850


def main():

  app = QtGui.QApplication(sys.argv)
  app_window = MainWindow(display_width,display_height)
  app_window.show()

  app.exec_()

if __name__ == "__main__":
  main()
