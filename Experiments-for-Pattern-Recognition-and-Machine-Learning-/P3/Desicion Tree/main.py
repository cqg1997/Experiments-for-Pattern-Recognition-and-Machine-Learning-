import csv
import copy
import numpy as np

	
mistake_num = 0
all_num = 150
node_num = 0
	
class TreeNode:
	def __init__(self, entropy = -1, classtype = -1, attribute_var = -1, attribute_value = 0.0,  left_node = None, right_node = None):
		self.entropy = entropy
		self.classtype = classtype
		self.attribute_value = attribute_value
		self.attribute_var =  attribute_var
		self.left_node = left_node
		self.right_node = right_node
		
	def set_entropy(self, entro):
		self.entropy = entro
	
	def set_classtype(self, type):
		self.classtype = type
	
	def set_attribute_var(self, attribute_var):
		self.attribute_var = attribute_var
		
	def set_attribute_value(self, attribute_value):
		self.attribute_value = attribute_value
		
	def set_left_node(self, node):
		self.left_node = node
		
	def set_right_node(self, node):
		self.right_node = node
		

def read_data():
	dataset = []
	dictionary_class = []
	csvFile = open("Iris_Dataset.csv","r")
	csv_reader = csv.reader(csvFile)
	for line in csv_reader:
		sepal_length = float(line[0])
		sepal_width = float(line[1])
		petal_length = float(line[2])
		petal_width = float(line[3])
		name = (line[4])
		if name in dictionary_class:
			class_idx = dictionary_class.index(name)
		else:
			dictionary_class += [name]
			class_idx = dictionary_class.index(name)
		dataset += [[sepal_length, sepal_width, petal_length, petal_width, class_idx]]
	csvFile.close()
	return (dictionary_class,dataset)
def Entropy(dataset):
	num_list = [0,0,0]
	for case in dataset:
		num_list[case[4]] += 1
	entro = 0
	for num in num_list:
		if(num != 0):
			p = num / len(dataset)
			entro -= p * np.log2(p)
	main_class = num_list.index(max(num_list))
	return (entro, main_class)
	
def compute_IG(dataset, i, atr_value):
	dataset1 = []
	dataset2 = []
	for case in dataset:
		if(case[i] < atr_value):
			dataset1 += [case]
		else:
			dataset2 += [case]
	entro, main_class = Entropy(dataset)
	entro1, main_class = Entropy(dataset1)
	entro2, main_class = Entropy(dataset2)
	IG = entro - entro1* len(dataset1)/ len(dataset) - entro2 * len(dataset2)/ len(dataset)
	return IG
			
	
def find_best_atr_value(dataset, i):
	atr_value_list = [case[i] for case in dataset]
	atr_value_list.sort()
	max_IG = 0
	max_atr_value = 0.0
	for j in range(1, len(atr_value_list)):
		atr_value = (atr_value_list[j-1] + atr_value_list[j])/2
		IG = compute_IG(dataset, i, atr_value)
		if(IG > max_IG):
			max_IG = IG
			max_atr_value = atr_value
	return (IG, max_atr_value)
		
		
def find_best_atr(dataset, atr_set):
	max_IG = 0
	max_atr_var = -1
	max_atr_value = 0
	for i in range(len(atr_set)):
		if(atr_set[i]):
			IG, atr_value = find_best_atr_value(dataset, i)
			if(IG > max_IG):
				max_IG = IG
				max_atr_var = i
				max_atr_value = atr_value
	return (max_atr_var, max_atr_value)
	
def tree_gen(dataset, atr_set, dictionary_class, attribute_var_list,alpha):
	global mistake_num
	global node_num
	node = TreeNode()
	node_num +=1
	print()
	print("************************")
	print( "______new node_____")
	
	entro, main_class = Entropy(dataset)
	node.set_classtype(main_class)
	node.set_entropy(entro)
	print("entro: ",entro)
	print("main_class: ", dictionary_class[main_class])
	print("len: ",len(dataset))
	main_num = 0
	for case in dataset:
		if(case[4] == main_class):
			main_num += 1
	if(main_num/len(dataset) >= alpha):
		mistake_num += (len(dataset)-main_num)
		return node
	if (atr_set[0] == False and atr_set[1] == False and atr_set[2] == False and atr_set[3] == False):
		return node
	if(entro == 0):
		return node 
	new_atr_set = copy.deepcopy(atr_set)
	atr_var, atr_value = find_best_atr(dataset, atr_set)
	
	dataset1 = []
	dataset2 = []
	print(atr_var)
	for case in dataset:
		if(case[atr_var] < atr_value):
			dataset1 += [case]
		else:
			dataset2 += [case]
			
	if(len(dataset1) == 0 or len(dataset2) == 0):
		return node
	print("attribute_var: ", attribute_var_list[atr_var])	
	print("attribute_value: ", atr_value)	
	node.set_attribute_var(atr_var)
	node.set_attribute_value(atr_value)
	##new_atr_set[atr_var] = False     // when the attribute is discrete
	l_node = tree_gen(dataset1, new_atr_set, dictionary_class, attribute_var_list, alpha)
	r_node = tree_gen(dataset2, new_atr_set, dictionary_class, attribute_var_list, alpha)
	node.set_left_node(l_node)
	node.set_right_node(r_node)
	return node 
	
	
def main():
	global mistake_num,all_num
	dictionary_class, dataset = read_data()
	atr_set = [True,True,True,True]
	attribute_var_list = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width ']
	alpha = 0.92 
	root = tree_gen(dataset,atr_set, dictionary_class, attribute_var_list,alpha)
	accurcy = (all_num- mistake_num)/all_num
	print("***************\n")
	print("alpha: ",alpha)
	print("accurcy: ",accurcy)
	print("node number: ",node_num)
	
	return

main()