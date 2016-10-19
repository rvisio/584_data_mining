from itertools import izip

def pairwise(iterable):
	a = iter(iterable)
	return izip(a,a)

#iris = datasets.load_iris()

#X = iris.data[:,:4]


#print X
'''
labels = {}
index = 0
with open('../data/features.label') as label_file:
	for line in label_file:
		index += 1
		labels[str(index)] = line.split()[0]
label_file.close()
'''
'''
matrix = []
with open('../data/input.mat') as input_file:
	for line in input_file:
		line = line.split()
		print len(line)
		temporaryList = []
		for x,y in pairwise(line):
			print 'The word ' , str(labels[x]) , ' appeared ' , y , ' times'
'''
label_list = []
with open('../data/features.label') as label_file:
	for line in label_file:
		label_list.append(line)
input_list = []
with open('../data/input.mat') as input_file:
	for line in input_file:
		input_list.append(line)

matrix = []
label_len = len(label_list)
for current_label in label_list:
	print current_label
	tempRecord = []
	tempRecord.append(current_label)
	for record in input_list:
		print record
		record = record.split()
		for x,y in pairwise(record):
			x = int(x)
			for current_index in range(label_len):
				if x == current_index:
					tempRecord.append(y)
				else:
					tempRecord.append(0)
		matrix.append(tempRecord)

for mat in matrix:
	print mat
'''
matrix = []
with open('../data/features.label') as label_file:
	with open('../data/input.mat') as input_file:
		for label_line in label_file:
			print label_line
			tempRecord = []
			label_line = label_line.strip()
			tempRecord.append(str(label_line))
			for input_line in input_file:
				input_line = input_line.split()

				for x,y in pairwise(input_line):
					#print x,y
					#print type(x)

					for current_index in range(index):
						#print 'current_index is ' , str(current_index)
						#print x
						if x == str(current_index):
							tempRecord.append(y)
					#		print 'x matches the current index'
					#		print x, current_index
						else:
							tempRecord.append(0)
					#print x,y

			matrix.append(tempRecord)

for mat in matrix:
	print mat
	'''
