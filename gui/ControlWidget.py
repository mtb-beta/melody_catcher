#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 17時42分46秒 JST
Note:コントロールパネルを制御するクラス
"""

from PyQt4 import QtCore,QtGui
from PyQt4.phonon import Phonon

class ControlWidget(QtGui.QWidget):
  def __init__(self,control_width,control_height,parent = None):
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

  def set_wave_panel(self,wave_panel):
    self.wave_widget = wave_panel.wave_widget


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

    """
    seekerLayout = QtGui.QHBoxLayout()
    seekerLayout.addWidget(self.seekSlider)
    """

    playbackLayout = QtGui.QHBoxLayout()
    playbackLayout.addWidget(bar)
    playbackLayout.addStretch()
    playbackLayout.addWidget(self.seekSlider)
    playbackLayout.addWidget(volumeLabel)
    playbackLayout.addWidget(self.volumeSlider)
    playbackLayout.addWidget(self.timeLcd)

    mainLayout = QtGui.QVBoxLayout()
    #mainLayout.addWidget(self.musicTable)
    #mainLayout.addLayout(seekerLayout)
    mainLayout.addLayout(playbackLayout)

    self.setLayout(mainLayout)
    self.setFixedSize(self.width,self.height)

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





