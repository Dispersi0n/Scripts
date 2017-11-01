import os
from PIL import Image

path = '/Users/Axl/Desktop/Niassa_S1'

# for filename in os.listdir(path):
# 	im = Image.open(path+"/"+filename)
# 	try:
# 		im.verify()
# 		print 'Good image: %s' % path+filename
# 	except IOError as e:
# 		print 'Bad image: %s' % path+filename

for directory,subdirectories,files in os.walk(path):
	for file in files:
		im = Image.open(os.path.join(directory,file))
		try:
			im.verify()
			print 'Good image: %s' % os.path.abspath(file)
		except IOError as e:
			print 'Bad image: %s' % os.path.abspath(file)