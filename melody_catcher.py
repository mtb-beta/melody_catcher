#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月11日 火曜日 16時34分17秒 JST
Note:
"""

from PyQt4 import QtCore,QtGui
from PyQt4.phonon import Phonon
import sys
import wave
import numpy as np
import os.path
import os
from wav import transport_mono_method as wavio


display_width = 1440
display_height =850
control_width = display_width
control_height = 100
wave_width = display_width
wave_height = display_height - control_height -480
midi_width = display_width
midi_height= 480 

class MusicObject():
  def __init__(self,filename):
    self.filepath = str(filename)
    self.filename = os.path.basename(self.filepath)
    print "file"
    print self.filename
    print self.filepath

    wavio.transport_mono_file(self.filepath)
    os.system("mv mono_"+self.filename+" ./sample_data" )
    self.signal = wavio.read_wav("./sample_data/mono_"+self.filename)

    self.nframes = len(self.signal)
    #self.rms(wave_width,wave_height)

  def rms(self,panel_width,panel_height):
    self.rms_signal = np.array([])
    frames = int(self.nframes/panel_width)
    for i in range(panel_width):
      sum = 0
      for j in range(frames):
        sum = sum + (self.signal[j])*(self.signal[j])
      self.rms_signal = np.hstack([self.rms_signal,sum/frames])
    self.rms_signal = self.rms_signal/max(self.rms_signal)*panel_height/2.0

class MidiViewWidget(QtGui.QWidget):
  def __init__(self,parent = None):
    QtGui.QWidget.__init__(self,parent = parent)
    self.width = midi_width-20
    self.height = midi_height-20
    self.width_size = 80
    self.height_size =30
    self.key_width = 100
    self.current_time = 0
    self.setup()

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

class WaveWidget(QtGui.QWidget):
  def __init__(self,parent = None):
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
  
class ControlWidget(QtGui.QWidget):
  def __init__(self,parent = None):
    QtGui.QWidget.__init__(self,parent = parent)
    self.width = control_width-20
    self.height = control_height-20
    self.setup()

  def setup(self):
    """
    コントロールパネルのセットアップ
    """
    self.setupAudio()
    self.sources = []
  def setup2(self,main_window):
    self.setupUi(main_window)
    self.timeLcd.display("00:00:00")

  def set_wave_widget(self,wave_widget):
    self.wave_widget = wave_widget


  def setupUi(self,main_window):
    self.main_window = main_window
    bar = QtGui.QToolBar()
    bar.addAction(self.main_window.playAction)
    bar.addAction(self.main_window.pauseAction)
    bar.addAction(self.main_window.stopAction)

    self.seekSlider = Phonon.SeekSlider(self)
    self.seekSlider.setMediaObject(self.mediaObject)

    self.volumeSlider = Phonon.VolumeSlider(self)
    self.volumeSlider.setAudioOutput(self.audioOutput)
    self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)

    volumeLabel = QtGui.QLabel()
    volumeLabel.setPixmap(QtGui.QPixmap('images/volume.png'))

    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Light,QtCore.Qt.darkGray)

    self.timeLcd = QtGui.QLCDNumber()
    self.timeLcd.setPalette(palette)

    headers = ('title','artist','album','year')
    
    self.musicTable = QtGui.QTableWidget(0,4)
    self.musicTable.setHorizontalHeaderLabels(headers)
    self.musicTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.musicTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.musicTable.cellPressed.connect(self.tableClicked)

    seekerLayout = QtGui.QHBoxLayout()
    seekerLayout.addWidget(self.seekSlider)

    playbackLayout = QtGui.QHBoxLayout()
    playbackLayout.addWidget(bar)
    playbackLayout.addStretch()
    playbackLayout.addWidget(volumeLabel)
    playbackLayout.addWidget(self.volumeSlider)
    playbackLayout.addWidget(self.timeLcd)

    mainLayout = QtGui.QVBoxLayout()
    mainLayout.addWidget(self.musicTable)
    mainLayout.addLayout(seekerLayout)
    mainLayout.addLayout(playbackLayout)

    self.setLayout(mainLayout)

  def tableClicked(self,row,column):
    wasPlaying = (self.mediaObject.state() == Phonon.PlayingState)
    self.mediaObject.stop()
    self.mediaObject.clearQueue()#TO DO
    self.mediaObject.setCurrentSource(self.sources[row])

    if wasPlaying:
      self.mediaObject.play()
    else:
      self.mediaObject.stop()




  def setupAudio(self):
    """
    オーディオ関連のセットアップ
    """

    self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory,self)
    self.mediaObject = Phonon.MediaObject(self)
    self.metaInformationResolver =Phonon.MediaObject(self)
    self.mediaObject.setTickInterval(1000)

    self.mediaObject.tick.connect(self.tick)#
    self.mediaObject.stateChanged.connect(self.stateChange)
    self.metaInformationResolver.stateChanged.connect(self.metaStateChanged)
    self.mediaObject.currentSourceChanged.connect(self.sourceChanged)

    self.mediaObject.aboutToFinish.connect(self.aboutToFinish)
    Phonon.createPath(self.mediaObject,self.audioOutput)

  def sizeHint(self):
    return QtCore.QSize(500,300)


  def aboutToFinish(self):
    """
    楽曲の再生が終了した時に実行される関数
    """
    index = self.sources.index(self.mediaObject.currentSource()) + 1
    if len(self.sources) > index:
        self.mediaObject.enqueue(self.sources[index])


  def sourceChanged(self,source):
    """
    再生するファイルが変更された時に実行される関数
    """
    self.wave_index = str(self.sources.index(source))
    self.musicTable.selectRow(self.sources.index(source))
    self.timeLcd.display('00:00:00')
    self.wave_widget.draw_wave(self.wave_index)

  def metaStateChanged(self,newState,oldState):
    """
    参照するファイルが追加された時に実行される関数
    """
    if newState == Phonon.ErrorState:
      QtGui.QMessageBox.warning(self,"Error opening files",
          self.metaInformatinonResolver.errorString())

      while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
        pass
      return
    
    if newState != Phonon.StoppedState and newState != Phonon.PausedState:
      return

    if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
      return

    metaData = self.metaInformationResolver.metaData()

    title = metaData.get("TITLE",[''])[0]
    if not title:
      title = self.metaInformationResolver.currentSource().fileName()

    titleItem = QtGui.QTableWidgetItem(title)
    titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

    artist = metaData.get('ARTIST',[''])[0]
    artistItem = QtGui.QTableWidgetItem(artist)
    artistItem.setFlags(artistItem.flags() ^ QtCore.Qt.ItemIsEditable)
    
    album = metaData.get('ALBUM',[''])[0]
    albumItem = QtGui.QTableWidgetItem(album)
    albumItem.setFlags(albumItem.flags() ^ QtCore.Qt.ItemIsEditable)

    year = metaData.get('DATE',[''])[0]
    yearItem = QtGui.QTableWidgetItem(year)
    yearItem.setFlags(yearItem.flags() ^ QtCore.Qt.ItemIsEditable)

    currentRow = self.musicTable.rowCount()
    self.musicTable.insertRow(currentRow)
    self.musicTable.setItem(currentRow,0,titleItem)
    self.musicTable.setItem(currentRow,1,artistItem)
    self.musicTable.setItem(currentRow,2,albumItem)
    self.musicTable.setItem(currentRow,3,yearItem)

    if not self.musicTable.selectedItems():
      self.musicTable.selectRow(0)
      self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())
    index =self.sources.index(self.metaInformationResolver.currentSource()) + 1


    if len(self.sources) > index :
      self.metaInformationResolver.setCurrentSource(self.sources[index])
    else :
      self.musicTable.resizeColumnsToContents()
      if self.musicTable.columnWidth(0)> 300:
        self.musicTable.setColumnWidth(0,300)
    self.wave_widget.draw_wave(self.wave_index)



  def tick(self,time):
    """
    tickが更新された際に動作する関数
    """
    displayTime  = QtCore.QTime(0,(time/60000) % 60,(time /1000) % 60 )
    self.timeLcd.display(displayTime.toString('mm:ss'))

  def stateChange(self,newState,oldState):
    """
    メディアオブジェクトのステータスが変更された際に動作する関数
    """
    if newState == Phonon.ErrorState:
      if self.mediaObject.erroType() == Phonon.FatalError:
        QtGui.QMessageBox.warning(self,"Fatal Error",
          self.mediaObject.errorString())
      else:
        QtGui.QMessageBox.warnings(self,"Error",
            self.mediaObject.errorString())
    elif newState == Phonon.PlayingState:
      self.main_window.playAction.setEnabled(False)
      self.main_window.pauseAction.setEnabled(True)
      self.main_window.stopAction.setEnabled(True)
    elif newState == Phonon.StoppedState:
      self.main_window.stopAction.setEnabled(False)
      self.main_window.playAction.setEnabled(True)
      self.main_window.pauseAction.setEnabled(False)
      self.timeLcd.display("00:00:00")
    elif newState == Phonon.PausedState:
      self.main_window.pauseAction.setEnabled(False)
      self.main_window.stopAction.setEnabled(True)
      self.main_window.playAction.setEnabled(True)



class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(QtGui.QMainWindow,self).__init__()
    self.setup()
  def setup(self):
    self.control_widget  = ControlWidget()
    self.wave_widget = WaveWidget()
    self.midi_view_widget = MidiViewWidget()
    self.control_widget.set_wave_widget(self.wave_widget)

    # 縦に並ぶレイアウト
    self.MainLayout = QtGui.QVBoxLayout()

    self.MainLayout.addWidget(self.control_widget)
    self.MainLayout.addWidget(self.wave_widget)
    self.MainLayout.addWidget(self.midi_view_widget)

    self.Panel = QtGui.QWidget()
    self.Panel.setLayout(self.MainLayout)

    self.Panel.setFixedSize(display_width,display_height)

    self.setWindowTitle("melody")
    self.setCentralWidget(self.Panel)
    self.setupActions()
    self.control_widget.setupUi(self)
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
        triggered=self.control_widget.mediaObject.play)

    self.pauseAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaPause),"Pause",
        self,shortcut="Ctrl+A",enabled=False,
        triggered=self.control_widget.mediaObject.pause)

    self.stopAction = QtGui.QAction(
        self.style().standardIcon(QtGui.QStyle.SP_MediaStop),"Stop",
        self,shortcut="Ctrl+S",enabled=False,
        triggered=self.control_widget.mediaObject.stop)

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

    index = len(self.control_widget.sources)

    for string in files:
      self.control_widget.sources.append(Phonon.MediaSource(string))

    if self.control_widget.sources:
      self.control_widget.metaInformationResolver.setCurrentSource(self.control_widget.sources[index])
      self.wave_widget.source.append(MusicObject(self.control_widget.metaInformationResolver.currentSource().fileName()))
      self.wave_widget.draw_wave(index)


def main():

  app = QtGui.QApplication(sys.argv)
  app_window = MainWindow()
  app_window.show()

  app.exec_()

if __name__ == "__main__":
  main()
