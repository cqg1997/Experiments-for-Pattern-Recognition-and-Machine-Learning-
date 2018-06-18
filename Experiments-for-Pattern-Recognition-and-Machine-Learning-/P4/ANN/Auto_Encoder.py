import numpy as np
import math
import random
import copy
import csv
import sys

def sigmoid(o,theta):
	return (1.0/(1.0+math.exp(theta-o)))## exp(-z)  z = o - theta

def align_int(x):
	return int(x+0.5)
	

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
		self.output = [np.mat([0 for i in range(output_layer)]), np.mat([0 for i in range(output_layer)]),np.mat([random.uniform(0,hidden_layers[0]/10) for i in range(output_layer)])]
		self.real_output = np.mat([0 for i in range(output_layer)])
		self.hidden = []
		self.g = np.mat([0.0 for i in range(output_layer)])
		self.e = []
		for num in hidden_layers:
			if(num<=0):
				print ("Invalid dimension of someone hidden layer")
				return
			else:
				self.hidden.append([np.mat([0 for i in range(num)]),np.mat([0 for i in range(num)]),np.mat([random.uniform(0,2) for i in range(num)])])
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
	dataset= []
	csv_File = open("dataset/encoder.csv","r")
	dataset_reader = csv.reader(csv_File)
	for line in dataset_reader:
		dataset += [[int(line[i])/10 for i in range(5)]]
	return dataset

def train(train_set,model,learn_rate):
	for case in train_set:
		model.bp(case,case,learn_rate)
	return

def test_E(test_set,model):
	E = 0.0
	for case in test_set:
		output = model.forecast(case)
		for i in range(5):
			E += (align_int(output[0,i]*10)- int(case[i]*10))* (align_int(output[0,i]*10)- int(case[i]*10))
	return E
	
def test(test_set,model,node):
	csv_File = open("result/result_encoder_"+str(node)+".csv","w",newline = '')
	result = csv.writer(csv_File)
	num = 0
	right_num = 0
	for case in test_set:
		output = model.forecast(case)
		output = output.tolist()[0]
		if_true= True
		for i in range(5):
			case[i] = int(case[i]*10)
			output[i] = align_int(output[i]*10)
			if(case[i]!= output[i]):
				if_true = False
		num += 1
		if(if_true):
			right_num += 1
		result.writerow([(case)] + [(output)])
	return (right_num/num)

def main():
	if (len(sys.argv) < 2):    
		learn_rate = 0.2           ## default learn rate 0.2
	else:	
		learn_rate = float(sys.argv[1])
		
	dataset = read_set()
	model1 = MODEL(5,[20],5)
	model2 = MODEL(5,[50],5)
	model3 = MODEL(5,[100],5)
	
	i = 0
	current_E = 999999.0
	pre_E = current_E +1
	while(current_E< pre_E):
		i += 1
		pre_E = current_E
		train(dataset,model1,learn_rate)
		current_E = test_E(dataset,model1)
	accuracy = test(dataset,model1,20)
	print ("\n\n")
	print ("************ hidden layer nodes : 20")
	print("number of iterations: ",i)
	print ("accuracy",accuracy)
	print ("E: ", current_E)
	print("***************************\n")
	
	i = 0
	current_E = 999999999.0
	pre_E = current_E +1
	while(i<3):
		i += 1
		pre_E = current_E
		train(dataset,model2,learn_rate)
		current_E = test_E(dataset,model2)
	accuracy = test(dataset,model2,50)
	print ("************ hidden layer nodes : 50")
	print("number of iterations: ",i)
	print ("accuracy",accuracy)
	print ("E: ", current_E)
	print("***************************\n")
	
	i = 0
	current_E = 999999999.0
	pre_E = current_E +1
	while(i<1):
		i += 1
		pre_E = current_E
		train(dataset,model3,learn_rate)
		current_E = test_E(dataset,model3)
	accuracy = test(dataset,model3,100)
	print ("************ hidden layer nodes : 100")
	print("number of iterations: ",i)
	print ("accuracy",accuracy)
	print ("E: ", current_E)
	print("***************************\n")
	return 

main()
	
				
				
	