# this program deletes all the consonents in a word, and stores the 
# deleted consonent word along with tag probabilities ina new file , "suffix_prob.txt"

import codecs
from collections import defaultdict

# list of vowels
from unicode_hindi import vowels


# train file
trainfile = codecs.open("data/train.txt",mode='r',encoding='utf-8')
rootfile = codecs.open("data/roofile.txt",mode='w',encoding='utf-8')
dic = {}
for sentence in trainfile:
	tokens = sentence.split()
	for token in tokens:
		word = token.split('|')[0]
		root = token.split('|')[1].split('.')[0]
		tag = token.split('|')[2].split('.')[0]
		newword = ''
		for letter in word:
			if letter not in vowels:
				newword += '*'
			else:
				newword += letter
		newroot = ''
		for letter in root:
			if letter not in vowels:
				newroot += '*'
			else:
				newroot += letter
		dic[newword] = newroot		
		
print "Dict Length = ",len(dic) 
for i in dic:
	rootfile.write(i+'\t'+dic[i]+'\n')
rootfile.close()
trainfile.close()
