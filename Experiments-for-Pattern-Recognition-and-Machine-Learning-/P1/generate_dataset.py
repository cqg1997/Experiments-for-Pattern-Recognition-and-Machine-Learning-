import numpy as np
import random
import csv

def dataset():
	list = []
	for i in range(-100,100):
		rand = random.uniform(-10,10)
		x = i + random.uniform(-1,1)
		y = random.uniform(-30,30)
		z = 5/4 - 1/2 * x - 3/4 * y + rand
		if (rand == 0):
			continue
		if(rand > 0):
			list += [[x,y,z,1]]
			continue
		else:
			list += [[x,y,z,-1]]
	out = open("dataset2.csv",'w',newline = '')
	csv_writer = csv.writer(out)
	csv_writer.writerows(list)
			
	return list


