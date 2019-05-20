#!/home/squalaob/virtualenv/kaori.squarepotato.com/2.7/bin/python
import cgi, os
import cgitb
import sys
import traceback
import shutil
import zipfile
import imagepro

print "Content-Type: text/html"
print
sys.stderr = sys.stdout
try:
	form = cgi.FieldStorage()
	#Get filename here.
	fileitem = form["inputFile"]
	fn = os.path.basename(fileitem.filename)
	open("/tmp/" + fn, "wb").write(fileitem.file.read() )
	zip_ref = zipfile.ZipFile("/tmp/" + fn, "r")
	for ifile in zip_ref.namelist():
		if "__MACOSX" in ifile:
			continue
		if ifile.endswith(".png"):
			image = zip_ref.open(ifile)
			nospacefilename = image.name.replace(" ", "_")
			f = open(os.path.join("tmp", os.path.basename(nospacefilename) ), 'wb')
		        shutil.copyfileobj(image, f) 
			f.close()
			response = imagepro.imagepro(os.path.basename(nospacefilename) )
except:
	print "\n\n<pre>"
	traceback.print_exc()
	print "</pre>"

print "Location: http://kaori.squarepotato.com/index.html"
print
