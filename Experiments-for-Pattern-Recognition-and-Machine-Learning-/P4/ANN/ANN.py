import numpy as np
import math
import random
import copy
import csv
import sys

def sigmoid(o,theta):
	return (1.0/(1.0+math.exp(theta-o)))## exp(-z)  z = o - theta
	

class MODEL:
	def __init__(self, input_layer, hidden_layers, output_layer):
		self.input_layer = input_layer
		self.output_layer = output_layer
		self.hidden_layers = copy.deepcopy(hidden_layers)
		self.hidden_depth = len(hidden_layers)
		if(len(hidden_layers)<1):
			print ("this model need more layers(>=3)")
			return
		if(input_layer<=0):
			print ("Invalid dimension of input")
			return
		if(output_layer<=0):
			print ("Invalid dimension of output")
			return
		self.input = np.mat([0 for i in range(input_layer)])
		self.output = [np.mat([0 for i in range(output_layer)]), np.mat([0 for i in range(output_layer)]),np.mat([random.uniform(0,2) for i in range(output_layer)])]
		self.real_output = np.mat([0 for i in range(output_layer)])
		self.hidden = []
		self.g = np.mat([0.0 for i in range(output_layer)])
		self.e = []
		for num in hidden_layers:
			if(num<=0):
				print ("Invalid dimension of someone hidden layer")
				return
			else:
				self.hidden.append([np.mat([0 for i in range(num)]),np.mat([0 for i in range(num)]),np.mat([random.uniform(0,100) for i in range(num)])])
				self.e.append(np.mat([0.0 for i in range(num)]))
		
		##generate all weight np.matrixs(T) 
		self.weight = []
		self.weight.append(np.mat([[random.uniform(0,0.25) for i in range(hidden_layers[0])] for i in range(input_layer)]))
		for i in range(1,len(hidden_layers)):
			self.weight.append(np.mat([[random.uniform(0,0.25) for j in range(hidden_layers[i])] for j in range(hidden_layers[i-1])]))
		self.weight.append(np.mat([[random.uniform(0,0.25) for i in range(output_layer)] for i in range(hidden_layers[-1])]))
		return
	
	def forecast(self,input):
		self.hidden[0][0] = np.mat(input) * self.weight[0]
		self.hidden[0][1] = np.mat([sigmoid(self.hidden[0][0][0,i], self.hidden[0][2][0,i]) for i in range(self.hidden_layers[0])])
		for i in range(1,self.hidden_depth):
			self.hidden[i][0] = self.hidden[i-1][1] * self.weight[i]
			self.hidden[i][1] = np.mat([sigmoid(self.hidden[i][0][0,j], self.hidden[i][2][0,j]) for j in range(self.hidden_layers[i])])
		self.output[0] = self.hidden[self.hidden_depth-1][1] * self.weight[self.hidden_depth]
		self.output[1] = np.mat([sigmoid(self.output[0][0,i], self.output[2][0,i]) for i in range(self.output_layer)])
		return self.output[1]
	
	def bp(self, input, output, learn_rate):
		self.input = np.mat(input)
		self.real_output = np.mat(output)
		self.forecast(input)
		for i in range(self.output_layer):
			self.g[0,i] = self.output[1][0,i]*(1- self.output[1][0,i])*(self.real_output[0,i]- self.output[1][0,i])
			
		for i in range(self.hidden_depth)[::-1]:
			if(i == self.hidden_depth-1):
				for j in range(self.hidden_layers[i]):
					self.e[i][0,j] = self.hidden[i][1][0,j] * (1 - self.hidden[i][1][0,j]) * (self.weight[i+1][j] * self.g.T)
			else:
				for j in range(self.hidden_layers[i]):
					self.e[i][0,j] = self.hidden[i][1][0,j] * (1 - self.hidden[i][1][0,j]) * (self.weight[i+1][j] * self.e[i+1].T)
		
		##+++++++++++ fresh the weight np.matrixs ++++++++++####
		delta_weight = learn_rate* self.hidden[self.hidden_depth-1][1].T * self.g
		self.weight[self.hidden_depth] += delta_weight
		for i in range(self.hidden_depth-1)[::-1]:
			delta_weight =  learn_rate * self.hidden[i][1].T * self.e[i+1]
			self.weight[i+1] += delta_weight
		delta_weight = learn_rate * self.input.T * self.e[0]
		self.weight[0] += delta_weight
		
		##++++++++++ fresh the Thresholds ++++++++++#####
		delta_shold = learn_rate* self.g
		self.output[2] -=  delta_shold
		for i in range(self.hidden_depth)[::-1]:
			delta_shold =  learn_rate * self.e[i]
			self.hidden[i][2] -= delta_shold
			
		return
		
def read_set():
	train = []
	test= []
	csv_File1 = open("dataset/train.csv","r")
	csv_File2 = open("dataset/test.csv","r")
	train_reader = csv.reader(csv_File1)
	test_reader = csv.reader(csv_File2)
	for line in train_reader:
		train += [[float(line[i]) for i in range(10)]]
	for line in test_reader:
		test += [[float(line[i]) for i in range(10)]]
	return (train,test)

def train(train_set,model,learn_rate):
	for case in train_set:
		input = case[0:9]
		output = case[9:]
		model.bp(input,output,learn_rate)
	return

def test_E(test_set,model):
	E = 0.0
	for case in test_set:
		input = case[0:9]
		output = model.forecast(input)
		E += (output[0,0]-case[9]) * (output[0,0]-case[9])
	return E
	
def test(test_set,model):
	csv_File = open("result/result.csv","w",newline = '')
	result = csv.writer(csv_File)
	for case in test_set:
		input = case[0:9]
		output = model.forecast(input)
		result.writerow(case + output.tolist()[0])
	return

def main():
	train_set,test_set = read_set()
	model = MODEL(9,[1024],1)
	if (len(sys.argv) == 1):    
		learn_rate = 0.2           ## default learn rate 0.2
	else:	
		learn_rate = float(sys.argv[1])
	for i in range(200):
		print("Eqho: ", i)
		train(train_set,model,learn_rate)
		print("Error of test dataset: ",test_E(test_set,model))
		print("Eqho: ", i, "  Done")
	test(test_set,model)
	return 

main()
	
				
				
	