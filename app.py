from flask import Flask
from flask import send_file
import ocean
seasurfaceheightapp = Flask(__name__)

@seasurfaceheightapp.route('/')
def getimage():
	compressedfilename = 'nrt_global_allsat_madt_h_latest.nc.gz'
	uncompressedfilename = 'netcd.txt'
	ocean.getFileFromServer(compressedfilename)
	ocean.uncompressFile(compressedfilename, uncompressedfilename)
	ocean.plotdata(uncompressedfilename)
	imagefilename = 'out.png'
	return send_file(imagefilename, mimetype='image/gif')

if __name__ == '__main__':
    seasurfaceheightapp.run()