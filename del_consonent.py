# this program deletes all the consonents in a word, and stores the 
# deleted consonent word along with tag probabilities ina new file , "suffix_prob.txt"

import codecs
from collections import defaultdict

# list of vowels
from unicode_hindi import vowels

# tag count dictionary
count = defaultdict(lambda : 1)
# tag prob dictionary
prob = {}
# total words
tot = 0

# all possible
all_possible_word = defaultdict(lambda : [])
all_possible_suff = defaultdict(lambda : [])


# train file
trainfile = codecs.open("train.txt",mode='r',encoding='utf-8')
for sentence in trainfile:
	tokens = sentence.split()
	for token in tokens:
		word = token.split('|')[0]
		tag = token.split('|')[2].split('.')[0]
		all_possible_word[word].append(tag)	# all possible tag for a suffix
		newword = ''
		for letter in word:
			if letter not in vowels:
				newword += '*'
			else:
				newword += letter
		count[(newword+'|'+tag)] += 1
		all_possible_suff[newword].append(tag)
		tot +=1
print "Total Words = ",tot
print "Dict Length = ",len(count) 

for term in count:
	prob[term] = count[term]/(tot*1.0)


# highest probability
print "highest = ",max(prob.values())
# lowest probability
print "lowest = ",min(prob.values())
probfile = codecs.open('suffix_prob.txt',mode='w',encoding='utf-8')
for term in prob:
	probfile.write(term+'\t'+str(prob[term])+'\n')

# all possible file
allfileword = codecs.open('all_possible_word.txt',mode='w',encoding='utf-8')
for term in all_possible_word:
	allfileword.write(term+'\t'+'.'.join(list(set(all_possible_word[term])))+'\n')
allfilesuff = codecs.open('all_possible_suff.txt',mode='w',encoding='utf-8')
for term in all_possible_suff:
	allfilesuff.write(term+'\t'+'.'.join(list(set(all_possible_suff[term])))+'\n')

trainfile.close()
probfile.close()
allfileword.close()
allfilesuff.close()	
