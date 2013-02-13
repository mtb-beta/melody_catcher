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

    def setObject(self,wave_panel,midi_view_widget,main_panel):
        self.wave_panel = wave_panel
        self.midi_view_widget = midi_view_widget
        self.main_panel = main_panel



