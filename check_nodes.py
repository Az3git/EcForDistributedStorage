import file_search
import create_config

if __name__ == '__main__':
    k, m, ec_type, data_location, storage_location, recovered_data_location = create_config.apply_configuration()
    create_config.print_configuration(k, m, ec_type, data_location, storage_location, recovered_data_location)

    print('data was found: ')
    encode_filenames = file_search.list_of_encode_files(storage_location)
    for file in encode_filenames:
        print(file)

    print('''
which files fragments need to check?
A list of files, or "all" in order to check all file fragments''')

    files_input = input()
    if files_input == 'all':
        files_to_check = encode_filenames
    else:
        files_to_check = files_input.split()

    filenames_surv_miss_fragments = file_search.dict_filenames_surv_miss_fragments(k,m,storage_location)
    for file in files_to_check:
        if len(filenames_surv_miss_fragments[file][0]) == k + m:
            print('fragments', file, 'available on all nodes')
        else:
            print('fragments',file,'missing on some nodes. Fragments are on the nodes under the number:')
            print(filenames_surv_miss_fragments[file][0])
            print('fragments', file, 'missing from nodes:')
            print(filenames_surv_miss_fragments[file][1])



