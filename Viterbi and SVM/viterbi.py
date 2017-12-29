from __future__ import division
# implements viterbi algorithm

import codecs
from math import log
import operator
from collections import defaultdict,OrderedDict

def viterbi(sentence,Prb_dict,all_tags,D,Trns_P):
	tag_seq = []
	l = len(all_tags)
	all_tags = list(all_tags)
	start_prob = log(1+1/l,2)
	DP_arr = [[0]*l for i in range(len(sentence))]
	OB_arr = [[0]*l for i in range(len(sentence))]
	rows = len(sentence)
	cols = l
	i,j = 0,0
	while i<rows:
		j = 0
		while j<cols:
			if i==0:
				DP_arr[i][j] = start_prob + Prb_dict[sentence[i]+'|'+all_tags[j]]
			else:
				obt_frm = 0
				max_val = -1*float('inf')
				for k in range(cols):
					val = DP_arr[i-1][k]+Trns_P[k][j]
					if val>max_val:
						max_val = val
						obt_frm = k
				DP_arr[i][j] = max_val+Prb_dict[sentence[i]+'|'+all_tags[j]]
				OB_arr[i][j] = obt_frm
			j += 1
		i += 1
	#res = [ DP_arr[-1].index(max(DP_arr[-1])) ] + [0]*(rows-1)
	#print res
	res = []
	lst = DP_arr[-1].index(max(DP_arr[-1]))
	res.append(lst)
	for i in range(rows-1,0,-1):
		lst = OB_arr[i][lst]
		res.append(lst)
	return [all_tags[i] for i in res[::-1]] 

def tag():
	__fTrain = codecs.open("new_train.txt", mode="r", encoding="utf-8")
	__fTest  = codecs.open("tagfile.txt", mode="r", encoding="utf-8")
	
	Dict 	 = defaultdict(int)
	Psb_tags = defaultdict(set)
	
	tag_pairs = []
	for line in __fTrain.readlines():
		tokens = line.split()
		tags = []
		for token in tokens:
			word = token.split('|')[0].strip()
			tag  = token.split('|')[2].split('.')[0].strip(':?').strip()
			if (tag=='I-NP' or tag=='B-NP' or tag=='O'):
				tag='NN'
			tags.append(tag)
			Dict[word+'|'+tag] += 1
			Psb_tags[word] = Psb_tags[word] | set([tag])
		tag_pairs.extend(zip(tags,tags[1:]))

	Prb_dict = defaultdict(int)
	all_tags = set([])
	for word in Psb_tags:
		tags = Psb_tags[word]
		all_tags = all_tags | set(tags)
		vals = [Dict[word+'|'+i] for i in tags]
		prob = [log(1+i/sum(vals), 2) for i in vals]
		for i in zip(tags,prob):
			Prb_dict[word+'|'+i[0]] = i[1]

	D = {v: k for k, v in OrderedDict(enumerate(all_tags)).iteritems()}
	Trns_prob = [[0]*len(all_tags) for i in range(len(all_tags))]
	for i in tag_pairs:
		Trns_prob[ D[i[0]] ][ D[i[1]] ] += 1
	Trns_P = [[0]*len(all_tags) for i in range(len(all_tags))]
	i=0
	while i<len(all_tags):
		j=0
		while j<len(all_tags):
			Trns_P[i][j] = Trns_prob[i][j]/sum(Trns_prob[i])
			j += 1
		i += 1
	sorted_D = sorted(D.items(), key=operator.itemgetter(1))
	__fTrain.close()

	for line in __fTest.readlines():
		try:
			tokens = line.split()
			tags = []
			sentence = []
			for token in tokens:
				word = token.split('|')[0].strip()
				sentence.append(word)
			tag_seq = viterbi(sentence,Prb_dict,all_tags,D,Trns_P)
			print tag_seq
		except:
			print "Couldn't tag sentence ..."
			continue

def test():
	__fTrain = codecs.open("new_train.txt", mode="r", encoding="utf-8")
	__fTest  = codecs.open("new_test.txt", mode="r", encoding="utf-8")

	Dict 	 = defaultdict(int)
	Psb_tags = defaultdict(set)

	tag_pairs = []
	for line in __fTrain.readlines():
		tokens = line.split()
		tags = []
		for token in tokens:
			word = token.split('|')[0].strip()
			tag  = token.split('|')[2].split('.')[0].strip(':?').strip()
			if (tag=='I-NP' or tag=='B-NP' or tag=='O'):
				tag='NN'
			tags.append(tag)
			Dict[word+'|'+tag] += 1
			Psb_tags[word] = Psb_tags[word] | set([tag])
		tag_pairs.extend(zip(tags,tags[1:]))

	Prb_dict = defaultdict(int)
	all_tags = set([])
	for word in Psb_tags:
		tags = Psb_tags[word]
		all_tags = all_tags | set(tags)
		vals = [Dict[word+'|'+i] for i in tags]
		prob = [log(1+i/sum(vals), 2) for i in vals]
		for i in zip(tags,prob):
			Prb_dict[word+'|'+i[0]] = i[1]

	D = {v: k for k, v in OrderedDict(enumerate(all_tags)).iteritems()}
	Trns_prob = [[0]*len(all_tags) for i in range(len(all_tags))]
	for i in tag_pairs:
		Trns_prob[ D[i[0]] ][ D[i[1]] ] += 1
	Trns_P = [[0]*len(all_tags) for i in range(len(all_tags))]
	i=0
	while i<len(all_tags):
		j=0
		while j<len(all_tags):
			Trns_P[i][j] = Trns_prob[i][j]/sum(Trns_prob[i])
			j += 1
		i += 1
	sorted_D = sorted(D.items(), key=operator.itemgetter(1))
	__fTrain.close()
	
	ACC = 0
	toks = 0
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	for line in __fTest.readlines():
		try:
			tokens = line.split()
			tags = []
			sentence = []
			for token in tokens:
				word = token.split('|')[0].strip()
				sentence.append(word)
				tag  = token.split('|')[2].split('.')[0].strip(':?').strip()
				if (tag=='I-NP' or tag=='B-NP' or tag=='O'):
					tag='NN'
				tags.append(tag)
			tag_seq = viterbi(sentence,Prb_dict,all_tags,D,Trns_P)
			acc = 0
			temp_toks = 0
			for i in zip(tag_seq,tags):
				if (i[0]==i[1] and i[0]!='UNK'):
					acc += 1
					ACC += 1
					TP += 1
				else:
					if (i[0]=='UNK' and i[1]=='UNK'):
						TN += 1
					elif (i[0]=='UNK' and i[1]!='UNK'):
						FN += 1
					elif (i[0]!='UNK' and i[1]=='UNK'):
						FP += 1
					elif (i[0]!='UNK' and i[1]!='UNK'):
						FP += 1
				toks += 1
				temp_toks += 1 
			print acc,temp_toks,acc/temp_toks
		except:
			pass
	print ACC,toks,ACC/toks
	print TP,FP,TN,FN
	print "Precision = ", TP/(TP+FP)
	print "Recall = ",TP/(TP+FN)
	print "Accuracy = ",(TP+TN)/(TP+FP+TN+FN)

if __name__ == "__main__":
	tag()