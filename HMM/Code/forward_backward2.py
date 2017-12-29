import codecs
from collections import defaultdict
from unicode_hindi import vowels,digits
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
for sentence in testfile.readlines():
	# for forward	
	prev = '$'
	tokens = sentence.split()
	dic1p = []
	dic1t = []
	actual_tags = []
	for token in tokens:
		word = token.split('|')[0]
		actual_tags.append(token.split('|')[2].split('.')[0].strip(':?'))
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
	# choose from forward/backwrd
	try:
		ct = '$'
		dic1t = dict1t	# forwrd tags
		dic2t = dic2t[::-1]	# backward tags
		pro1 = 1
		for i in dic1t:
			pro1 *= tagprob[i+'|'+ct]
			ct = i
		ct = '$'		
		pro2 = 1
		for i in dic2t:
			pro2 *= tagprob[i+'|'+ct]
			ct = i
		tot = 0		
		if pro1 > pro2:
			acc = 0
			for j in zip(dic1t,actual_tags):
				if j[0]==j[1]:
					acc += 1
		else:
			acc = 0
			for j in zip(dic2t,actual_tags):
				if j[0]==j[1]:
					acc += 1
		finacc += acc
		fintot += tot
		print "Total Matched = ",acc,"\tTotal Words = ",tot
	except:
		pass
print "Final Accuracy = ",finacc*1.0/fintot
print "Total Senteces = ",totsent
p = TP*1.0/(TP+FP)
r = TP*1.0/(TP+FN)
print "precision = ",TP*1.0/(TP+FP)
print "recall = ",TP*1.0/(TP+FN)
print "f measure = ",2*p*r/(p+r)
print "accuracy = ",TP*1.0/(TP+FP+FN)
