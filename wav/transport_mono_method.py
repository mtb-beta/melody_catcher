#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2012Ç¯ 11·î 3Æü ÅÚÍËÆü 22»þ06Ê¬20ÉÃ JST
Note:This method is that stereo wave file transport mono wave file
"""
import wave
import numpy as np
import os.path
import os


#main method
def transport_mono_file(filepath):
  filename = os.path.basename(filepath)

  # chunk is number processing at a time
  chunk =1024

  # wf_in is input stereo wave file
  wf_in =wave.open(filepath,'rb')

  print "wf"
  print wf_in.getnchannels()

  if wf_in.getnchannels() != 1:
    # output file name
    output_file = 'mono_'+filename

    # preparation output wave file
    wf_out =wave.open(output_file,'wb')

    # output file is mono
    wf_out.setnchannels(1)

    # output file is 16bit samples
    wf_out.setsampwidth(2)

    # output file's sample rate is 441000.
    wf_out.setframerate(44100)

    # remain is input file's frame sum.
    remain = wf_in.getnframes()

    #repeat input file frame end
    while remain >0:
      # check object frame remain chunk
      s = min(chunk,remain)

      # data is read frame
      data = wf_in.readframes(s)

      # data transport numpy.int16 because data is string.
      ary =np.fromstring(data,np.int16)

      # L and R pull each signal
      left =np.int32(ary[::2])
      right = np.int32(ary[1::2])

      # ary2 is mean L and R signal power.
      ary2=np.int16((left+right)/2)

      # Because ary2 is int16,it transport string and substitute data2.
      data2 = ary2.tostring()

      # output file add a postscript which data2
      wf_out.writeframes(data2)

      # remain substract already process data.
      remain = remain-s
    wf_out.close()
  else:
    os.system("cp "+filepath+" mono_"+filename)

  wf_in.close()


def read_wav(filename):
  wf = wave.open(filename,'rb')
  data = wf.readframes(wf.getnframes())
  ary=np.fromstring(data,np.int16)

  return ary



if __name__=="__main__":
  filename = "mix_sample.wav"
  transport_mono_file(filename)
