#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 11時40分55秒 JST
Note:スライダーを統括するクラス。
"""

from PyQt4 import QtCore,QtGui

class Slider(QtGui.QGroupBox):
  valueChanged =QtCore.pyqtSignal(int)
  def __init__(self,orientation,title,parent=None):
    super(Slider,self).__init__(title,parent)

    self.scrollBar = QtGui.QScrollBar(orientation)
    self.scrollBar.setFocusPolicy(QtCore.Qt.StrongFocus)

    self.scrollBar.valueChanged.connect(self.scroll)

    self.layout = QtGui.QHBoxLayout()
    self.layout.addWidget(self.scrollBar)

    self.setLayout(self.layout)

  def scroll(self,event):
    print 'scroll'
    print 'event:'+str(event)
    print type(event)

  def setMinimum(self,value):
    self.scrollBar.setMinimum(value)

  def setMaximum(self,value):
    self.scrollBar.setMaximum(value)

  def invertAppearance(self,invert):
    self.scrollBar.setInvertedAppearance(invert)

  def invertKeyBindings(self,invert):
    self.scrollbar.setInvertedControls(invert)

class Window(QtGui.QWidget):
  def __init__(self):
    super(Window,self).__init__()

    self.slider = Slider(QtCore.Qt.Horizontal,'Horizontal')
    self.slider.setMinimum(100)
    self.slider.setMaximum(200)

    self.button = QtGui.QPushButton('Button')

    self.Layout= QtGui.QHBoxLayout()
    self.Layout.addWidget(self.slider)
    self.Layout.addWidget(self.button)
    self.setLayout(self.Layout)


if __name__ == '__main__':


  import sys

  app = QtGui.QApplication(sys.argv)
  window = Window()
  window.show()
  sys.exit(app.exec_())
