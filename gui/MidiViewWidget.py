#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 17時34分01秒 JST
Note:ピアノロールビューを制御するクラス
"""
from PyQt4 import QtCore,QtGui

class MidiViewWidget(QtGui.QWidget):
    def __init__(self,midi_width,midi_height,parent = None):
        QtGui.QWidget.__init__(self,parent = parent)
        self.width = midi_width-20
        self.height = midi_height-20
        self.width_size = 80
        self.height_size =30
        self.key_width = 100
        self.current_time = 0
        self.setup()
        self.midi_dict = {}
        self.view_times = 0

    def setObject(self,wave_panel,control_panel,main_panel):
        self.wave_panel = wave_panel
        self.control_panel = control_panel
        self.main_panel = main_panel

    def createPalette(self,view_times,palette_width,frames):
        self.view_times = view_times
        self.midi_dict[view_times]=MidiPalette(self.width_size,palette_width,self.height,frames)
        print 'createPalette'

    def set_current_time(self,index,shift):
        if self.midi_dict.has_key(self.view_times):
            self.midi_dict[self.view_times].SetShift(shift)
        self.current_times = index
        print 'midi current',index
        # self.draw_frame()
        # self.draw_current_times()
        # self.update()
        # TODO

    def draw_piano(self):
        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

    def make_pianoroll_key(self):
        painter = QtGui.QPainter()

        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #painter.setPen(QtCore.Qt.black)
        painter.setPen(QtGui.QColor(0,0,0))


        # 鍵盤とピアノロールの境
        painter.drawLine(self.key_width - 3,0,self.key_width - 3, self.width)
        painter.drawLine(self.key_width,0, self.key_width,self.width)
        
        # 黒鍵の描画
        def BlackKey_draw(y):
            painter.fillRect(0,y-(self.height_size/4)+3,self.key_width/2+3,self.height_size/2,QtCore.Qt.gray)
            painter.fillRect(0,y-(self.height_size/4),self.key_width/2,self.height_size/2,QtCore.Qt.black)

        # 鍵盤の描画
        note = 1
        y = self.height_size
        while(y < self.height):
            if note != 0 and note != 4:
                BlackKey_draw(y)
            painter.drawLine(0,y, self.key_width,y)
            y = y + self.height_size
            note = (note+1)%7

        painter.end()

  
    def draw_cell(self):

        painter = QtGui.QPainter()

        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(QtCore.Qt.gray)

        # ピアノロールのセル
        x = self.key_width+(self.current_time%self.width_size)
        y_space = ((self.height_size*7)/12.0)
        y = 0
        note = 0
        while(y < self.height):
            y_tmp = int(y)
            if note == 1 or note == 3 or note ==5 or note == 8 or note ==10:
                painter.fillRect(self.key_width,y,self.width,self.height_size/2,QtGui.QColor(230,230,230))
            elif note ==0 or note == 7:
                painter.drawLine(self.key_width,y_tmp,self.width,y_tmp) # horizonal
            y = y + y_space
            note = (note+1)%12

        while(x < self.width):
            painter.drawLine(x,0,x,self.height)# vartical
            x = x + self.width_size

        painter.end()

    def redraw_frame(self):
        painter = QtGui.QPainter()
        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # ピアノロールの淵
        for i in range(1):
            painter.drawLine(i,0,i,self.height)# left
            painter.drawLine(self.width-i,0,self.width-i,self.height) #right
            painter.drawLine(0,self.height-i,self.width,self.height-i) # bottom
            painter.drawLine(0,i,self.width,i) # top

        painter.end()

    def draw_frame(self):
        self.offscreen.fill(QtCore.Qt.white)

        painter = QtGui.QPainter()

        painter.begin(self.offscreen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # ピアノロールの淵
        for i in range(1):
            painter.drawLine(i,0,i,self.height)# left
            painter.drawLine(self.width-i,0,self.width-i,self.height) #right
            painter.drawLine(0,self.height-i,self.width,self.height-i) # bottom
            painter.drawLine(0,i,self.width,i) # top

        painter.end()

    def redraw(self):
        self.draw_frame()
        self.make_pianoroll_key()
        self.draw_cell()
        self.redraw_frame()
        self.update()

    def setup(self):
        self.setFixedSize(self.width,self.height)
        self.offscreen = QtGui.QPixmap(self.width,self.height)

        self.timer = QtCore.QTimer()

        self.timer.setInterval(1000)
        self.redraw()
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.redraw)
        self.timer.start()

    def paintEvent(self,paint_event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawPixmap(0,0,self.offscreen)
        painter.end()

class MidiPalette():
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

    def SetShift(self,shift):
        self.shift = shift



