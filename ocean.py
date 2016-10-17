# basic NOMADS OpenDAP extraction and plotting script
import mpl_toolkits
mpl_toolkits.__path__.append('/Library/Python/2.7/site-packages/mpl_toolkits')
from mpl_toolkits.basemap import Basemap
from ftplib import FTP
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import gzip
import struct


def getFileFromServer(filename):
	ftp = FTP('ftp.aviso.altimetry.fr')
	ftp.login('apl_dasaro','gpo68zr')      
	WD = ftp.cwd('global/near-real-time/grids/madt/all-sat-merged/h')
	localfile = open(filename, 'wb')
	ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

def getuncompressedsize(filename):
    with open(filename, 'rb') as f:
        f.seek(-4, 2)
        return struct.unpack('I', f.read(4))[0]	


def uncompressFile(filename, newfilename):
	sz = getuncompressedsize(filename)
	with gzip.open(filename, 'rb') as f:
		file_content = f.read(sz - 3)
		
		
		newfile = open(newfilename, "w")

		newfile.write(file_content)
		newfile.close()

def plotdata(filename):
	plt.figure()
	file = netCDF4.Dataset(filename)
	print file.variables.keys()
	lat  = file.variables['lat'][:]
	lon  = file.variables['lon'][:]
	adt = file.variables['adt'][:,:,:]
	time = file.variables['time'][:]
	file.close()
	data = adt
	lonmin = 70
	lonmax = 100
	latmin = 0
	latmax = 23

	# m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), resolution='c')
	m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lonmin, urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, resolution='c')

	x, y = m(*np.meshgrid(lon,lat))

	# plot the field using the fast pcolormesh routine 
	# set the colormap to jet.

	m.pcolormesh(x,y,data[0],shading='flat',cmap=plt.cm.jet)
	# m.colorbar(location='right')


	# Add a coastline and axis values.

	m.drawcoastlines()
	m.fillcontinents()
	# m.drawmapboundary()
	# m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
	# m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

	# plt.title('Example 1: NWW3 Significant Wave Height from NOMADS')
	# plt.show()
	# plt.savefig('plot.png')

	# plt.savefig('plot.png')
	plt.savefig('out.png', bbox_inches='tight', pad_inches=0)



# set up the figure


# compressedfilename = 'nrt_global_allsat_madt_h_latest.nc.gz'
# uncompressedfilename = 'netcd.txt'
# # getFileFromServer(compressedfilename)
# # uncompressFile(compressedfilename, uncompressedfilename)
# plotdata(uncompressedfilename)



# # Since Python is object oriented, you can explore the contents of the NOMADS
# # data set by examining the file object, such as file.variables.

# # The indexing into the data set used by netCDF4 is standard python indexing.
# # In this case we want the first forecast step, but note that the first time 
# # step in the RTOFS OpenDAP link is all NaN values.  So we start with the 
# # second timestep

# # Plot the field using Basemap.  Start with setting the map
# # projection using the limits of the lat/lon data itself:

# m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
#   urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
#   resolution='c')

# convert the lat/lon values to x/y projections.

# x, y = m(*np.meshgrid(lon,lat))

# # plot the field using the fast pcolormesh routine 
# # set the colormap to jet.

# m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
# m.colorbar(location='right')

# # Add a coastline and axis values.

# m.drawcoastlines()
# m.fillcontinents()
# m.drawmapboundary()
# m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
# m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

# # Add a colorbar and title, and then show the plot.

# plt.title('Example 1: NWW3 Significant Wave Height from NOMADS')
# plt.show()
