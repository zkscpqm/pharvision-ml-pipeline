# pharvision-ml-pipeline


## Running instructions 

*(Requires Python 3.9+ for := syntax)*


### Arguments

#### Pipeline definition file (REQUIRED)
 
 **--pipeline=str**
 - A path to the pipeline definition file (eg: .\pipelines\pipeline_big.txt)

#### Target (REQUIRED)

 **--target=str**
 - The name of the model whose execution will be evaluated (eg: MM2)

#### CPU Cores (Default=1)
 **--cpu_cores=int**
 - Number of components to be executed in parallel

#### Save To (Default=.)
 **--save_to=str**
 - The *directory* where to save the report

#### Show (Default=False)
 **--show=bool**
 - Should the report be flushed to stdout?

### Windows
    python .\main.py --pipeline=pipelines\pipeline_big.txt --target=MM2 --cpu_cores=6 --save_to=reports --show=True

### Linux
    python ./main.py --pipeline=pipelines/pipeline_big.txt --target=MM2 --cpu_cores=6 --save_to=reports --show=True


