from numpy import *
import operator
import pickle
from PIL import Image
import os

def createDataSet():
	group = array([1.0,1.1],[1.0,1.0],[0,0.1])
	labels = ['A','A','B','B']
	return group,labels

def classify_origin(inX,DataSet,labels,k):
	datasize = DataSet.shape[0]
	diffMat = tile(inX,(datasize,1))-DataSet
	sqdiffMat = diffMat**2
	sqdistance = sqdiffMat.sum(axis = 1)
	distance = sqdistance ** 0.5
	print distance
	sorteddistance = distance.argsort()
	#print sorteddistance
	classCount = {}
	for i in range(k):
		currentlabel =  labels[list(sorteddistance).index(i)]
		classCount[currentlabel] = classCount.get(currentlabel,0) + 1
	sortedclasscount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse = True)
	return sortedclasscount[0][0]

def autoNorm(DataSet):
	minVals = DataSet.min(0)
	maxVals = DataSet.max(0)
	rangelength = maxVals - minVals
	norm =  zeros(shape(DataSet))
	if len(DataSet.shape) == 1:
		minMat = tile(minVals,DataSet.shape[0])
		rangelengthMat = tile(rangelength,DataSet.shape[0])
	else:
		x,y = DataSet.shape[0],DataSet.shape[1]
		minMat = tile(minVals,(x,y))
		rangelengthMat = tile(rangelength,(x,y))
	norm = DataSet - minMat
	norm = norm/rangelengthMat
	return norm , rangelength , minVals

def unflat(data,x):
	if len(data) % x <> 0:
		print "Error,not completely divided"
	else:
		y = len(data)/x
		new = zeros((y,x))
		for i in range(y):
			new[i,:] = data[i*32:(i+1)*x]
		return new

def saveData(data,filename):
	f = open(filename,'wb')
	pickle.dump(data,f)
	f.close()

def loadTrainingData(path):
	# The naming method is "{num}_{count of num}.png"
	filenames = [i for i in os.listdir(path) if i.split('.')[-1] == 'png']
	print filenames
	filecount = len(filenames)
	labels = []
	dataset = zeros((filecount,1024))
	for i in range(filecount):
		labels.append(filenames[i].split('.')[0].split('_')[0])
		im = Image.open(path+'/'+filenames[i]).convert('L')
		proc, ranges, minval = autoNorm(array(im).flatten())
		dataset[i] = proc
	print dataset
	return dataset, labels

def loadTestingData(path):
	filenames = [i for i in os.listdir(path) if i.split('.')[-1] == 'png']
	print filenames
	filecount = len(filenames)
	expected = []
	dataset = zeros((filecount,1024))
	for i in range(filecount):
		expected.append(filenames[i].split('.')[0].split('_')[0])
		im = Image.open(path+'/'+filenames[i]).convert('L')
		proc, ranges, minval = autoNorm(array(im).flatten())
		dataset[i] = proc
	return dataset, filecount,expected

def classify():
	"""if not os.path.lexists('TrainingData/TrainedData'):
		dataset, labels = loadTrainingData('TrainingData')
		f = open('TrainingData/TrainedData','wb')
		pickle.dump((dataset,labels),f)
		f.close()
	else:
		(dataset,labels) = pickle.load(open('TrainingData/TrainedData','rb'))"""
	dataset, labels = loadTrainingData('TrainingData')
	test, testcount, expected = loadTestingData('TestingData')
	for i in range(testcount):
		result = classify_origin(test[i], dataset, labels, 3)
		print "result is ",result," correct result is ", expected[i]
	print "Done"

