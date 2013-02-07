#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2013年 1月26日 土曜日 21時36分08秒 JST
Note:wavファイルの書き出しサンプル
"""

import wave
import numpy as np
from pylab import*


wf_o = wave.open('tmp.wav','wb')
wf_o.setnchannels(1)
wf_o.setsampwidth(2)
wf_o.setframerate(44100)
wf_o.setcomptype("NONE",'not compressed')

f0 = 1000
t = np.arange(44100 * 3)
signal = np.sin(f0 * t * 2 * np.pi / 44100)

signal = np.int16(signal)*2**14

#plot(signal)
#show()
for i in range(len(signal)):
    wf_o.writeframes(signal[i].tostring())
wf_o.close()
