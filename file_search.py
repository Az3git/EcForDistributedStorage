import os

#Returns the names list of files in a directory
def list_of_data_files(data_location):
    list_of_name = []
    for entry in os.listdir(data_location):
        if os.path.isfile(os.path.join(data_location, entry)):
            list_of_name.append(entry)
    return list_of_name

#Returns a list of files located in the storage
def list_of_encode_files(storage_location):
    read_file = []
    with open(storage_location + '/' + 'name_storage_files.txt', 'r') as file:
        for line in file:
            read_file.append(line)
    read_file = [line.rstrip() for line in read_file]
    return read_file

# Returns a dictionary whose keys are the names of the files
# in the storage and whose values
# are the indexes of existing fragments and missing fragments.
# For example {'1.pdf': [[0,1,3],[2]}
def dict_filenames_surv_miss_fragments(k, m, storage_location):
    encode_filenames = list_of_encode_files(storage_location)
    result_dict = {}
    for filename in encode_filenames:
        surv_miss_nodes_indexes = [[],[]]
        for i in range(k+m):
            for root, dir, files in os.walk(storage_location):
                if (filename + '.' + str(i)) in files:
                    surv_miss_nodes_indexes[0].append(i)
        for j in range(k+m):
            if j not in surv_miss_nodes_indexes[0]:
                surv_miss_nodes_indexes[1].append(j)
        result_dict[filename] = surv_miss_nodes_indexes
    return result_dict

