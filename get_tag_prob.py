# this program calculates the tag probabilities
# and stores in a file "tag_prob.txt"

import codecs
from collections import defaultdict

# trainfile
trainfile = codecs.open('new_train.txt',mode='r',encoding='utf-8')

# count of tag sequences
count = defaultdict(lambda : 1)
# prob of tag sequence
prob = {}
# total sequences
tot = 0
cnttt = 0
shit = defaultdict(list)
for sentence in trainfile.readlines():
	if len(sentence)>5:
		cnttt += 1
		tags = []
		for token in sentence.split():
			tags.append(token.split('|')[2].split('.')[0].strip(':?'))
			shit[token.split('|')[2].split('.')[0].strip(':?')].append(token.split('|')[0].split('.')[0])
			tot += 1
		count[(tags[0]+'|'+'$')] += 1	
		for i in range(1,len(tags)):
			count[(tags[i]+'|'+tags[i-1])] += 1
for term in count:
	prob[term] = count[term]/(tot*1.0)

print ""
print "Max Prob = ",max(prob.values())
print "Min Prob = ",min(prob.values())
print "Total Senteces = ",cnttt
print "Total Words = ",tot

probfile = codecs.open('tag_prob.txt',mode='w',encoding='utf-8')
for term in prob:
	probfile.write(term+'\t'+str(prob[term])+'\n')

trainfile.close()
probfile.close()
