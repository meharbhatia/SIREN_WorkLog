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

def simDoc(text1, text2):
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
	for i in enumerate(text1):
		words = text1
		doc1 = TaggedDocument(words, [i])
	taggeddocs.append(doc1)
	for i in enumerate(text2):
		words = text2
		doc2 = TaggedDocument(words, [i])
	taggeddocs.append(doc2)
	
	#build the modwl
	model = Doc2Vec(dm =0, alpha=0.025, vector_size=20, min_alpha=0.025, min_count=0)
	model.build_vocab(taggeddocs)
	model.train(taggeddocs, epochs=model.iter, total_examples=model.corpus_count)
	
	print("Saved")
	
	similarity = model.n_similarity(text1, text2
	return similarity

#example texts are added! 
f1 = open('C:/Python34/Internship/Algorithms/Algorithm 7/pizza_document.txt', 'r')
text1 = preprocessing(f1.read())

f2 = open('C:/Python34/Internship/Algorithms/Algorithm 7/pizza_document_2.txt', 'r')
text2 = preprocessing(f2.read())


similarity = simDoc(text1, text2)
print("Similarity index: {:4.2f} %".format(similarity*100))
