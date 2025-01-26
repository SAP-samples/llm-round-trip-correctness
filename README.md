*blinded for submission*
# Round-trip-correctness to evaluate BPMN generation

## Description
This repository tests the idea of a proxy evaluation method for text to BPMN model pipeline.
The proxy evaluation involves a round-trip pipeline, "text to bpmn to text" and calculating an average text to text similarity in the absence of a ground truth BPMN.
To show if the proxy method is effective, we first must investigate how the existing BPMN to BPMN evaluation from [model_evaluation](./model_evaluation) module correlates with the proxy text to text method.
This work is inspired by [this](https://arxiv.org/abs/2402.08699) publication on text to code round-tripping.  



## Requirements and set up

The requirements are in this [pyproject.toml](./pyproject.toml) file. After cloning the repository, run:

```shell
poetry install
```

## Getting started

To run the pipeline, use a command similar to this:
```shell
screen -d -m python genai_gpt_pipeline.py --model-path ./data/pet/ground_json --text-path ./data/pet/process_descriptions --example pet --direction t2t 
```
The csv files are written to the results directory. The jupyter notebooks are used to visualize the results. 


## Known Issues
No known issue.

## How to obtain support
*blinded for submission* in this repository if you find a bug or have questions about the content.



## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. *blinded for submission* uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) *blinded for submission* or *blinded for submission*. All rights reserved. This project is licensed under the Apache Software License, version 2.0.

