import numpy as np
import generate_dataset as gendata
import csv

def data_process():
	data = []
	csvFile = open("dataset2.csv","r")
	csv_reader = csv.reader(csvFile)
	for line in csv_reader:
		x = float(line[0])
		y = float(line[1])
		z = float(line[2])
		t = int(line[3])
		data += [[x*t, y*t, z*t, t]]
	csvFile.close()
	return data

def model_init(dimension):
	vector = []
	for i in range(0,dimension):
		vector += [i*i*5]
	print (vector)
	return vector

	
def model(rate,data):
	csvFile = open((str(rate)+".csv"),"w", newline = '')
	csv_writer = csv.writer(csvFile)
	[w1,w2,w3,w4] = model_init(4)
	iteration = 0
	flag = True
	while(flag):
		iteration += 1
		wrong_num = 0
		flag = False
		for [x,y,z,t] in data:
			if ((x*w1+y*w2+z*w3+t*w4)<= 0):
				flag = True
				wrong_num += 1;
				w1 += x * rate
				w2 += y * rate
				w3 += z * rate
				w4 += t * rate
		if(iteration%2000 == 0):
			csv_writer.writerow((iteration,wrong_num))
			##print(wrong_num)
	csv_writer.writerow((iteration,wrong_num))
	print(iteration)
	return (rate, -w1/w4*5,-w2/w4*5,-w3/w4*5,-5,iteration)
				
				
	

def main():
	min = 1
	max = 1.5
	csvFile = open("iteration","w", newline = '')
	csv_writer = csv.writer(csvFile)
	data = data_process()
	line = model(0.01,data)
	min = line[5]
	max = line[5]
	csv_writer.writerow(line)
	line = model(0.1,data)
	csv_writer.writerow(line)
	line = model(0.2,data)
	csv_writer.writerow(line)
	line = model(0.3,data)
	csv_writer.writerow(line)
	line = model(0.4,data)
	csv_writer.writerow(line)
	line = model(0.5,data)
	csv_writer.writerow(line)
	line = model(0.6,data)
	csv_writer.writerow(line)
	line = model(0.7,data)
	csv_writer.writerow(line)
	line = model(0.8,data)
	csv_writer.writerow(line)
	line = model(0.9,data)
	csv_writer.writerow(line)
	line = model(0.99,data) 
	csv_writer.writerow(line)
	return
	
main()