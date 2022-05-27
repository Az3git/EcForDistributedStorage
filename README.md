# EcForDistributedStorage
## What is it?

EcFor Distributed Storage is a learning project. The goal was to create a simple distributed storage 
implementation that uses erasure coding to improve storage reliability at low overhead.
To implement erasure coding, the open library PyECLib [1] was taken as a basis.
To simulate distributed storage, the directory is divided into disks.
The number of disks corresponds to the sum k+m of the erasure coding algorithm. When used, pieces of data 
are placed on each of the disks. Thus, the original data can be restored if up to m nodes are lost. Recovery from 1 to m lost nodes based on surviving nodes is also implemented.

## Installation
Creation of virtual environment:

    $ python3 -m venv venv
    
Activation of virtual environment:
    
    $ source venv/bin/activate
 
Installing required dependencies:

    $ pip install -r requirements.txt


    
## Getting started
A configuration file has already been created in the project itself, as well as test data and a storage directory. Below is an instruction for the general case.
To get started, you need to create a configuration file. To do this, run the script:

    $ python3 create_config.py
    
This script will create a config.txt file, which is used by all the tools in the project. The following information must be written to the configuration file:

    --k - number of data elements
    --m - number of parity elements
    --ec_type - the name of the algorithm (Attention! Only liberasurecode_rs_vand is supported)
    --Path to your data
    --Path to storage
    --Path to where you want to store the decoded data
### Tools
encoder:

    encode.py
decoder:

     decode.py
Checking the safety of fragments encoded on storage nodes

     check_nodes.py
Reconstruction of lost fragments

     reconstruction.py
     
## References
[1] PyEClib, this library provides a simple Python interface for implementing erasure codes. To obtain the best possible performance, the underlying erasure code algorithms are written in C. https://pypi.org/project/pyeclib/1.2.0/
