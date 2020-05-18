import numpy as np
import pandas as pd
import os
import gensim
path = os.getcwd()

save_model_name = 'doc2vec_v2.model'
saved_path = path + "/doc2vec_v2.model.bin"


def trans2vec(d2v_data):
    train = []
    for i, s in enumerate(d2v_data):
        tokens = s.split(' ')
        train_sentences = gensim.models.doc2vec.TaggedDocument(tokens, [i])
        train.append(train_sentences)
    return train


def recom_music(train_corpus, doc_id):

    inferred_docvec = model.infer_vector(train_corpus[doc_id].words)
    sim_songs = model.docvecs.most_similar([inferred_docvec], topn=5)
    return sim_songs
#     print('%s:\n %s ' % (model, sim_songs))
#     print(lyrics.iloc[doc_id])
#     print(lyrics.iloc[sim_songs[1][0]])

if __name__ == '__main__':
    lyrics = pd.read_csv(path + '\\trainSet.csv')
    d2v_data = pd.Series(lyrics.iloc[:, 0])
    train_corpus = trans2vec(d2v_data)  # 获得模型训练corpus
    model = gensim.models.doc2vec.Doc2Vec.load(saved_path)  # 加载模型
    doc_id = np.random.randint(model.docvecs.count)  # 随机选择一首歌
    sim_songs = recom_music(train_corpus, doc_id)  # 找到这首歌的相似歌曲id
    print(sim_songs)
    # print(lyrics.iloc[doc_id])
    # print(lyrics.iloc[sim_songs[1][0]])