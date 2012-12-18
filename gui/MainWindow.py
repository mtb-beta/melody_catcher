#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 17時51分14秒 JST
Note:メインウィンドウを制御するクラス
"""
from PyQt4 import QtCore,QtGui
from wav.MusicObject import*
from gui.MidiViewWidget import*
from gui.WaveWidget import*
from gui.ControlPanel import*



class MainWindow(QtGui.QMainWindow):
  def __init__(self,display_width,display_height):
    super(QtGui.QMainWindow,self).__init__()
    self.display_width = display_width
    self.display_height = display_height
    self.control_width = display_width
    self.control_height = 100
    self.wave_width = display_width
    self.wave_height = display_height - self.control_height -480
    self.midi_width = display_width
    self.midi_height= 480 

    self.setup()
  def setup(self):
    self.control_panel  = ControlPanel('Control',self.control_width,self.control_height)
    #self.control_widget  = ControlWidget(self.control_width,self.control_height)
    self.wave_widget = WaveWidget(self.wave_width,self.wave_height)
    self.midi_view_widget = MidiViewWidget(self.midi_width,self.midi_height)
    self.control_panel.control_widget.set_wave_widget(self.wave_widget)

    # 縦に並ぶレイアウト
    self.MainLayout = QtGui.QVBoxLayout()

    self.MainLayout.addWidget(self.control_panel.control_widget)
    self.MainLayout.addWidget(self.wave_widget)
    self.MainLayout.addWidget(self.midi_view_widget)

    self.Panel = QtGui.QWidget()
    self.Panel.setLayout(self.MainLayout)

    self.Panel.setFixedSize(self.display_width,self.display_height)

    self.setWindowTitle("melody")
    self.setCentralWidget(self.Panel)
    self.setupActions()
    self.control_panel.control_widget.setupUi(self)
    self.setupMenus()

  def setupMenus(self):
    fileMenu = self.menuBar().addMenu("&File")

    fileMenu.addAction(self.addFilesAction)
    fileMenu.addSeparator()
    fileMenu.addAction(self.exitAction)

    aboutMenu = self.menuBar().addMenu("&Help")
    aboutMenu.addAction(self.aboutAction)
    aboutMenu.addAction(self.aboutQtAction)

  def setupActions(self):
    self.playAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaPlay),"Play",
        self,shortcut="Ctrl+P",enabled=False,
        triggered=self.control_panel.control_widget.mediaObject.play)

    self.pauseAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaPause),"Pause",
        self,shortcut="Ctrl+A",enabled=False,
        triggered=self.control_panel.control_widget.mediaObject.pause)

    self.stopAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaStop),"Stop",
        self,shortcut="Ctrl+S",enabled=False,
        triggered=self.control_panel.control_widget.mediaObject.stop)

    self.nextAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward),
        "Next",self,shortcut="Ctrl+N")

    self.previousAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward),
        "Previous", self, shortcut="Ctrl+R")

    self.addFilesAction = QtGui.QAction("Add &Files", self,
        shortcut="Ctrl+F", triggered=self.addFiles)

    self.exitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
        triggered=self.close)

    self.aboutAction = QtGui.QAction("A&bout", self, shortcut="Ctrl+B",
        triggered=self.about)

    self.aboutQtAction = QtGui.QAction("About &Qt", self,
        shortcut="Ctrl+Q", triggered=QtGui.qApp.aboutQt)


  def about(self):
    QtGui.QMessageBox.information(self,"About Melody Catcher",
        "The Melody Catcher show melody part "
        "within your disignated area pich about object music file.")

  def addFiles(self):
    files = QtGui.QFileDialog.getOpenFileNames(self,"Select Music Files",
        QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation),
        "Audio(*.wav)")

    if not files:
      return

    index = len(self.control_panel.control_widget.sources)

    for string in files:
      self.control_panel.control_panel.control_widget.sources.append(Phonon.MediaSource(string))

    if self.control_panel.control_widget.sources:
      self.control_panel.control_widget.metaInformationResolver.setCurrentSource(self.control_panel.control_widget.sources[index])
      self.wave_widget.source.append(MusicObject(self.control_panel.control_widget.metaInformationResolver.currentSource().fileName()))
      self.wave_widget.draw_wave(index)
