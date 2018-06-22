import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import warnings
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

stopwords_en = stopwords.words("english")

def preprocessing(raw):
	wordlist = nltk.word_tokenize(raw)
	text = [w.lower () for w in wordlist if w not in stopwords_en]
	return text

#example texts are added! 
f1 = open('C:/Python34/Internship/Algorithms/Algorithm 7/pizza_document.txt', 'r')
text1 = preprocessing(f1.read())

f2 = open('C:/Python34/Internship/Algorithms/Algorithm 7/pizza_document_2.txt', 'r')
text2 = preprocessing(f2.read())

word_set = set(text1).union(set(text2))

freqd_text1 = FreqDist(text1)
text1_count_dict = dict.fromkeys(word_set, 0)
for word in text1:
	text1_count_dict[word] = freqd_text1[word]

freqd_text2 = FreqDist(text2)
text2_count_dict = dict.fromkeys(word_set, 0)
for word in text2:
	text2_count_dict[word] = freqd_text2[word]

taggeddocs = []
doc1 = TaggedDocument(words = text1, tags = [u'NEWS_1'])
taggeddocs.append(doc1)
doc2 = TaggedDocument(words = text2, tags = [u'NEWS_2'])
taggeddocs.append(doc2)

#build the modwl
model = Doc2Vec(taggeddocs, dm =0, alpha=0.025, size=20, min_alpha=0.025, min_count=0)
#training
'''for epoch in range(60):
	if epoch % 20 == 0:
		print('Now training epoch %s' % epoch)
	model.train(taggeddocs)
	model.alpha -=0.002 #decrease the learning rate
	model.min_alpha = model.alpha #fix the learning rate, no decay
'''
model.train(taggeddocs, epochs=model.iter, total_examples=model.corpus_count)

similarity = model.n_similarity(text1, text2)
print("Similarity index: {:4.2f} %".format(similarity*100))

#for above two documents Similarity is 77.77%


