import os

def apply_configuration():
    config = []
    with open('config.txt', "r") as file:
        for line in file:
            config.append(line)
    config = [line.rstrip() for line in config]
    return int(config[0]), int(config[1]), config[2], config[3], config[4], config[5]

def print_configuration(k,m,ec_type,data_location,storage_location,recovered_data_location):
    print('Current configuration:\nnumber of data elements k: ', k,
          '\n-number of parity elements m:', m,
          '\n-ec algoritm:', ec_type,
          '\n-data:', data_location,
          '\n-storage:', storage_location,
          '\n-recovered data:', recovered_data_location)

if __name__ == "__main__":
    print('specify the location of Data:')
    data_dir = input()
    print('specify the location of Storage:')
    storage_dir = input()
    print('specify the location of data encode:')
    encode_data_dir = input()
    print('enter number of data elements k:')
    k = int(input())
    print('enter number of parity elements m:')
    m = int(input())
    print("""enter EC algorithm used:
    --liberasurecode_rs_vand
    --jerasure_rs_vand
    --jerasure_rs_cauchy
    --flat_xor_hd_3
    --flat_xor_hd_4
    --isa_l_rs_vand
    --shss""")
    while True:
        ec_type = input()
        if ec_type != 'liberasurecode_rs_vand':
            print('Please select liberasurecode_rs_vand. Other algorithms are not yet available')
        else:
            break

    config_value = [str(k) + '\n',str(m) + '\n',
                    ec_type +'\n',data_dir +'\n',
                    storage_dir +'\n',
                    encode_data_dir +'\n']

    try:
        os.remove('config.txt')
    except:
        pass
    with open('config.txt', "a+") as file:
        file.writelines(config_value)

