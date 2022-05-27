from pyeclib.ec_iface import ECDriver
import create_config
import file_search
import sys
import os.path

try:
    k, m, ec_type, data_location, storage_location, recovered_data_location = create_config.apply_configuration()
except FileNotFoundError:
    print('You need to create a configuration file. Run the create_config.py')
    sys.exit()
create_config.print_configuration(k,m,ec_type,data_location,storage_location,recovered_data_location)

print('\nData was found: ')
encode_files = file_search.list_of_encode_files(storage_location)
for filename in encode_files:
    print(filename)

print('\nwhich files need to be decoded?\nPass a list of files, or "all" in order to decode all files')
files_input = input()
if files_input == 'all':
    files_to_decode = encode_files
else:
    files_to_decode = files_input.split()

ec_driver = ECDriver(k=k, m=m, ec_type=ec_type)

for elem in files_to_decode:
    fragment_list = []

    #read fragments
    for i in range(k+m):
        try:
            with open("%s" % (storage_location + '/disk' + str(i) + '/' + elem + '.' + str(i) ), "rb") as fp:
                fragment_list.append(fp.read())
        except:
            pass

    # decode
    decoded_file = ec_driver.decode(fragment_list)

    # write
    with open("%s" % (recovered_data_location + '/' + elem), "wb") as fp:
        fp.write(decoded_file)

#Data recovery check
check = True
for filename in files_to_decode:
    if not os.path.exists(recovered_data_location + '/' + filename):
        check = False
if not check:
    print('Something went wrong')
else:
    print('Recover data was successful')