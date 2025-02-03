[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/model-to-model-evaluation-code)](https://api.reuse.software/info/github.com/SAP-samples/model-to-model-evaluation-code)

# Round-trip-correctness to evaluate BPMN generation

## Description
This repository tests the idea of a proxy evaluation method for text to BPMN model pipeline.
The proxy evaluation involves a round-trip pipeline, "text to bpmn to text" or "bpmn to text to bpmn" and calculating an average similarity metric we call RTC in the absence of a ground truth BPMN/text.
To show if the proxy method is effective, we first must investigate how the existing BPMN to BPMN evaluation from [model_evaluation](./model_evaluation) module correlates with the text to text similarity methods from [text_evaluation](./text_evaluation).
This work is inspired by [this](https://arxiv.org/abs/2402.08699) publication on text to code round-tripping.  



## Requirements and set up

The requirements are in this [pyproject.toml](./pyproject.toml) file. After cloning the repository, run:

```shell
poetry install
```

## Getting started

To run the LLM specific pipeline, use a command similar to this:
```shell
screen -d -m python genai_gpt_pipeline.py --model-path ./data/pet/ground_json --text-path ./data/pet/process_descriptions --example pet --direction t2t 
```
or run the LLM agnostic pipeline as:
```shell
screen -d -m python universal_pipeline.py --llm gemini --model-path ./data/pet/ground_json --text-path ./data/pet/process_descriptions --example pet --direction t2t 
```
The csv files are written to the results directory. The jupyter notebooks are used to visualize the results. 


## Known Issues
No known issue.

## How to obtain support
[Create an issue](https://github.com/SAP-samples/model-to-model-evaluation-code/issues) in this repository if you find a bug or have questions about the content.



## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) 2024 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0.

