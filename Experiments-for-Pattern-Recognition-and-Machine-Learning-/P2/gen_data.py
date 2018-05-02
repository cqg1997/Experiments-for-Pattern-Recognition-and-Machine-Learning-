import random
import csv

def gen_data():
	csv_File = open("test.csv","w",newline = '')
	writer = csv.writer(csv_File)
	for i in range (0,6):
		x = random.uniform(0,20)
		y = random.uniform(0,20)
		writer.writerow((x,y,1))
	for i in range (0,8):
		x = random.uniform(0,-20)
		y = random.uniform(0,20)
		writer.writerow((x,y,2))
	for i in range (0,12):
		x = random.uniform(0,-20)
		y = random.uniform(0,-20)
		writer.writerow((x,y,3))
	for i in range (0,14):
		x = random.uniform(0,20)
		y = random.uniform(0,-20)
		writer.writerow((x,y,4))
	return
		
gen_data()