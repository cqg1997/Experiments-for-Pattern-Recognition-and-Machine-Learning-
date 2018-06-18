import csv
import copy
import numpy as np
import random

def gen_set():
	csv_File0 = open("dataset/origin.csv","r")
	csv_File1 = open("dataset/train.csv","w",newline = '')
	csv_File2 = open("dataset/test.csv","w",newline = '')
	origin = csv.reader(csv_File0)
	train = csv.writer(csv_File1)
	test = csv.writer(csv_File2)
	for line in origin:
		rand = random.uniform(0,1)
		if(rand <= 0.2):
			test.writerow([((int(line[i])-1)/9) for i in range(1,10)]+[(int(line[10])-2)/2])
		else:
			train.writerow([((int(line[i])-1)/9) for i in range(1,10)]+[(int(line[10])-2)/2])
	return
	
gen_set()
	
	