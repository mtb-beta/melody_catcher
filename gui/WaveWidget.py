#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 17時40分03秒 JST
Note:音楽信号描画ウィジェットの制御クラス
"""
from PyQt4 import QtCore,QtGui

class WaveWidget(QtGui.QWidget):
    def __init__(self,wave_width,wave_height,parent = None):
        QtGui.QWidget.__init__(self,parent = parent)
        self.width  = wave_width-20
        self.height = wave_height-20
        self.setup()
        self.source = []
        self.wave_dict = {}
        self.wave_palette = 0
        self.sample_rate = 44100.0
        self.time_bar = CurrentTimeBar()

    def setup(self):
        self.setFixedSize(self.width,self.height)
        self.offscreen = QtGui.QPixmap(self.width,self.height)
        self.draw_frame()
        self.update()

    def set_slider(self,slider):
        self.slider = slider

    def set_parameter(self,view_times,index):
        self.index = index
        self.view_times = view_times
        self.width_size = view_times/2
        self.frames = (self.view_times * self.sample_rate) / self.width
        self.palette_width = int( ( self.source[self.index].nframes) / self.frames )
        self.wave_dict[self.view_times] = WavePalette(self.width_size,self.palette_width,self.height,self.frames)
        #print 'frames:',self.frames
        #print 'palette_width:',self.palette_width
        self.slider.setMaximum(self.palette_width-self.width)

    def init_current_times(self):
        self.current_times = 0

    def expansion(self):
        if self.view_times*2 < 50:
            self.view_times = self.view_times*2
        self.width_size =self.view_times/2
        self.frames = self.view_times*self.sample_rate / self.width
        self.draw_wave(self.index)

    def cuttail(self):
        if self.view_times/2 >5:
            self.view_times = self.view_times/2
        self.width_size =self.view_times/2
        self.frames = self.view_times*self.sample_rate / self.width
        self.draw_wave(self.index)

    def draw_frame(self):
        #self.back_ground_color = QtGui.QColor.fromCmykF(0.3,0.2,0.2,0.1)
        self.back_ground_color = QtCore.Qt.white
        self.offscreen.fill(self.back_ground_color)

        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        for i in range(2):
            painter.drawLine(i,0,i,self.height)
            painter.drawLine(self.width-i,0,self.width-i,self.height)
            painter.drawLine(0,self.height-i,self.width,self.height-i)
            painter.drawLine(0,i,self.width,i)
        painter.end()

    def draw_wave(self,index):
        print 'draw_wave'
        self.index = index
        painter = QtGui.QPainter()
        objectPalette =self.wave_dict[self.view_times]
        painter.begin(objectPalette.palette)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawLine(0,objectPalette.height/2,objectPalette.width,objectPalette.height/2)
        painter.setPen(QtCore.Qt.black)
        old_x = 0
        old_y = 0
        index = int(index)
        #frames = int(self.source[index].nframes/self.width)
        for x in range(objectPalette.width):
            new_x = x 
            for j in range(objectPalette.size):
                new_y = self.source[index].signal[x*self.frames+int(objectPalette.frames/objectPalette.size*j)]/2.0**15.0*objectPalette.height/2+objectPalette.height/2
                #new_y = self.source[self.index].signal[x* self.frames ]/2.0**15.0*objectPalette.height/2 + objectPalette.height/2
                painter.drawLine(old_x,int(old_y),new_x,int(new_y))
                old_y = new_y
            old_x = new_x
        painter.end()
        self.wave_dict[self.view_times].CopyPalette()
        print 'draw_wave end'

    def draw_current_times(self):
        print 'draw_current+times'
        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        self.screen = self.wave_dict[self.view_times].view_palette.copy(self.current_times,0,self.current_times+self.width,self.height)
        painter.drawPixmap(0,0,self.screen)
        painter.end()
        self.update()


    def reverse(self,x):
        self.end_pos = x

        self.reverse_color = QtGui.QColor.fromCmykF(0.30,0.2,0.2,0.1)
        self.draw_frame()
        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.start_pos,2,self.end_pos-self.start_pos,self.height-4,self.reverse_color)
        painter.end()


        if self.wave_dict.has_key(self.view_times):
            self.draw_current_times()
        
        self.redraw()

    def redraw(self):
        self.update()

    def mousePressEvent(self,event):
        self.oldpos_x = event.x()
        self.start_pos = event.x()
        self.draw_frame()
        if self.wave_dict.has_key(self.view_times):
            self.draw_current_times()
        self.redraw()

    def mouseReleaseEvent(self,event):
        if self.start_pos == event.x():
            self.time_bar.time = self.current_times*4410.0 + event.x()*self.sample_rate/10.0
            self.timeBarPaint(event.x())

    def timeBarPaint(self,x):
        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QColor.fromCmykF(1,0.1,1.0,0.6))
        painter.fillRect(x,2,2,self.height-4,QtGui.QColor.fromCmykF(1,0.1,1.0,0.6))
        for i in range(4):
            painter.drawLine(x-3+i,2,x+1,10)
        painter.drawLine(x+5-i,2,x+1,10)
        painter.drawLine(x-3+i,self.height-2,x+1,self.height-12)
        painter.drawLine(x+5-i,self.height-2,x+1,self.height-12)
        painter.end()
        self.update()

    def mouseMoveEvent(self,event):
        self.reverse(event.x())


    def set_current_time(self,index):
        print 'set_current_time'

        self.current_times = index
        self.draw_frame()
        self.draw_current_times()
        self.update()


    def paintEvent(self,paint_event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawPixmap(0,0,self.offscreen)
        painter.end()

class CurrentTimeBar():
    def __init__(self):
        self.time = 0

class WavePalette():
    def __init__(self,size,width,height,frames):
        self.width = width
        self.height = height
        self.frames = frames
        self.palette = QtGui.QPixmap(width,height)
        self.view_palette = QtGui.QPixmap(width,height)
        self.size = size

        painter = QtGui.QPainter()
        painter.begin(self.palette)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        for i in range(2):
            painter.drawLine(i,0,i,self.height)
            painter.drawLine(self.width-i,0,self.width-i,self.height)
            painter.drawLine(0,self.height-i,self.width,self.height-i)
            painter.drawLine(0,i,self.width,i)
        painter.end()

    def CopyPalette(self):
        self.view_palette = self.palette.copy(0,0,self.width,self.height)
