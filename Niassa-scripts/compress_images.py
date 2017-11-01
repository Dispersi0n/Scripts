import sys, os, glob, random, getpass, time
from PIL import Image
from shutil import move, copytree, ignore_patterns
from panoptes_client import Project, Panoptes, Subject, SubjectSet

##########################################
# Usage:
# Place this file in the same directory as the images folder.
# Use full paths for the input/output directories and the output csv directory.

# <input_directory> : Full path of directory containing this script and the folder of images
# <image_file_extension> : The file extension of all the images in the image folder
# <output_directory> : Full path of directory to put all the images in the folder
# <output_csv> : Full desired path of the output csv mapping log including filename.
# <backup_directory> : Full path of desired backup directory to keep full-res images (Note: cannot be inside input_directory)

# Example
#python compress_images.py ~/Desktop/Testing_Images JPG ~/Desktop/Testing_Images ~/Desktop/Testing_Images/imagemappings.csv ~/Desktop/backup
##########################################


# Start Timer
t0 = time.time()

# make sure we have 6 arguments
if len(sys.argv) < 5:
    print ("format: python compress_images.py <input_directory> <image_file_extension> <output_directory> <output_csv> <backup_directory>")
    exit(1)

# argument variables
input_directory = sys.argv[1]
image_file_extension = sys.argv[2]
output_directory = sys.argv[3]
output_csv = sys.argv[4]
backup_directory = sys.argv[5]

# Get Zooniverse credentials
username = raw_input("What is your Zooniverse username?: ")
password = getpass.getpass("What is your Zooniverse password?: ")
site = raw_input("What is the site name? (ex. Serengeti, Niassa, etc.): ")
subject_set_name = raw_input("What would you like to name the subject set on Zooniverse?: ")
print "\n"

#Connect to Zooniverse with inputted credentials, error out if broken.
print "Connecting to Zooniverse with username and pasword..."
try:
	Panoptes.connect(username=username, password=password)
	project = Project.find(slug='meredithspalmer/snapshot-'+str.lower(site))
	print "Connected to Zooniverse!"
except Exception, e:
	print e
	exit(1)

#Backup all full-res images to folder
print "Backing up all full-resolution images to "+backup_directory
try:
	copytree(input_directory,backup_directory,ignore=ignore_patterns('*.py','*.csv'))
	print "All images successfully backed up!"
except OSError as exc:
	print exc
	exit(1)

# Open output file, create if doesn't exist
f = open(output_csv,'w+')
f.write("New filename,Old Filename,Old Filepath\n")

# set quality score
quality = 17
print "Quality has been set to "+str(quality)

# Function to move all files out of subdirectory and into indicated root folder (normally the input directory)
def move_to_main_folder(main_dir):
	# Get a list of all subdirectories of main_dir
	subdirs = filter(os.path.isdir,
	                 [os.path.join(main_dir, path)
	                  for path in os.listdir(main_dir)])

	# For all subdirectories,
	# collect all files and all subdirectories recursively
	for subdir in subdirs:
	  files_to_move = []
	  subdirs_to_remove = []
	  for dirpath, dirnames, filenames in os.walk(subdir):
	    files_to_move.extend([os.path.join(dirpath, filename)
	                          for filename in filenames])
	    subdirs_to_remove.extend([os.path.join(dirpath, dirname)
	                              for dirname in dirnames])

	  # To move files, just rename them replacing the original directory
	  # with the target directory (subdir in this case)
	  for filename in files_to_move:
	    source = filename
	    destination = os.path.join(main_dir, os.path.basename(filename))
	    os.rename(source, destination)

	  # Reverse subdirectories order to remove them
	  # starting from the lower level in the tree hierarchy
	  subdirs_to_remove.reverse()

	  # Remove subdirectories
	  for dirname in subdirs_to_remove:
	    os.rmdir(dirname)

# Move all files to root directory
print "Moving all files to "+output_directory
move_to_main_folder(input_directory)

# Get file paths of all files with our desired extension
directory_files = glob.glob(input_directory+"/*."+image_file_extension)

# Make output directory and raise error if exists
if os.path.isdir(output_directory)==True:
	print "Output directory already exists. Skipping creation...\n"
else:
	os.makedirs(output_directory)

# Loop through files in directory, convert to desired quality and log mappings in csv file.
print "Starting filename anonymization...\n"
for path in directory_files:
	old_filename = os.path.basename(path)
	print "Old Filename: "+old_filename
	filepath, file_extension = os.path.splitext(path)
	random_list = random.sample(range(10000),3)
	R1 = random_list[0]
	R2 = random_list[1]
	R3 = random_list[2]
	
	new_filename = str(R1)+str(R2)+str(R3)+file_extension
	print "New Filename: "+new_filename
	f.write(new_filename+","+old_filename+","+os.path.abspath(path)+"\n")

	# Perform image conversion and quality change
	try:
		im = Image.open(path)
		im.thumbnail(im.size)
		im.save(output_directory+"/"+new_filename, "JPEG", quality=quality)
		os.remove(path)
	except Exception, e:
		print e

print "File anonymization complete!\n"
# ------------------- Start Panoptes Zooniverse work -------------------

# Get list of images in output directory
image_list = glob.glob(output_directory+'/*.JPG')

subject_set = SubjectSet()
subject_set.links.project = project
subject_set.display_name = subject_set_name
subject_set.save()

image_uploaded_count = 0
# Add image to Zooniverse using path
for path in image_list:
	subject = Subject()
	subject.links.project = project
	subject.add_location(path)
	subject.metadata['attribution'] = site
	subject.metadata['license'] = 'Snapshot Safari & University of Minnesota Lion Project'
	subject.save()
	subject_set.add(subject)
	print "Uploaded image: "+os.path.basename(path)
	image_uploaded_count = image_uploaded_count + 1

# Stop timer
t1 = time.time()
total = t1-t0

print "\nTotal number of images uploaded: " + str(image_uploaded_count)
print "Time taken: " + str(total/60) + " minutes."