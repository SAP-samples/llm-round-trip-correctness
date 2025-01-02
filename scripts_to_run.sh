#!/bin/bash 
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/realset_diverse/ground_truth/ --text-path ./data/realset_diverse/process_descriptions/ --example realset_diverse --direction m2m
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/realset_diverse/ground_truth/ --text-path ./data/realset_diverse/process_descriptions/ --example realset_diverse --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/realset_diverse/ground_truth/ --text-path ./data/realset_diverse/process_descriptions/ --example realset_diverse --direction m2m
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/realset_diverse/ground_truth/ --text-path ./data/realset_diverse/process_descriptions/ --example realset_diverse --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction m2m
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction m2m
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction t2t
exec bash
