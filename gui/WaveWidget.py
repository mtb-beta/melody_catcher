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
    self.width_size = 4
    self.wave_palette = 0

  def draw_frame(self):
    self.back_ground_color = QtGui.QColor.fromCmykF(0.40,0.4,0.1,0.6)
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
    print 'draw_wave1'
    self.index = index
    #c:self.draw_frame()
    painter = QtGui.QPainter()
    painter.begin(self.offscreen)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.drawLine(0,self.height/2,self.width,self.height/2)
    old_x = 0
    old_y = 0
    index = int(index)
    frames = int(self.source[index].nframes/self.width)
    for i in range(self.width):
      new_x = i
      for j in range(self.width_size):
        new_y = self.source[index].signal[i*frames+int(frames/self.width_size*j)]/2.0**15.0*self.height/2+self.height/2
        painter.drawLine(old_x,int(old_y),new_x,int(new_y))
        old_y = new_y
      old_x = new_x
    painter.end()
    self.update()
    self.wave_palette = self.offscreen


  def reverse(self,x):
    self.reverse_color = QtGui.QColor.fromCmykF(0.40,0.4,0.1,0.2)

    painter = QtGui.QPainter()
    painter.begin(self.offscreen)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
    if self.start_pos < x:
      if x-self.oldpos_x > 0:
        painter.fillRect(self.oldpos_x,0,x-self.oldpos_x,self.height,self.reverse_color)
      elif x-self.oldpos_x < 0:
        painter.fillRect(self.oldpos_x,0,x-self.oldpos_x,self.height,self.back_ground_color)
    elif self.start_pos > x:
      if x-self.oldpos_x < 0:
        painter.fillRect(self.oldpos_x,0,x-self.oldpos_x,self.height,self.reverse_color)
      elif x-self.oldpos_x > 0:
        painter.fillRect(self.oldpos_x,0,x-self.oldpos_x,self.height,self.back_ground_color)
   
    painter.end()
    if self.wave_palette != 0 :
      self.draw_wave(self.index)
    self.redraw()

    self.oldpos_x = x

  def redraw(self):
    self.update()

  def mousePressEvent(self,event):
    self.oldpos_x = event.x()
    self.start_pos = event.x()
    self.draw_frame()
    if self.wave_palette != 0 :
      self.draw_wave(self.index)
    self.redraw()

  def mouseMoveEvent(self,event):
    self.reverse(event.x())

  def setup(self):
    self.setFixedSize(self.width,self.height)
    self.offscreen = QtGui.QPixmap(self.width,self.height)

    self.draw_frame()
    self.update()

  def paintEvent(self,paint_event):
    painter = QtGui.QPainter()
    painter.begin(self)
    painter.drawPixmap(0,0,self.offscreen)
    painter.end()
  
