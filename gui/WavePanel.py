#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月18日 火曜日 15時43分58秒 JST
Note:波形描画パネルのコントロールクラス
"""

from PyQt4 import QtCore,QtGui
from WaveWidget import*
from Slider import*

class WavePanel(QtGui.QGroupBox):
  def __init__(self,title,width,height,parent=None):
    super(WavePanel,self).__init__(title,parent)
    width = width
    height = height - 50
    self.set_ui(width,height)
    self.view_times = 10


  def set_ui(self,width,height):
    self.wave_widget = WaveWidget(width-10,height-50)
    self.slider = self.initSlider()
    self.layout= QtGui.QVBoxLayout()
    self.layout.addWidget(self.wave_widget)
    self.layout.addWidget(self.slider.scrollBar)
    self.setLayout(self.layout)
    self.setFixedSize(width,height)

  def wheelEvent(self,event):
    self.slider.moveWheel(event.delta())
    self.wave_widget.set_current_time(self.slider.current)
    print 'wave wheel'

  def initSlider(self):
    widget = Slider(QtCore.Qt.Horizontal,'time')
    widget.initValue()
    return widget

  def setValue(self,value1,value2):
    self.slider.setMinimum(value1)
    self.slider.setMaximum(value2)

  def setMaximum(self,value):
    self.slider.setMaximum(value)

  def file_init(self,index):
    self.set_slider_range(index)
    self.wave_widget.set_parameter(self.view_times,index)
    self.wave_widget.init_current_times()
    self.wave_widget.draw_wave(index)

  def set_slider_range(self,index):
    self.setMaximum(self.wave_widget.source[index].nframes/4410.0)


