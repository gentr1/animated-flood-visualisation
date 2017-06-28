#import json
import math
import os
from copy import copy, deepcopy


##----------------------------------------------------------------------------------------------------------
def getAsciiTerrainIntScaler(inputFilePath,inputFileName,margin_floor=0.0,additional_height=10.0,verbose = False):

	#verbose = True
	#margin_floor=0.0
	#additional_height=10.0

	#inputFileName = "tq02m.asc"
	#inputFilePath = "C:/Prog/GITS/caddies-tests/TQ/"

	min_height=9999.0
	max_height=-9999.0
	mylines=[]

	# open file, and find min and max within range, and read the lines floats
	with open(inputFilePath+inputFileName, 'r') as f:
		lines = f.readlines()
		# remove first 6 lines, as these contain the file attributes
		lines = lines[6:]
		for i in range(len(lines)):
			listnb = map(float, lines[i].split())
			for fg in listnb:
				if ((fg<min_height) and ( fg!=-9999.0)):
					min_height = fg
				if ((fg>max_height) and ( fg!=9999.0)):
					max_height = fg
			mylines.append(listnb)

			
	# round the min/max
	min_height = math.floor(min_height)
	max_height = math.ceil(max_height)
	# 
	h_range=(max_height+additional_height) - (min_height-margin_floor)
	#h_scale = 1.0#(max_height - min_height + margin_floor+additional_height)/(max_height-(-9999.0))#0.3

	h_scale = 4294967295.0/h_range

			
	if verbose:		
		print("min_height: " + str(min_height) )
		print("max_height: " + str(max_height) )
		print("h_range   : " + str(h_range) )
		print("h_scale   : " + str(h_scale) )

	return (h_scale,h_range,min_height,max_height)
		
##----------------------------------------------------------------------------------------------------------

if __name__ == "__namin__":

	inputFilePath =  "C:/Prog/GITS/caddies-tests/MillBrock/"


	getAsciiTerrainIntScaler(inputFilePath,inputFileName,margin_floor=0.0,additional_height=10.0,verbose = False)
	
	
