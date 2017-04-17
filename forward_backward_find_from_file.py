#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import codecs
from collections import defaultdict
from unicode_hindi import vowels,digits
# testfile
testfile = codecs.open('hindi_twitter.txt',mode='r',encoding='utf-8')

wrifl = codecs.open('hindi_twitter_op.txt',mode='w',encoding='utf-8')
# all tags
alltags = []
trainfile = codecs.open('new_train.txt',mode='r',encoding='utf-8')
for sentence in trainfile.readlines():
	tokens = sentence.split()
	for token in tokens:
		alltags.append(token.split('|')[2].split('.')[0].strip(':?'))
alltags = list(set(alltags))
print alltags
print len(alltags)

# word prob file 
wordprobfile = codecs.open('word_prob.txt',mode='r',encoding='utf-8')
wordprob = defaultdict(lambda : 1e-8)
for term in wordprobfile.readlines():
	wordprob[term.split('\t')[0]] = float(term.split('\t')[1])

tagprobfile = codecs.open('tag_prob.txt',mode='r',encoding='utf-8')
tagprob = {}
for term in tagprobfile.readlines():
	tagprob[term.split('\t')[0]] = float(term.split('\t')[1])

tagprobfile = codecs.open('tag_prob_rev.txt',mode='r',encoding='utf-8')
tagprob_rev = {}
for term in tagprobfile.readlines():
	tagprob_rev[term.split('\t')[0]] = float(term.split('\t')[1])


dict_actual = defaultdict(int)
dict_predicted = defaultdict(int)

for sentence in testfile.readlines():
	# for forward	
	predicted = []
	prev = '$'
	tokens = sentence.split()
	dic1p = []
	dic1t = []
	words = []
	for token in tokens:
		word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=').strip('|').strip()
		words.append(word)
		ans = -1*float('inf')
		for digit in digits:
			if digit in word:
				predicted_tag = u'QC'
				prev = u'QC'
				ans = 1
		else:
			if (not word) or (word and word[0] in [',','.','|','\'','\"','(',')',':',';','?','-','!','+','*','%','@','#','&','_','=']):
				predicted_tag = u'SYM'
				prev = u'SYM'
				ans = 1
			else:
				word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=')
				for tag in alltags:
					try:
						tp = tagprob[tag+'|'+prev]
					except:
						tp = 1e-8
					try:
						wp = wordprob[word+'|'+tag]
					except:
						wp = 1e-8
					if tp*wp>ans:
						ans = tp*wp
						predicted_tag = tag
				prev = predicted_tag
		dic1p.append(ans)
		dic1t.append(predicted_tag)
	# for backward	
	prev = '$'
	tokens = sentence.split()
	dic2p = []
	dic2t = []
	for token in tokens[::-1]:
		word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=').strip('|').strip()
		ans = -1*float('inf')
		for digit in digits:
			if digit in word:
				predicted_tag = u'QC'
				prev = u'QC'
				ans = 1
		else:
			if (not word) or (word and word[0] in [',','.','|','\'','\"','(',')',':',';','?','-','!','+','*','%','@','#','&','_','=']):
				predicted_tag = u'SYM'
				prev = u'SYM'
				ans = 1
			else:
				word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=').strip('|').strip()
				for tag in alltags:
					try:
						tp = tagprob_rev[tag+'|'+prev]
					except:
						tp = 1e-8
					try:
						wp = wordprob[word+'|'+tag]
					except:
						wp = 1e-8
					if tp*wp>ans:
						ans = tp*wp
						predicted_tag = tag
				prev = predicted_tag
		dic2p.append(ans)
		dic2t.append(predicted_tag)
	acc = 0
	tot = 0
	prev = '$'
	flag = 0
	for i in zip(dic1p,dic2p[::-1],dic1t,dic2t[::-1],words):
		if i[2]==i[3]:
			predicted.append(i[2])
		elif wordprob[i[4]+'|'+i[2]] >wordprob[i[4]+'|'+i[3]]:
			predicted.append(i[2])
		elif wordprob[i[4]+'|'+i[3]] >wordprob[i[4]+'|'+i[2]]:
			predicted.append(i[3])
		else:
			predicted.append(i[2] if wordprob[i[4]+'|'+i[2]] >wordprob[i[4]+'|'+i[3]] else i[3])
	injs = ['अहा','शाबाश','वाह','वाह-वाह','धन्य','अरे','हाय','ओह','रे','ओ','अजी','छि','हट','धत','धिक्']
	for i in zip(predicted, words):
		if i[1].encode('utf-8') in injs:
			wrifl.write(i[1])
			wrifl.write('\t')
			wrifl.write('INJ')
			wrifl.write('\n')
		else:
			wrifl.write(i[1])
			wrifl.write('\t')
			wrifl.write(i[0])
			wrifl.write('\n')	
	wrifl.write('\n\n')
