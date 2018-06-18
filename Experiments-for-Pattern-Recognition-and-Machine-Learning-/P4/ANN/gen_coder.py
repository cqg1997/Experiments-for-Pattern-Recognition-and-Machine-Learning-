import csv
import copy
import numpy as np
import random

def gen_coder():
	csv_File = open("dataset/encoder.csv","w",newline = '')
	dataset = csv.writer(csv_File)
	for i in range(100):
		line = []
		for j in range(5):
			line += [random.randint(0,10)]
		dataset.writerow(line)
	return
	
gen_coder()
	
	