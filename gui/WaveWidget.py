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
    self.wave_palette = 0
    self.sample_rate = 44100.0
    self.time_bar = CurrentTimeBar()

  def set_parameter(self,view_times):
    self.view_times = view_times
    self.width_size = view_times/2
    self.frames = self.view_times*self.sample_rate / self.width
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
    painter.begin(self.offscreen)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.drawLine(0,self.height/2,self.width,self.height/2)
    painter.setPen(QtCore.Qt.black)
    old_x = 0
    old_y = 0
    index = int(index)
    #frames = int(self.source[index].nframes/self.width)
    for x in range(self.width):
      new_x = x
      for j in range(self.width_size):
        new_y = self.source[index].signal[self.current_times*self.sample_rate/10.0+x*self.frames+int(self.frames/self.width_size*j)]/2.0**15.0*self.height/2+self.height/2
        painter.drawLine(old_x,int(old_y),new_x,int(new_y))
        old_y = new_y
      old_x = new_x
    painter.end()
    self.update()
    self.wave_palette = self.offscreen


  def reverse(self,x):
    self.reverse_color = QtGui.QColor.fromCmykF(0.30,0.2,0.2,0.3)

    painter = QtGui.QPainter()
    painter.begin(self.offscreen)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
    if self.start_pos < x:
      if x-self.oldpos_x > 0:
        painter.fillRect(self.oldpos_x,2,x-self.oldpos_x,self.height-4,self.reverse_color)
      elif x-self.oldpos_x < 0:
        painter.fillRect(self.oldpos_x,2,x-self.oldpos_x,self.height-4,self.back_ground_color)
    elif self.start_pos > x:
      if x-self.oldpos_x < 0:
        painter.fillRect(self.oldpos_x,2,x-self.oldpos_x,self.height-4,self.reverse_color)
      elif x-self.oldpos_x > 0:
        painter.fillRect(self.oldpos_x,2,x-self.oldpos_x,self.height-4,self.back_ground_color)
   
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
    self.current_times = index
    print 'index--'
    print index
    self.draw_frame()
    self.draw_wave(self.index)
    self.update()



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
  
class CurrentTimeBar():
  def __init__(self):
    self.time = 0

class WaveSignal():
  def __init__(self,palette,size):
    self.palette = palette
    self.size = size
