# Data Simulator
Used to generate datasets based on dictionary


# Motivation

It is sometimes necessary to create simulated data when it is impractical to obtain real data. This is an important technique to generate data that can be used for building models or running services over datasets that may have protected information or may not be available for legal reasons.  The functions in this simulation suite allow a user to:

* Simulate and validate data
* Organize simulated data by nodes in a data model and export to json for easy upload.


## Basic Functionality

#### Dictionary Validation

This function is very helpful for user to validate dictionary
```
data-simulator validate --url https://s3.amazonaws.com/dictionary-artifacts/bhcdictionary/0.4.3/schema.json
```

Required arguments:
* url: s3 dictionary link

#### Simulating data

Simulate the data using dictionary
```
data-simulator simulate --url https://s3.amazonaws.com/dictionary-artifacts/bhcdictionary/0.4.3/schema.json --path ./data-simulator/sample_test_data --program DEV --project test
```

Required arguments:
* url: s3 dictionary link
* path: path to save files to
* program
* project

Optional arguments:
* max_samples: maximum number of instances for each node. default is 1
* required_only: only simulate required properties
* random: randomly generate the numbers of node instances (up to `max_samples`). If this argument is not used, all nodes have `max_samples` instances
* node_num_instances_file ./file.json: generate the numbers of node instances specified in the JSON file. The file should contain the number of instances (integer)  to generate for each node name, for example: `{"submitted_unaligned_reads": 100}`. `max_samples` instances are generated for nodes that are not specified in the file.
* consent_codes: whether to include generation of random consent codes

#### Submission Order

Generate a submission order given a node name and a dictionary
```
data-simulator submission_order --url https://s3.amazonaws.com/dictionary-artifacts/bhcdictionary/0.4.3/schema.json --node_name case --path ./data-simulator/sample_test_data
```

Required arguments:
* url: s3 dictionary link
* path: path to save file to

Optional arguments:
* node_name: node to generate the submission order for. by default, the command selects a random data file node
* skip: skip raising an exception if gets an error

#### Submitting Data

Submit the data via sheepdog api

```
data-simulator submitting_data --host http://devplanet.planx-pla.net --project DEV/test --dir ./data-simulator/sample_test_data --access_token_file ./token --chunk_size 10
```

Required arguments:
* dir: path containing data
* host
* project: program name and project code separated by a forward slash
* access_token_file

Optional arguments:
* chunk_size: default is 1

## Setup
Poetry needs to be installed before installing data simulator.
Please follow https://python-poetry.org/docs/#installation for installing poetry.

To install data simulator, run the following command.
```
poetry install -vv
```

## Running tests locally
```
poetry install -vv
poetry run pytest -vv ./tests
```


## PCDC notes
    - `poetry install -vv`
    - `data-simulator simulate --url https://pcdc-gen3-dictionaries.s3.amazonaws.com/pcdc-schema-compose-20220106.json --path /path/to/save/simulated/data --program pcdc --project 20211006`
    - use the `max_samples` params to create more than one record
    - submit all with `data-simulator submitting_data --host http://devplanet.planx-pla.net --project DEV/test --dir ./data-simulator/sample_test_data --access_token_file ./token --chunk_size 10`

    poetry run data-simulator simulate --url https://pcdc-gen3-dictionaries.s3.amazonaws.com/pcdc-schema-dev-20220106.json --path ~/Downloads/ --program pcdc --project 20211006 --max_samples 400 --random 

python main.py simulate --url https://pcdc-compose-docs.s3.amazonaws.com/pcdc-schema-compose-20220516.json --path ./Downloads/sample_test_data --program pcdc --project 20220602 --max_samples 400 --random 

python main.py simulate --url https://pcdc-compose-docs.s3.amazonaws.com/pcdc-schema-compose-20220516.json --path ~/Projects/GEN3_dev/dev_tools/gen3_scripts/gen3_load/fake_data/data-simulator --program pcdc --project 20220602 --max_samples 400 --random
