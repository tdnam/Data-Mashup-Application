import os
import shutil
import zipfile
from subprocess import run

datasets_folder = "datasets"

script_lines_folder = "the-simpsons-by-the-data"
path_to_script_lines_script = "scripts/download_script_lines.sh"

pictures_folder = "the-simpsons-characters-dataset"
path_to_pictures_script = "scripts/download_pictures.sh"

def download_dataset(new_folder, script, unzip_more):
	""" Download a specific dataset. A script is given to download
	the file, and then unzipping and moving is done here.
	"""
	zip = new_folder + ".zip"
	zipped_to = datasets_folder+ "/" + zip
	path_to_new_folder = datasets_folder + "/" + new_folder
	if os.path.isdir(path_to_new_folder) and len(os.listdir(path_to_new_folder)) > 0:
		return

	os.makedirs(path_to_new_folder, exist_ok=True)
	run(["sh", script])
	os.rename(zip, zipped_to)
	zip_ref = zipfile.ZipFile(zipped_to, 'r')
	zip_ref.extractall(path_to_new_folder)
	zip_ref.close()
	os.remove(zipped_to)

	if not unzip_more:
		return
	removable = "kaggle_simpson_testset.zip"
	removable2 = "simpsons_dataset.tar.gz"
	path_to_removable = path_to_new_folder + "/" + removable
	path_to_removable2 = path_to_new_folder + "/" + removable2
	os.remove(path_to_removable)
	os.remove(path_to_removable2)
	another_folder = "simpsons_dataset"
	path_to_another_folder = path_to_new_folder + "/" + another_folder
	path_to_another_zip = path_to_another_folder + ".zip"
	zip_ref_another = zipfile.ZipFile(path_to_another_zip, 'r')
	zip_ref_another.extractall(path_to_another_folder)
	zip_ref_another.close()
	os.remove(path_to_another_zip)

	temp_folder = "tempfolder"
	path_to_real_folder = path_to_another_folder + "/" + another_folder
	path_to_temp_folder = path_to_new_folder + "/" + temp_folder
	os.rename(path_to_real_folder, path_to_temp_folder)
	shutil.rmtree(path_to_another_folder, ignore_errors=True)
	os.rename(path_to_temp_folder, path_to_another_folder)

def download_datasets():
	""" Download the required datasets. """
	os.makedirs(datasets_folder, exist_ok=True)
	download_dataset(script_lines_folder, path_to_script_lines_script, unzip_more=False)
	download_dataset(pictures_folder, path_to_pictures_script, unzip_more=True)
