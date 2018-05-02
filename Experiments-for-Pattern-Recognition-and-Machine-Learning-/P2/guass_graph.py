import numpy as np
import math
import csv

def Guass(u,omega,omega2,x):
	PI = 3.1415926
	r = math.exp(-(x-u)*(x-u)/2/omega2)/omega/math.sqrt(2*PI)
	return r
def main():
	csvFile = open("guass_Graph.csv","w",newline = '')
	csv_writer = csv.writer(csvFile)
	for i in range(-60,60):
		x = i/10
		print (i,x)
		y1 = Guass(-2.12262,1.21482,1.475789,x)
		y2 = Guass(2.10192,1.31631,1.732677,x)
		y3 = (y1*0.9)/(y1*0.9+y2*0.1)
		y4 = 1 - y3
		y5 = y3 -y4
		y6 = y4 - y3*6
		csv_writer.writerow((x,y1,y2,y3,y4,y5,y6))
	return

main()
		
		
		
		
		
		