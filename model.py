import numpy as np
import pandas as pd
import os
import gensim
path = os.getcwd()

save_model_name = 'd2v_10k.model'
saved_path = path + "/d2v_10k.model.bin"


def trans2vec(d2v_data):
    # 转换原始数据为模型训练和infer所需格式
    train = []
    for i, s in enumerate(d2v_data):
        tokens = s.split(' ')
        train_sentences = gensim.models.doc2vec.TaggedDocument(tokens, [i])
        train.append(train_sentences)
    return train


def recom_music(lyrics, train_corpus):
    song_name = input('请输入歌曲名:')
    id = lyrics.loc[lyrics['song_name'] == song_name].index.tolist()
    doc_id = id[0]  # 获得歌曲对应index
    inferred_docvec = model.infer_vector(train_corpus[doc_id].words)
    sim_song = model.docvecs.most_similar([inferred_docvec], topn=5)
    sim_songs = [(lyrics['song_name'].iloc[sim_song[i][0]],lyrics['singer'].iloc[sim_song[i][0]], sim_song[i][1]) for i in range(5)]
    return sim_songs


if __name__ == '__main__':
    lyrics = pd.read_csv(path + '\\trainSet_new.csv')
    d2v_data = pd.Series(lyrics.iloc[:, 0])
    train_corpus = trans2vec(d2v_data)  # 获得模型训练corpus
    model = gensim.models.doc2vec.Doc2Vec.load(saved_path)  # 加载模型
    sim_songs = recom_music(lyrics, train_corpus)  # 找到这首歌的相似歌曲id
    print(sim_songs)