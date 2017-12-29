# -*- coding: utf-8 -*-

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_recall_fscore_support

fTrn = open("train.txt",mode='r')
fTst = open("test.txt",mode='r')

def features(sentence, tags, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
	#'prev-tag':'' if index == 0 else tags[index - 1],
	#'next-tag':'' if index == len(sentence) - 1 else tags[index + 1],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
	'suffix-4': sentence[index][-4:],
	'suffix-5': sentence[index][-5:],
	'suffix-6': sentence[index][-6:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
    }

trn_X = []
tst_X = []
trn_Y = []
tst_Y = []
for i in fTrn.readlines():
	sentence = [w.split('|')[0] for w in i.split()]
	tags_  = [w.split('|')[-1].split('.')[0] for w in i.split()]
	tags = []
	for i in tags_:
		if i in ['I-NP','B-NP','O']:
			tags.append('NN')
		elif i.endswith(':?'):
			tags.append(i.split(':?')[0])
		else:
			tags.append(i)
	temp = []
	for i in range(len(sentence)):
		trn_X.append(features(sentence,tags,i))
		trn_Y.append(tags[i])

for i in fTst.readlines():
	sentence = [w.split('|')[0] for w in i.split()]
	tags_  = [w.split('|')[-1].split('.')[0] for w in i.split()]
	tags = []
	for i in tags_:
		if i in ['I-NP','B-NP','O']:
			tags.append('NN')
		elif i.endswith(':?'):
			tags.append(i.split(':?')[0])
		else:
			tags.append(i)
	temp = []
	for i in range(len(sentence)):
		tst_X.append(features(sentence,tags,i))
		tst_Y.append(tags[i])

# train model
clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', SVC())
])
clf.fit(trn_X[:10000],trn_Y[:10000])
print "Accuracy : ",clf.score(tst_X[:5000],tst_Y[:5000])
print "Scores prec,rec,fm : ",precision_recall_fscore_support(y_true, y_pred, average='macro')
	
# close files
fTrn.close()
fTst.close()
