#!/usr/bin/env python3
# coding: utf-8
"""
歌唱データベースの音声ファイルからブレスを切り出すスクリプト
"""

import os
import sys
from glob import glob

from pydub import AudioSegment

import utaupy

TARGET_PHONEME = 'br'


def main():
    """
    音声ファイルとラベルファイルを指定
    ラベルファイルを読み取る
    ラベルファイルのうち特定の音素の開始・終了時刻を取得
    音声ファイルを切断
    音声ファイルを保存
    """
    labdir = input('LABのフォルダを指定してください : ').strip(r'"')
    wavdir = input('WAVのフォルダを指定してください : ').strip(r'"')
    dirname = input('目印にしたい文字列を入力してください :')
    labfiles = glob(f'{labdir}/*.lab')
    wavfiles = glob(f'{wavdir}/*.wav')
    # 曲ごとのフォルダな場合は再帰的に検索
    if max(len(labfiles), len(wavfiles)) == 0:
        print('  LABとWAVが0個なので再帰的に検索して続行します。')
        labfiles = glob(f'{labdir}/**/*.lab', recursive=True)
        wavfiles = glob(f'{wavdir}/**/*.wav', recursive=True)
    # ファイルの個数が合わないときはエラーで終了
    if len(labfiles) != len(wavfiles):
        print(f'  LABファイルとWAVファイルの個数が合いません。({len(labfiles)}, {len(wavfiles)})')
        print('  ファイル名が対応していること、個数が一致することを確認してやり直してください。')
        input('Enterを押すと終了します。')
        sys.exit()

    print(f'対象のLABとWAVは{len(labfiles)}個です。')
    print('処理を始めます。')
    os.makedirs(f'./out/{dirname}', exist_ok=False)
    for labfile, wavfile in zip(labfiles, wavfiles):
        small_label = extract_label(labfile, TARGET_PHONEME)
        cutout_wav(wavfile, small_label, dirname)
    print('処理が終わりました。')
    input('Enterを押すと終了します。')


def extract_label(labfile, target_phoneme):
    """切り出したい音素のみのラベルを返す(単位は100ns)"""
    label = utaupy.label.load(labfile)

    l = []  # [[音素, 開始時刻, 終了時刻], [], ...]
    for v in label:
        if v.symbol == target_phoneme:
            l.append(v)
    return l


def cutout_wav(wavfile, l, dirname):
    """
    wavfile中の指定区間を切り出す。
    l は [[音素, 開始時刻, 終了時刻], [], ...] の2次元リスト
    """
    songname = os.path.splitext(os.path.basename(wavfile))[0]
    # wavファイルの読み込み
    sound = AudioSegment.from_file(wavfile, format='wav')

    # ミリ秒で区間指定して抽出
    for i, v in enumerate(l):
        # 100ns(10^-7)をms(10^-3)に変換
        t_start = int(v.start // 10000)
        t_end = int(v.end // 10000)
        # 出力パスを設定
        # './out/(任意文字列)/(音素)_(元の名前)_000001.wav'
        outpath = f'./out/{dirname}/{v.symbol}_{songname}_{(i+1):06}.wav'
        # '(出力パス)tab(音声の長さ)'
        print(f'    {outpath}\t{t_end - t_start}ms')
        # 指定音素区間を切り出し
        cutsound = sound[t_start:t_end]
        # ファイル出力
        cutsound.export(outpath, format='wav')


if __name__ == '__main__':
    main()
