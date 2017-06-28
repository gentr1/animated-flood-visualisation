
import sys
import subprocess
import os

from Scale_ASCII_32bit import getAsciiTerrainIntScaler

from ConvertToPicture101 import convertAsciiToTiffRGBA
from ConvertToPicture101 import getFloodDepths

import gdal

import argparse

##----------------------------------------------------------------------------------------------------------

verbose = False

#---------------------------------------------------------------
# caddies program parameters
CADDIES_program = "caflood_64.exe"#"cafloodpro_64.exe"
CADDIES_program_location = ""

CADDIES_program_args_inputFolder =  "MillBrock/"
CADDIES_program_args_inputSetupFile = "test2_10m.csv"

CADDIES_program_args_outputFolder = "outs/"



# note this could be retrieved from the setup file
CADDIES_program_outputFile_depths = "Millbrock2_10m_WDraster_PEAK.asc"
CADDIES_program_outputFile = "Millbrock2_10m_WLraster_WLPEAK.asc"
#---------------------------------------------------------------
# from Scale_ASCII_32bit import getAsciiTerrainIntScaler
# parameters


orinialTerrain_inputFilePath = CADDIES_program_args_inputFolder
# again could retrieve from setup file
orinialTerrain_inputFileName = "millbrook_DTM_10m_resample1m.asc"

margin_floor=0.0
additional_height=10.0
#---------------------------------------------------------------
#from ConvertToPicture101 import convertAsciiToTiffRGBA
# parameters

#convertAsciiToTiffRGBA(fileName, increase, outName):

Conversion_inputFileName = CADDIES_program_args_outputFolder + CADDIES_program_outputFile

Conversion_outputFileName = CADDIES_program_args_outputFolder + os.path.splitext(CADDIES_program_outputFile)[0]+'_RGBA_scaled.tif'

#---------------------------------------------------------------
# gdal translate parameters

translate_outputFilename = CADDIES_program_args_outputFolder + 'millbrook-flood-2.png'#os.path.splitext(CADDIES_program_outputFile)[0]+'_RGBA_scaled.png'




##----------------------------------------------------------------------------------------------------------

addtional_Flood_Height = 0.0

zeroNoFloodArea = False
tolerance = 0.1
runSim = True

############################################################################################################

# arguements

parser = argparse.ArgumentParser() 


parser.add_argument('-CADDIES_program_path', nargs =1,help="The directory/path to the CADDIEs Application")
parser.add_argument('-CADDIES_input_path', nargs =1,help="The directory/path to the CADDIEs setup files")
parser.add_argument('-output_path', nargs =1,help="The directory/path to output files to")
parser.add_argument('-addtional_Flood_Height', nargs =1,help="Depth added to flooded area's")
parser.add_argument('-zero_noFlood', nargs =1, help="Output terrain Level where no flood, set the tolerance")

# flags
parser.add_argument('-GPU', action='store_true', help="Activate the GPU version")
#parser.add_argument('-zero_noFlood', action='store_true', help="Output zero where no flood")

parser.add_argument('-noSim', action='store_true', help="Don't run the simulation part")


args = parser.parse_args()
#---------------------------------------------------------------
if args.CADDIES_program_path is not None:
	CADDIES_program_location = args.CADDIES_program_path
if args.GPU:
	CADDIES_program = "caflood_GPU_64.exe"
if args.CADDIES_input_path is not None:
	CADDIES_program_args_inputFolder = args.CADDIES_input_path
if args.output_path is not None:
	CADDIES_program_args_outputFolder = args.output_path
#
if args.addtional_Flood_Height is not None:
	addtional_Flood_Height = float(args.addtional_Flood_Height[0])
if args.zero_noFlood is not None:
	zeroNoFloodArea = True
	tolerance = float(args.zero_noFlood[0])
	#print(tolerance)
if args.noSim:
	runSim = False
	


CADDIES_program_args = [CADDIES_program_location+CADDIES_program, '/WCA2D']

CADDIES_program_args.append(CADDIES_program_args_inputFolder)
CADDIES_program_args.append(CADDIES_program_args_inputSetupFile)
CADDIES_program_args.append(CADDIES_program_args_outputFolder)
	
##----------------------------------------------------------------------------------------------------------
#print(CADDIES_program_args)

# call caddies application, and wait for completion
if runSim:
	subprocess.call(CADDIES_program_args)


# Call scaling function to find min,max and scaling factor
(h_scale,h_range,min_height,max_height) = getAsciiTerrainIntScaler(orinialTerrain_inputFilePath,orinialTerrain_inputFileName,margin_floor,additional_height,False)

if verbose:		
	print("min_height: " + str(min_height) )
	print("max_height: " + str(max_height) )
	print("h_range   : " + str(h_range) )
	print("h_scale   : " + str(h_scale) )
	
	#print("Conversion_inputFileName   : " + Conversion_inputFileName )
	#print("Conversion_outputFileName   : " + Conversion_outputFileName )

#flood_depths = None
#if args.addtional_Flood_Height is not None or zeroNoFloodArea:
flood_depths = getFloodDepths(CADDIES_program_args_outputFolder+CADDIES_program_outputFile_depths)
terrain_levels = getFloodDepths(orinialTerrain_inputFilePath + orinialTerrain_inputFileName)
#
convertAsciiToTiffRGBA(Conversion_inputFileName, h_scale, Conversion_outputFileName,flood_depths,terrain_levels,addtional_Flood_Height,zeroNoFloodArea,tolerance)

## gdal translate, from tiff to png

#Open existing dataset
src_ds = gdal.Open( Conversion_outputFileName )

#Open output format driver, see gdal_translate --formats for list
format = "PNG"
driver = gdal.GetDriverByName( format )

#Output to new format
dst_ds = driver.CreateCopy( translate_outputFilename, src_ds, 0 )

#Properly close the datasets to flush to disk
dst_ds = None
src_ds = None



#---------------------------------------------------------------
if verbose:	
	print("BLAH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!?! program ends....")