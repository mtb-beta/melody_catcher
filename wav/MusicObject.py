#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012年 12月17日 月曜日 17時30分04秒 JST
Note:楽曲ファイルを制御するクラス
"""
import wave
import os
from wav import transport_mono_method as wavio

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

    def Cutout(self,start,end):
        #print 'cutout'
        wf_o = wave.open('./sample_data/tmp.wav','wb')
        wf_o.setnchannels(1)
        wf_o.setsampwidth(2)
        wf_o.setframerate(44100)
        wf_o.setcomptype('NONE','not compressed')

        outData = self.signal[start:start + end]

        wf_o.writeframes(outData.tostring())
        wf_o.close()
