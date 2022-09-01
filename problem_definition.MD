# Data Pipeline Planning
## Problem Statement
You need to optimize a machine learning data pipeline that collects raw data, builds features out of the raw data, and then uses both the raw data and the features to train ML models, and finally build on top of models and train meta-models. 

You are given `n` tasks, each having the following attributes:

- execution time: the time is given in whole minutes - integers
- group: each task may belong to a group of tasks - e.g. raw, feature, model, meta-model or stand-alone task that is not a member of any group 
- dependencies: a list of other tasks, that must be completed to start executing the current task
## Your task

1. Write a python script accepting two command line arguments: `--pipeline` and `--cpu_cores`. The script should parse the `pipeline` text file defining the pipeline and compute the **minimum execution time** of the pipeline given the following constraints:
- you can execute at most `cpu_cores` number of tasks in parallel
- all tasks in a group should be executed before we proceed with another group, i.e. if we started executing a task from a group `g`, the algorithm should not schedule for execution tasks belonging to another group until all tasks in group `g` are completed. The only exception is a task that doesn't belong to any group.

2. The script should also output the scheduling diagram of the optimal solution that shows which tasks from which group were running at time <img src="https://render.githubusercontent.com/render/math?math=t">.


### The structure of the  `pipeline` file:

Each pipeline file consists of `4*n + 1` lines, describing the tasks in the pipeline: 4 lines for each task and a terminating line with value `END`. The properties of each task  are described in 4 consecutive lines:

| Line    | Description                                                   | Example Value
| ------- | ------------| ---------------
|  1      | task name                                                     | A
|  2      | execution time                                                | 3
|  3      | group name, empty line if no group                            | feature
|  4      | comma-separated list of task names that this task depends on, empty line if no group  | B,C,D


## Example

For example, given `cpu_cores=2` a pipeline of 3 tasks **A** (2 minutes) & **B** (1 minute) belonging to group $feature$, and a task **C** (2 minutes) that depends on **B**  and belongs to group $model$ is executed optimally in **4** minutes has the following input and output:

Given a pipeline.txt file:
```txt
A
2
feature

B
1
feature

C
2
model
B
END
```

##### Input:
`python script.py --cpu_cores=2 --pipeline=pipeline.txt`
    
##### Output: 
```sh
Minimum Execution Time = 4 minute
```
- prints or saves a file with the following scheduling diagram:

```
| Time    | Tasks being Executed | Group Name
| ------- | -------------------- | ----------
|  1      | A,B                  | feature                         
|  2      | A                    | feature
|  3      | C                    | model
|  4      | C                    | model

```

##### Explanation

Even though task **C** depends only on **B**, it cannot start executing before task **A** finishes due to the constraint that all tasks in a group should finish before we proceed with another group.


## Test Cases

You can try your solutions on `pipeline_big.txt` and `pipeline_small.txt` pipeline files given in this gist.`