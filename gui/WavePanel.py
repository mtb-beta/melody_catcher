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
        self.width = width
        self.height = height - 50
        self.set_ui(width,height)
        self.view_times = 10 # 画面上には波形として表示される時間の長さ

    def setObject(self,midi_view_widget,control_panel,main_panel):
        self.midi_view_widget = midi_view_widget
        self.control_panel = control_panel
        self.main_panel = main_panel

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

    def set_value(self,value):
        print 'value:',value

    def initSlider(self):
        print 'init'
        widget = Slider(QtCore.Qt.Horizontal,'time')
        widget.initValue(self.wave_widget)
        return widget

    def setValue(self,value1,value2):
        self.slider.setMinimum(value1)
        self.slider.setMaximum(value2)

    def setMaximum(self,value):
        self.slider.setMaximum(value)

    def file_init(self,index):
        #self.set_slider_range(index)
        self.wave_widget.set_slider(self.slider)
        self.wave_widget.set_parameter(self.view_times,index)
        self.wave_widget.init_current_times()
        self.wave_widget.draw_wave(index)
        self.wave_widget.draw_frame()
        self.wave_widget.draw_current_times()

    def set_slider_range(self,index):
        print self.wave_widget.source[index].nframes
        print self.view_times
        print self.width
        tmp = ( self.wave_widget.source[index].nframes / ( ( self.view_times*44100.0 ) / self.width -10 ))
        print 'tmp:',tmp
        self.setMaximum(tmp)

