from os.path import isfile, join
from os import listdir


def get_all_file_name(file_path, file_type):
	# file type: for example, .csv .txt .pdf ...

	files_names = [f for f in listdir(file_path) if isfile(join(file_path, f))]
	name_array = []

	for name in files_names:
		if file_type in name:
			name_array.append(name)

	return name_array
