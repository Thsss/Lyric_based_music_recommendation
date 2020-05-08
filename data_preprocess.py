import pandas as pd
import numpy as np
import re

def loadData():
    csv_data = pd.read_csv('lyrics.csv', encoding='UTF-8').astype(str)
    df = pd.DataFrame(csv_data)
    # 删除singer列
    df = df.drop('singer', axis=1)
    # 删除NAN
    df = df.dropna(axis=0, how='any')
    # 删除纯音乐
    df = df[~df['lyrics'].str.contains('纯音乐')]
    df = df[~df['lyrics'].str.contains('暂时没有歌词')]
    df = df[~df['lyrics'].str.contains('节选自')]
    df.index = range(0, len(df))
    return pd.DataFrame(df)

def filterLyrics(data):
    for i in range(np.shape(data)[0]):
        lyrics = data.iloc[i]['lyrics']
        # 删除特殊符号
        p = re.compile(r"[~～`\\\·\!\！\@\#\$\%\^\&\*\{\}\[\]《》「」<>\?\？,\.，。、’‘“”ㄟ;；×——_=\+……\^\'\"a-zA-Z0-9]")
        lyrics = re.sub(p, "", lyrics)
        # 删除括号间的内容
        lyrics = re.sub(u"\\（.*?）", "", lyrics)
        lyrics = re.sub(u"\\(.*?\\)", "", lyrics)
        lyrics = re.sub(u"\\（.*?\\)", "", lyrics)
        lyrics = re.sub(u"\\(.*?）", "", lyrics)
        lyrics = re.sub(u"\\〔.*?〕", "", lyrics)
        lyrics = re.sub(u"\\【[\u4e00-\u9fa5]*( )*:", "", lyrics)
        lyrics = re.sub(u"\\【[\u4e00-\u9fa5]*( )*：", "", lyrics)
        p = re.compile(r"[【】（）\(\)]")
        lyrics = re.sub(p, "", lyrics)
        # 删除多余的空格
        lyrics = re.sub(u" +", " ", lyrics)
        # 过滤掉工作人员
        lyrics = re.sub(r"[\u4e00-\u9fa5]*( )*:( )*[\u4e00-\u9fa5]*( )*", "", lyrics)
        lyrics = re.sub(r"[\u4e00-\u9fa5]*( )*：( )*[\u4e00-\u9fa5]*( )*", "", lyrics)
        lyrics = re.sub(r"/( )*[\u4e00-\u9fa5]*( )*", "", lyrics)
        lyrics = re.sub(r"/( )*[\u4e00-\u9fa5]*( )*", "", lyrics)
        # 过滤A--B
        lyrics = re.sub(r"[\u4e00-\u9fa5]*(\-)+[\u4e00-\u9fa5]*", "", lyrics)
        # 删除空格
        lyrics = re.sub(u" +", "", lyrics)
        data.iloc[i]['lyrics'] = lyrics
    return data
    # print(data.head(100))
    # column_1 = data['lyrics'].str.extract('([\u4e00-\u9fa5 ]+)', expand=True)
    # column_2 = data['song_name']
    # df = pd.concat([column_1, column_2], axis=1)
    # print(df.head(100))

def filterName(data):
    for i in range(np.shape(data)[0]):
        song_name = data.iloc[i]['song_name']
        song_name = re.sub(u"\\（.*?）", "", song_name)
        song_name = re.sub(u"\\(.*?\\)", "", song_name)
        song_name = re.sub(u"\\（.*?\\)", "", song_name)
        song_name = re.sub(u"\\(.*?）", "", song_name)
        data.iloc[i]['song_name'] = song_name
    return data

# 判断是否是中文歌
def isChinese(data):
    drop_index = []
    for i in range(np.shape(data)[0]):
        lyrics = data.iloc[i]['lyrics']
        res = ' '.join([r for r in re.findall(r"[\u4e00-\u9fa5]+", lyrics)])
        # 删除中文占比少于80%的歌
        if len(res) < len(lyrics)*0.8:
            drop_index.append(i)
    data = data.drop(drop_index,axis=0)
    data.index = range(0, len(data))
    return data

def getCleanData(data):
    drop_index = []
    for i in range(np.shape(data)[0]):
        lyrics = data.iloc[i]['lyrics']
        if len(lyrics) <= 10:
            drop_index.append(i)
    data = data.drop(drop_index, axis=0)
    data.index = range(0, len(data))
    return data

if __name__=='__main__':
    df = loadData()
    df = filterLyrics(df)
    df = filterName(df)
    df = isChinese(df)
    cleanData = getCleanData(df)
    cleanData.to_csv('clean_data.csv', index=False)