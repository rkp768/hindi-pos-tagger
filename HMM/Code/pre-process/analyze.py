import codecs

f = codecs.open("data/train.txt",mode="r",encoding="utf-8")
f2 = codecs.open("data/new_train.txt",mode="w",encoding="utf-8")
cnt = 0
red = 0
for i in f.readlines():
	cnt += 1
	if ('|UNK' in i) or ('B-NP' in i) or ('I-NP' in i) or ('|O' in i):
		red += 1
	else:
		f2.write(i)
print red
print cnt
print cnt-red

f.close()
f2.close()

f = codecs.open("data/test.txt",mode="r",encoding="utf-8")
f2 = codecs.open("data/new_test.txt",mode="w",encoding="utf-8")
cnt = 0
red = 0
for i in f.readlines():
	cnt += 1
	if ('|UNK' in i) or ('B-NP' in i) or ('I-NP' in i) or ('|O' in i):
		red += 1
	else:
		f2.write(i)

print red
print cnt
print cnt-red

f.close()
f2.close()
