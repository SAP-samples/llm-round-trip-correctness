#!/bin/bash
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/domain/ground_truth/ --text-path ./data/domain/process_descriptions/ --example domain --direction t2t
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/pet/ground_truth/ --text-path ./data/pet/process_descriptions/ --example pet --direction t2t
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction t2t
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/domain/ground_truth/ --text-path ./data/domain/process_descriptions/ --example domain --direction m2m
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/pet/ground_truth/ --text-path ./data/pet/process_descriptions/ --example pet --direction  m2m
screen poetry run python iteration_eval.py --llm gemini --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction  m2m
screen poetry run python iteration_eval.py --llm gpt --model-path ./data/domain/ground_truth/ --text-path ./data/domain/process_descriptions/ --example domain --direction  m2m
screen poetry run python iteration_eval.py --llm gpt --model-path ./data/pet/ground_truth/ --text-path ./data/pet/process_descriptions/ --example pet --direction  m2m
screen poetry run python iteration_eval.py --llm gpt --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction  m2m
exec bash
