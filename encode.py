from pyeclib.ec_iface import ECDriver
import file_search
import disk_create
import create_config
import sys

try:
    k, m, ec_type, data_location, storage_location, recovered_data_location = create_config.apply_configuration()
except FileNotFoundError:
    print('You need to create a configuration file. Run the create_config.py')
    sys.exit()
create_config.print_configuration(k,m,ec_type,data_location,storage_location,recovered_data_location)

print('\nData was found: ')
for filename in file_search.list_of_data_files(data_location):
    print(filename)

print('\nWhich files need to be encoded?\nPass a list of files, or "all" in order to encode all files')
files_input = input()
if files_input == 'all':
    files_to_encode = file_search.list_of_data_files(data_location)
else:
    files_to_encode = files_input.split(sep = ' ')

ec_driver = ECDriver(k=k, m=m, ec_type=ec_type)

# create storage nodes
disk_create.nodes_create(k+m, storage_location)

for file in files_to_encode:
    # open data file
    with open(("%s/%s" % (data_location, file)), "rb") as fp:
        whole_file_str = fp.read()

    # encode data file
    fragments = ec_driver.encode(whole_file_str)
    i = 0

    # writing fragments to storage nodes
    for fragment in fragments:
        with open("%s/%s.%d" % (storage_location + '/' + 'disk' + str(i), file, i), "wb") as fp:
            fp.write(fragment)
        i += 1

# creating a file containing the name of the files located in the storage
storage_files_name = []
try:
    with open(storage_location + '/' + 'name_storage_files.txt', 'r') as file:
        for line in file:
            storage_files_name.append(line)
except FileNotFoundError:
    pass

with open(storage_location + '/' + 'name_storage_files.txt', "a") as file:
    for line in files_to_encode:
        if line + '\n' in storage_files_name:
            continue
        else:
            file.write(line + '\n')

#checking that files have been successfully written to storage
check = True
filenames_surv_miss_fragments = file_search.dict_filenames_surv_miss_fragments(k,m,storage_location)

for filename in files_to_encode:
    if len(filenames_surv_miss_fragments[filename][1]) != 0:
        check = False

if not check:
    print('Something went wrong, please run check_nodes')
else:
    print('Writing data to storage was successful')

