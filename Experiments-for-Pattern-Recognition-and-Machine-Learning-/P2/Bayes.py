import csv
import math

def data_process():
	csv_File = open("dataset.csv","r")
	reader = csv.reader(csv_File)
	freq = [0,0,0,0,0]
	data = [[],[],[],[],[]]
	for line in reader:
		x = float(line[0])
		y = float(line[1])
		z = int(line[2])
		freq[z] += 1
		data[z] += [(x,y)]
	print (freq)
	return (freq[1:5],data[1:5])
def Guass(u,delta,delta2,x):
	PI = 3.1415926
	r = math.exp(-(x-u)*(x-u)/2/delta2)/delta/math.sqrt(2*PI)
	return r
def post_prob(x,y,w,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion):
	sum = 0
	for i in range(0,4):
		sum += proportion[i]*Guass(avg_x[i],delta_x[i],delta2_x[i],x)*Guass(avg_y[i],delta_y[i],delta2_y[i],y)
	r = proportion[w]*Guass(avg_x[w],delta_x[w],delta2_x[w],x)*Guass(avg_y[w],delta_y[w],delta2_y[w],y)/sum
	return r
	
def compute():
	freq,data = data_process()
	avg_x = []
	avg_y = []
	delta_x = []
	delta_y = []
	delta2_x = []
	delta2_y = []
	i = 0
	for cla in data:
		sum_x = 0
		sum_y = 0
		for (x,y) in cla:
			sum_x += x
			sum_y += y
		avg_x += [sum_x/freq[i]]
		avg_y += [sum_y/freq[i]]
		i += 1
	i = 0
	for cla in data:
		sum_x = 0
		sum_y = 0
		for (x,y) in cla:
			sum_x += (x-avg_x[i])*(x-avg_x[i])
			sum_y += (y-avg_y[i])*(y-avg_y[i])
		delta2_x += [sum_x/freq[i]]
		delta2_y += [sum_y/freq[i]]
		delta_x += [math.sqrt(sum_x/freq[i])]
		delta_y += [math.sqrt(sum_y/freq[i])]
		i += 1
	print (delta_x)
	print (avg_x)
	print (delta2_x)
	print (delta_y)
	print (avg_y)
	print (delta2_y)
	return (avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y)

def risk(a,x,y,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion,loss):
	r = 0
	for w in range(0,4):
		r += loss[a][w]*post_prob(x,y,w,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion)
	return r

def minum_risk(x,y,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion,loss):
	risklist = []
	for i in range(0,4):
		risklist += [risk(i,x,y,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion,loss)]
	r = risklist.index(min(risklist))
	return (r+1)

def main():
	test_File = open("test.csv","r")
	result_File = open("result.csv","w",newline ='')
	reader = csv.reader(test_File)
	writer = csv.writer(result_File)
	avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y = compute()
	proportion = [0.15, 0.20, 0.30, 0.35]
	loss = [[0,1,4,1],
			[1,0,1,4],
			[4,1,0,1],
			[1,4,1,0]]
	writer.writerow(("X坐标","Y坐标","实际分类","预测分类","预测是否正确"))
	for line in reader:
		x = float(line[0])
		y = float(line[1])
		z = int(line[2])
		r = minum_risk(x,y,avg_x,avg_y,delta2_x,delta2_y,delta_x,delta_y,proportion,loss)
		if(z == r):
			writer.writerow((x,y,z,r,"True"))
		else:
			writer.writerow((x,y,z,r,"False"))
	print ("Done")
	return

main()
		