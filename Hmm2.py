# main hmm code
import codecs
from collections import defaultdict
from unicode_hindi import vowels,digits
# testfile
testfile = codecs.open('test.txt',mode='r',encoding='utf-8')

# all tags
alltags = []
trainfile = codecs.open('train.txt',mode='r',encoding='utf-8')
for sentence in trainfile.readlines():
	tokens = sentence.split()
	for token in tokens:
		alltags.append(token.split('|')[2].split('.')[0])
alltags = list(set(alltags))

# word prob file 
wordprobfile = codecs.open('word_prob.txt',mode='r',encoding='utf-8')
wordprob = {}
for term in wordprobfile.readlines():
	wordprob[term.split('\t')[0]] = float(term.split('\t')[1])
tagprobfile = codecs.open('tag_prob2.txt',mode='r',encoding='utf-8')
tagprob = {}
for term in tagprobfile.readlines():
	tagprob[term.split('\t')[0]] = float(term.split('\t')[1])
fintot = 0
finmat = 0
asssssss= 0
aWEEEEEEEEEEE = 0
for sentence in testfile.readlines():	
	if sentence!='\n' and ('SYM' not in ' '.join(sentence.split()[:-1])):
		asssssss += 1
		tot = 0
		acc = 0
		indx = 0 
		prev = '$'
		for token in sentence.split():
			aWEEEEEEEEEEE += 1
			word = token.split('|')[0]
			actual_tag = token.split('|')[2].split('.')[0]
			ans = -1*float('inf')
			for digit in digits:
				if digit in word:
					predicted_tag = u'QC'
					prev = u'QC'
			else:
				word = token.split('|')[0].strip('(').strip(')').strip('\'').strip('\"').strip('-').strip('[').strip(']').strip(':').strip(';').strip(',').strip('?').strip('-').strip('!').strip('@').strip('#').strip('&').strip('_').strip('=')
				for tag in alltags:
					if indx == 0:
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
							prevprev = prev	
							prev = predicted_tag
					else:
						try:
							tp = tagprob[tag+'|'+prev+'|'+prevprev]
						except:
							tp = 1e-8
						try:
							wp = wordprob[word+'|'+tag]
						except:
							wp = 1e-8
						if tp*wp>ans:
							ans = tp*wp
							predicted_tag = tag
				prevprev = prev
				prev = predicted_tag			
			indx += 1	
		if actual_tag == predicted_tag or actual_tag=='UNK' or actual_tag.strip(':?') == predicted_tag.strip(':?'):
			acc+=1
		tot +=1	
		if tot:
			print "Accuracy = ",acc*100.0/tot,"\tTotal = ",tot,"\tMatched = ",acc
			fintot += tot
			finmat += acc
print "Final Accuracy = ",(finmat*100.0)/fintot
print asssssss,aWEEEEEEEEEEE
tagprobfile.close()
wordprobfile.close()
trainfile.close()
testfile.close()
