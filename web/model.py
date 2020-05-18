import numpy as np
import pandas as pd
import os
import gensim
import pickle

saved_path = "./model/doc2vec_v2.model.bin"

def load():
	lyrics = pd.read_csv('./model/trainSet_new.csv')
	dbfile = open('./model/train_corpus', 'rb')      
	train_corpus = pickle.load(dbfile)
	dbfile.close() 
	model = gensim.models.doc2vec.Doc2Vec.load(saved_path)  # 加载模型
	return lyrics, train_corpus, model

def recom_music(lyrics, train_corpus, model, song_name):
    # song_name = input('请输入歌曲名:')
    id = lyrics.loc[lyrics['song_name'] == song_name].index.tolist()
    doc_id = id[0]  # 获得歌曲对应index
    inferred_docvec = model.infer_vector(train_corpus[doc_id].words)
    sim_song = model.docvecs.most_similar([inferred_docvec], topn=5)
    sim_songs = [(lyrics['song_name'].iloc[sim_song[i][0]],lyrics['singer'].iloc[sim_song[i][0]], sim_song[i][1]) for i in range(5)]
    return sim_songs