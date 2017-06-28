## CreateMask program

#import sys
#import argparse

#import ogr
import gdal


import numpy

##----------------------------------------------------------------------------------------------------------
def convertAsciiToTiffRGBA(fileName, increase, outName,flood_depths,terrainLevels,additonal_Flood_Heights=0.0,zeroNoFloodArea = False,tolerance=0.1):





	#tolerance = 0.0001
	#tolerance = 0.01
	#tolerance = 0.1

	

	#####################################

	terrain_source_ds = gdal.Open(fileName)

	args = terrain_source_ds.GetGeoTransform()
	
	#print(args)

	band = terrain_source_ds.GetRasterBand(1)

	ulx = int(args[0])
	cellSize = int(args[1])
	
	uly = int(args[3])
	xres = int(args[1])
	yres = int(args[5])

	lrx = ulx + int(terrain_source_ds.RasterXSize * xres)

	lry = uly + int(terrain_source_ds.RasterYSize * yres)



	pixelWidth = cellSize
	pixelHeight = cellSize # depending how fine you want your raster

	# lazy coding....
	x_min = ulx
	x_max = lrx
	y_min = lry
	y_max = uly


	cols = int((x_max - x_min) / pixelHeight)

	rows = int((y_max - y_min) / pixelWidth)
	
	#print("cols: " +str(cols))
	#print("rows: " +str(rows))

	data = band.ReadAsArray(0, 0, cols, rows).astype(numpy.float)

	if additonal_Flood_Heights is not 0.0:
		#data = data + additonal_Flood_Heights
		#data[flood_depths.nonzero()] += additonal_Flood_Heights
		data[flood_depths >= tolerance] += additonal_Flood_Heights
		
	if zeroNoFloodArea:
		#data[flood_depths == 0.0] = 0
		data[flood_depths < tolerance] = terrainLevels[flood_depths < tolerance]
	

	#print(data[0][0])

	data *= increase
	
	#print(data[0][0])

	dataInt = data.astype(numpy.uint32)
	
	#print(dataInt[0][0])
	#print(numpy.binary_repr(dataInt[0][0]))

	
	#print(numpy.binary_repr(numpy.right_shift(dataInt[0][0],8)))
	
	dataByte1 = dataInt.astype(numpy.uint8)
	dataByte2 = numpy.right_shift(dataInt,8).astype(numpy.uint8)
	dataByte3 = numpy.right_shift(dataInt,16).astype(numpy.uint8)
	dataByte4 = numpy.right_shift(dataInt,24).astype(numpy.uint8)
	
	#print(dataByte1[0][0])
	#print(dataByte2[0][0])
	#print(dataByte3[0][0])
	#print(dataByte4[0][0])
	#print("-----------------------")

	#print(numpy.binary_repr(dataByte1[0][0]))
	#print(numpy.binary_repr(dataByte2[0][0]))
	#print(numpy.binary_repr(dataByte3[0][0]))
	#print(numpy.binary_repr(dataByte4[0][0]))
	
	##-----------------------------------------------------------------





	target_ds = gdal.GetDriverByName("GTiff").Create(outName, cols, rows, 4, gdal.GDT_Byte)
	#target_ds = gdal.GetDriverByName("GTiff").Create(outName, cols, rows, 3, gdal.GDT_Byte)


	args = [0]*6

	args[0] = x_min
	args[1] = pixelWidth
	args[2] = 0
	args[3] = y_max
	#args[3] = y_min
	args[4] = 0
	args[5] = -pixelHeight
	#args[5] = pixelHeight
	target_ds.SetGeoTransform(args)

	dataArray = [dataByte4,dataByte3,dataByte2,dataByte1]


	NoData_value = 0;

	for i in range(len(dataArray)):

		bandOut = target_ds.GetRasterBand(i+1)

		bandOut.SetNoDataValue(NoData_value)

		#bandOut.WriteRaster(0, 0, cols, rows, newData, cols, rows, 0, 0);
		bandOut.WriteArray(dataArray[i])

	bandOut.FlushCache()
##----------------------------------------------------------------------------------------------------------
def getFloodDepths(inputFileWD):

	terrain_source_ds = gdal.Open(inputFileWD)

	args = terrain_source_ds.GetGeoTransform()
	
	#print(args)

	band = terrain_source_ds.GetRasterBand(1)

	ulx = int(args[0])
	cellSize = int(args[1])
	
	uly = int(args[3])
	xres = int(args[1])
	yres = int(args[5])

	lrx = ulx + int(terrain_source_ds.RasterXSize * xres)

	lry = uly + int(terrain_source_ds.RasterYSize * yres)



	pixelWidth = cellSize
	pixelHeight = cellSize # depending how fine you want your raster

	# lazy coding....
	x_min = ulx
	x_max = lrx
	y_min = lry
	y_max = uly


	cols = int((x_max - x_min) / pixelHeight)

	rows = int((y_max - y_min) / pixelWidth)
	
	#print("cols: " +str(cols))
	#print("rows: " +str(rows))

	data = band.ReadAsArray(0, 0, cols, rows).astype(numpy.float)

	#data_addtional_height[data.nonzero()] = addtional_height

	return data


##----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
	
	#fileName = "C:/PROCESSING/Millbrock/outs/Millbrock1_WDraster_PEAK.asc"
	#fileName = "C:/PROCESSING/Millbrock/Millbrock2_10m_WDraster_PEAK.asc"
	fileName = "C:/Prog/GITS/caddies-tests/MillBrock/millbrook_DTM_10m_resample1m.asc"
	#fileName = "C:/PROCESSING/MillBrock/millbrook-DTM_1m.asc"
	#increase = 1000
	#increase = 10000000
	increase = 31122951.413043477
	#outName = "C:/PROCESSING/Millbrock/outs/Millbrock1_WDraster_PEAK_encoded.tif"
	#outName = "C:/PROCESSING/Millbrock/outs/test2.tif"
	#outName = "C:/PROCESSING/Millbrock/millbrook-DTM_1m_RGBA.tif"
	#outName = "C:/PROCESSING/Millbrock/millbrook-DTM_1m_RGBA_scaledLarge.tif"
	#outName = "C:/PROCESSING/Millbrock/Millbrock2_10m_WDraster_PEAK_RGBA_scaleded.tif"
	outName = "C:/PROCESSING/Millbrock/millbrook_DTM_10m_resample1m_RGBA_scaleded.tif"

	convertAsciiToTiffRGBA(fileName,increase,outName)
