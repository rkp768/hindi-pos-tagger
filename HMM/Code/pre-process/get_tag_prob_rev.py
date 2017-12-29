# this program calculates the tag probabilities
# and stores in a file "tag_prob.txt"

import codecs
from collections import defaultdict

# trainfile
trainfile = codecs.open('data/new_train.txt',mode='r',encoding='utf-8')

# count of tag sequences
count = defaultdict(lambda : 1)
# prob of tag sequence
prob = {}
# total sequences
tot = 0
cnttt = 0
kan = 0
for sentence in trainfile.readlines():
	if len(sentence)>5:
		cnttt += 1
		tags = []
		tokens = sentence.split()[::-1]
		for token in tokens:
			tags.append(token.split('|')[2].split('.')[0].strip(':?'))
			tot += 1
		count[(tags[0]+'|'+'$')] += 1	
		for i in range(1,len(tags)):
			count[(tags[i]+'|'+tags[i-1])] += 1
		kan += 1
for term in count:
	prob[term] = count[term]/(tot*1.0)

print ""
print "Max Prob = ",max(prob.values())
print "Min Prob = ",min(prob.values())
probfile = codecs.open('data/tag_prob_rev.txt',mode='w',encoding='utf-8')
for term in prob:
	probfile.write(term+'\t'+str(prob[term])+'\n')
print kan
trainfile.close()
probfile.close()
