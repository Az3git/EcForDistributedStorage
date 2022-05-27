from pyeclib.ec_iface import ECDriver
import create_config
import file_search
import sys

k, m, ec_type, data_location, storage_location, recovered_data_location = create_config.apply_configuration()
create_config.print_configuration(k,m,ec_type,data_location,storage_location,recovered_data_location)

ec_driver = ECDriver(k=k, m=m, ec_type=ec_type)

files_to_reconstruct = []

filenames_surv_miss_fragments = file_search.dict_filenames_surv_miss_fragments(k,m,storage_location)

for filename in filenames_surv_miss_fragments:
    if len(filenames_surv_miss_fragments[filename][1]) != 0:
        files_to_reconstruct.append(filename)

if len(files_to_reconstruct) == 0:
    print('\nFragments of all files are available on all nodes. Reconstruction is not needed')
    sys.exit()

print('Fragments of the following files are missing on some nodes:')
for file in files_to_reconstruct:
    print(file)
    print('File fragments are contained on node:', filenames_surv_miss_fragments[file][0])
    print('File fragments are missing on nodes:', filenames_surv_miss_fragments[file][1])

print('\nFragments of which files need to be restored?\nPass a list of files, or "all" in order to decode all files')

files_input = input()
if files_input == 'all':
    pass
else:
    files_to_reconstruct = files_input.split()


for file_name in files_to_reconstruct:
    surviving_nodes = filenames_surv_miss_fragments[file_name][0]
    missing_nodes = filenames_surv_miss_fragments[file_name][1]

    name_surviving_fragments = []
    for node in surviving_nodes:
        name_surviving_fragments.append(storage_location + '/disk' + str(node) + '/' +  file_name + '.' + str(node))

    surviving_fragments_data = []
    for name in name_surviving_fragments:
        with open(("%s" % name), "rb") as fp:
            surviving_fragments_data.append(fp.read())

    # fragment recovery
    rec_payload = ec_driver.reconstruct(surviving_fragments_data,missing_nodes)

    count_miss_nodes = int(len(missing_nodes))

    # writing recovered fragments to disks
    i = 0
    for fragment in rec_payload:
        with open(storage_location + '/disk' + str(missing_nodes[i]) + '/' \
                  + file_name + '.' + str(missing_nodes[i]), "wb") as fp:
            fp.write(fragment)
        i = i + 1

#node recovery check
check = True
filenames_surv_miss_fragments = file_search.dict_filenames_surv_miss_fragments(k,m,storage_location)
for filename in filenames_surv_miss_fragments:
    if len(filenames_surv_miss_fragments[filename][1]) != 0:
        check = False
if not check:
    print('Something went wrong, please run check_nodes')
else:
    print('File fragments were successfully restored')