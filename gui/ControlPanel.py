#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月18日 火曜日 15時20分35秒 JST
Note:コントロールパネルを制御するクラス
"""

from PyQt4 import QtGui,QtCore
from ControlWidget import*

class ControlPanel(QtGui.QGroupBox):
  def __init__(self,title,width,height,parent= None):
    super(ControlPanel,self).__init__(title,parent)
    #print title
    self.control_widget = ControlWidget(width,height)
    self.layout = QtGui.QHBoxLayout()
    self.layout.addWidget(self.control_widget)
    self.setLayout(self.layout)
    self.setFixedSize(width,height)


