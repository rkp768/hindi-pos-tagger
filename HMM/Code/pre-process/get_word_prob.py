# this program calculates word probabilities and stores them 
# in "word_prob.txt"

import codecs
from collections import defaultdict
from unicode_hindi import vowels


# training file
trainfile = codecs.open('data/new_train.txt',mode='r',encoding='utf-8')
# count
count = defaultdict(lambda :1)
# prob
prob = {}
# total
total = 0 
sent = 0
for sentence in trainfile.readlines():
	tokens = sentence.split()
	if len(tokens) >5:
		sent += 1
		for token in tokens:
			word = token.split('|')[0].split('.')[0]
			tag = token.split('|')[2].split('.')[0].strip(':?')
			count[(word+'|'+tag)] += 1
			total += 1
for term in count:
	prob[term] = (1.0*count[term])/total

print "Max prob = ",max(prob.values())
print "Min prob = ",min(prob.values())
print "total words = ",total
print "total sentences = ",sent
# prob file
probfile = codecs.open('data/word_prob.txt', mode='w', encoding = 'utf-8')
for term in prob:
	probfile.write(term+'\t'+str(prob[term])+'\n')

trainfile.close()
probfile.close()
