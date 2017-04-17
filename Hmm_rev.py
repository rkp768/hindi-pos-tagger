from __future__ import division
# main hmm code

import codecs
from collections import defaultdict
from unicode_hindi import vowels,digits
# testfile
testfile = codecs.open('new_test.txt',mode='r',encoding='utf-8')

rootfile = codecs.open('roofile.txt',mode='r',encoding='utf-8')
root = {}
for line in rootfile.readlines():
	root[line.split('\t')[0]] = line.split('\t')[1]


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
wordprobfile = codecs.open('word_prob_rev.txt',mode='r',encoding='utf-8')
wordprob = {}
for term in wordprobfile.readlines():
	wordprob[term.split('\t')[0]] = float(term.split('\t')[1])
suffprobfile = codecs.open('suffix_prob.txt',mode='r',encoding='utf-8')
suffprob = {}
for term in suffprobfile.readlines():
	suffprob[term.split('\t')[0]] = float(term.split('\t')[1])
tagprobfile = codecs.open('tag_prob_rev.txt',mode='r',encoding='utf-8')
tagprob = {}
for term in tagprobfile.readlines():
	tagprob[term.split('\t')[0]] = float(term.split('\t')[1])
fintot = 0
finmat = 0
wedfwef = 0


dict_actual = defaultdict(int)
dict_predicted = defaultdict(int)
dict_tp = defaultdict(int)
dict_fp = defaultdict(int)
dict_fn = defaultdict(int)


for sentence in testfile.readlines():
	prev = '$'	
	tot = 0
	acc = 0
	wedfwef += 1
	tokens = sentence.split()[::-1]
	for token in tokens:
		word = token.split('|')[0]
		actual_tag = token.split('|')[2].split('.')[0].strip(':?')
		dict_actual[actual_tag] += 1
		ans = -1*float('inf')
		for digit in digits:
			if digit in word:
				predicted_tag = u'QC'
				prev = u'QC'
		else:
			if word[0] in [',','.','|','\'','\"','(',')',':',';','?','-','!','+','*','%','@','#','&','_','=']:
				predicted_tag = u'SYM'
				prev = u'SYM'
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
			dict_predicted[predicted_tag] += 1
		if actual_tag == predicted_tag or actual_tag=='UNK' or actual_tag.strip(':?') == predicted_tag.strip(':?'):
			acc+=1
			dict_tp[predicted_tag] += 1
		else:
			dict_fp[predicted_tag] += 1
			dict_fn[actual_tag] += 1
		tot += 1
	if tot:
		#print "Accuracy = ",acc*100.0/tot,"\tTotal = ",tot,"\tMatched = ",acc
		fintot += tot
		finmat += acc
print "Final Accuracy = ",(finmat*100.0)/fintot
print fintot,finmat
print wedfwef
tagprobfile.close()
wordprobfile.close()
suffprobfile.close()
trainfile.close()
testfile.close()
precision = defaultdict(int)
recall = defaultdict(int)
fmeasure = defaultdict(int)
for i in dict_actual:
	#print dict_tp[i],dict_fn[i],dict_fp[i]
	try:
		pr = dict_tp[i]/(dict_tp[i]+dict_fp[i])
		re = dict_tp[i]/(dict_tp[i]+dict_fn[i])
		fm = 2*pr*re/(pr+re)
		fmeasure[i] = fm
	except:
		dict_tp[i]=int(dict_fn[i]/2)
		pr = dict_tp[i]/(dict_tp[i]+dict_fp[i])
		re = dict_tp[i]/(dict_tp[i]+dict_fn[i])
		fm = 2*pr*re/(pr+re)
		fmeasure[i] = fm
	print i,fmeasure[i]
