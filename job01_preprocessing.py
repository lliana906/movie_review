import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('datasets/reviews_2017_2022.csv')
df.info()

df_stopwords= pd.read_csv('datasets/stopwords.csv')
stopwords = df_stopwords['stopword'].tolist()
stopwords = stopwords + ['가다', '감동', '연출',' 연기', '배우', '하다','모르다','주연','보여주다','많다','좋다',]

okt = Okt()
print(df.titles[0])
print(df.reviews[0])
# tokened_reviews = okt.pos(df.reviews[0])
# print(tokened_reviews)

cleaned_sentences = []
for review in df.reviews:
    review = re.sub('[^가-힣]', ' ', review)
    tokened_review = okt.pos(review, stem = True)
    df_token = pd.DataFrame(tokened_review, columns = ['word', 'class'])
    df_token = df_token[(df_token['class'] == 'None') |
                        (df_token['class'] == 'Verd') |
                        (df_token['class'] == 'Adjective')]
    words = []
    for word in df_token['word']:
        if len(word) > 1:
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df.reviews = cleaned_sentences
df.dropna( inplace = True)
df.info()
df.to_csv('datasets/reviews_2017_2022_test.csv', index = False)