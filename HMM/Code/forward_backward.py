from __future__ import division

import codecs
from collections import defaultdict
from unicode_hindi import vowels,digits
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

# testfile
testfile = codecs.open('data/new_test.txt',mode='r',encoding='utf-8')


# all tags
alltags = []
trainfile = codecs.open('data/new_train.txt',mode='r',encoding='utf-8')
for sentence in trainfile.readlines():
	tokens = sentence.split()
	for token in tokens:
		alltags.append(token.split('|')[2].split('.')[0].strip(':?'))
alltags = list(set(alltags))
print alltags
print len(alltags)

# word prob file 
wordprobfile = codecs.open('data/word_prob.txt',mode='r',encoding='utf-8')
wordprob = {}
for term in wordprobfile.readlines():
	wordprob[term.split('\t')[0]] = float(term.split('\t')[1])

tagprobfile = codecs.open('data/tag_prob.txt',mode='r',encoding='utf-8')
tagprob = {}
for term in tagprobfile.readlines():
	tagprob[term.split('\t')[0]] = float(term.split('\t')[1])

tagprobfile = codecs.open('data/tag_prob_rev.txt',mode='r',encoding='utf-8')
tagprob_rev = {}
for term in tagprobfile.readlines():
	tagprob_rev[term.split('\t')[0]] = float(term.split('\t')[1])

finacc = 0
fintot = 0
totsent = 0
TP = 0
FP = 0
TN = 0
FN = 0



dict_actual = defaultdict(int)
dict_predicted = defaultdict(int)
dict_tp = defaultdict(int)
dict_fp = defaultdict(int)
dict_fn = defaultdict(int)
y_true = []
y_pred = []
for sentence in testfile.readlines():
	# for forward	
	prev = '$'
	tokens = sentence.split()
	dic1p = []
	dic1t = []
	actual_tags = []
	words = []
	for token in tokens:
		word = token.split('|')[0]
		actual_tags.append(token.split('|')[2].split('.')[0].strip(':?'))
		words.append(token.split('|')[0])
		ans = -1*float('inf')
		for digit in digits:
			if digit in word:
				predicted_tag = u'QC'
				prev = u'QC'
				ans = 1
		else:
			if word[0] in [',','.','|','\'','\"','(',')',':',';','?','-','!','+','*','%','@','#','&','_','=']:
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
		word = token.split('|')[0]
		actual_tag = token.split('|')[2].split('.')[0].strip(':?')
		ans = -1*float('inf')
		for digit in digits:
			if digit in word:
				predicted_tag = u'QC'
				prev = u'QC'
				ans = 1
		else:
			if word[0] in [',','.','|','\'','\"','(',')',':',';','?','-','!','+','*','%','@','#','&','_','=']:
				predicted_tag = u'SYM'
				prev = u'SYM'
				ans = 1
			else:
				word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=')
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
	try:
		acc = 0
		tot = 0
		prev = '$'
		flag = 0
		predicted = []
		for i in zip(dic1p,dic2p[::-1],dic1t,dic2t[::-1],actual_tags,words):
			#if tot == 0:
			#	if i[2]==i[3] and i[2]==i[4]:
			#		acc+=1
			#		predicted.append(i[4])	
			#		TP += 1				
			#	elif tagprob[i[2]+'|'+'$'] >tagprob[i[3]+'|'+'$']  and i[2]==i[4]:
			#		acc+=1
			#		predicted.append(i[4])
			#		TP += 1
			#	elif tagprob[i[3]+'|'+'$'] > tagprob[i[2]+'|'+'$'] and i[3]==i[4]:
			#		acc+=1
			#		flag = 1
			#		predicted.append(i[4])
			#		TP += 1
			#	#elif i[4]=='UNK' or (':?' in i[4]):
			#	#	acc+=1
			#	#	predicted.append(i[4])
			#	#	TN += 1	# unnkown
			#	else:
			#		FP += 1
			#		predicted.append(i[2] if tagprob[i[2]+'|'+prev] >tagprob[i[3]+'|'+prev] else i[3])				
			#else:
			if i[2]==i[3] and i[2]==i[4]:
				acc+=1
				predicted.append(i[4])
				TP += 1
				dict_actual[i[4]] += 1
				dict_predicted[i[4]] += 1
				dict_tp[i[4]] += 1
			elif wordprob[i[5]+'|'+i[2]] >wordprob[i[5]+'|'+i[3]]  and i[2]==i[4]:
				acc+=1
				predicted.append(i[4])
				TP += 1
				dict_tp[i[4]] += 1
				dict_actual[i[4]] += 1
				dict_predicted[i[4]] += 1
			elif wordprob[i[5]+'|'+i[3]] >wordprob[i[5]+'|'+i[2]]  and i[3]==i[4]:
				acc+=1
				predicted.append(i[4])
				TP += 1
				dict_tp[i[4]] += 1
				dict_actual[i[4]] += 1
				dict_predicted[i[4]] += 1
				#elif tagprob[i[3]+'|'+prev] >tagprob[i[2]+'|'+prev]  and i[3]==i[4]:
				#	acc+=1
				#	flag = 1
				#	predicted.append(i[4])
				#	TP += 1
			else:
				FP += 1
				dict_fp[i[2] if wordprob[i[5]+'|'+i[2]] >wordprob[i[5]+'|'+i[3]] else i[3]] += 1
				dict_fn[i[4]] += 1
				predicted.append(i[2] if wordprob[i[5]+'|'+i[2]] >wordprob[i[5]+'|'+i[3]] else i[3])
		#	prev = i[4]
			tot += 1
		#print dic1p
		#print dic2p[::-1]
		#if flag:
		#	print ' '.join([x.split('|')[0] for x in tokens])
		#	print dic1t
		#	print dic2t[::-1]
		#	print predicted
		#	print actual_tags
		#try:
		#	print "Accuracy = ",acc*1.0/tot,acc,tot
		#except:
		#	pass
		finacc += acc
		fintot += tot
		totsent += 1
		#if raw_input():
		#	continue
		y_true.extend(actual_tags)
		y_pred.extend(predicted)
	except:
		pass

print "\n\n\n\n\n\n"
print "Accuracy : ",accuracy_score(y_true, y_pred)
print "tp :",sum([i[0]==i[1] for i in zip(y_true,y_pred)])
print "Scores prec,rec,fm : ",precision_recall_fscore_support(y_true, y_pred, average='macro')
print "\n\n\n\n\n\n"
print set(y_true),set(y_pred)
def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1
    for i in range(len(y_hat)): 
        if y_hat[i]==1 and y_actual!=y_hat[i]:
           FP += 1
    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==0:
           TN += 1
    for i in range(len(y_hat)): 
        if y_hat[i]==0 and y_actual!=y_hat[i]:
           FN += 1
    return(TP, FP, TN, FN)
print "tp,fp,tn,fn",perf_measure(y_true,y_pred)
print "Final Accuracy = ",finacc*1.0/fintot
print "Total Senteces = ",totsent
print "Total Matched = ",finacc
print "Total Words = ",fintot
p = TP*1.0/(TP+FP)
r = TP*1.0/(TP+FN)
print "precision = ",TP*1.0/(TP+FP)
print "recall = ",TP*1.0/(TP+FN)
print "f measure = ",2*p*r/(p+r)
print "accuracy = ",TP*1.0/(TP+FP+FN)
print "TP,FP wagera ... :",TP,FP,TN,FN
precision = defaultdict(int)
recall = defaultdict(int)
fmeasure = defaultdict(int)
for i in dict_actual:
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
