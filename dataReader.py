import random
data = []
test = {'x':[], 'y':[]}
index = 0

dimension = 10;
category = 5;

def read(filename):
	f = open(filename, 'r')
	vectors = []
	global data
	for line in f:
		numbers = []
		for number in line.split(' '):
			numbers.append(float(number))
		vectors.append(numbers)
	for vec in vectors:
		if (random.randint(0, 100) < 10):
			test['x'].append(vec[0:dimension])
			test['y'].append(vec[dimension:dimension + category])
		else:
			data.append({'x':vec[0:dimension], 'y': vec[dimension:dimension + category]})


def next_batch(batchSize):
	counter = batchSize
	x = []
	y = []
	global index
	global data
	while (counter > 0):
		x.append(data[index]['x'])
		y.append(data[index]['y'])
		index = (index + 1) % len(data);
		counter -= 1
	return x, y 