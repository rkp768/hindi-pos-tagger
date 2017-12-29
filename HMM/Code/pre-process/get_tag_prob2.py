from __future__ import division
# this program calculates the tag probabilities
# and stores in a file "tag_prob.txt"

import codecs
from collections import defaultdict

# trainfile
trainfile = codecs.open('data/new_train.txt',mode='r',encoding='utf-8')

# count of tag sequences
cnt = defaultdict(lambda : 1)
# prob of tag sequence
prob = {}
# total sequences
tot1,tot2 = 0,0
ttootoot = 0
for sentence in trainfile.readlines():
	if sentence!='\n' and ('SYM' not in ' '.join(sentence.split()[:-1])):
		tags = ['$']
		for token in sentence.split():
			tags.append(token.split('|')[2].split('.')[0])
			ttootoot += 1
		cnt[tags[0]+'|'+tags[1]] += 1
		tot1 += 1
		for t in range(len(tags[:-2])):
			cnt[tags[t]+'|'+tags[t+1]+'|'+tags[t+2]] += 1
			tot2 += 1
for i in cnt:
	if i.count('|')==1:
		prob[i] = cnt[i]/tot1
	else:
		prob[i] = cnt[i]/tot2
print ttootoot
probfile = codecs.open('data/tag_prob2.txt',mode='w',encoding='utf-8')
for i in prob:
	probfile.write(i+'\t'+str(prob[i])+'\n')
trainfile.close()
probfile.close()
