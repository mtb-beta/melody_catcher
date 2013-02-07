#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author:mtb_beta
Date:
2013年 1月 9日 水曜日 21時02分14秒 JST
Note:PreFestで作成されたxmlファイルの解析
"""

from xml.etree.ElementTree import *

def readxml(filename):
    # ファイル読み込み
    tree = parse(filename)
    root = tree.getroot()

    # メタデータの辞書の作成
    meta = {}
    for M in root[0]:
        meta.update({M.items()[1][1]:M.items()[0][1]})

    a = []
    for child in root:
        a.append(child.attrib)

    # データ内容について
    dim = int(a[1]['dim']) # 音階の数
    frames = int(a[1]['frames']) # 総フレーム数

    # データ列
    data = root[1].text

    # データ列を改行で分割
    data = data.split('\n')

    # データ列の返り値の格納リスト
    pitch = []

    # データ列のリストを半角スペースで分割
    for w in data:
        pitch.append(w.split(' '))

    # データ列のリストの中に含まれる''を削除
    for list in pitch:
        while '' in list:
            list.remove('')

    # データ列のリストの中に含まれる[]を削除
    while [] in pitch:
        pitch.remove([])

    # データ列のリストに格納されている各値をstrからfloatへ変更
    for i in range(len(pitch)):
        for j in range(len(pitch[i])):
            pitch[i][j] = float(pitch[i][j])
    
    return pitch,dim,frames,meta

if __name__ == '__main__':
    pitch,dim,frames,meta = readxml('output.xml')
    
    print pitch
    print dim
    print frames
    print meta
