#!/bin/bash
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/domain/ground_truth/ --text-path ./data/domain/process_descriptions/ --example domain --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/pet/ground_truth/ --text-path ./data/pet/process_descriptions/ --example pet --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/sapsam/ground_truth/ --text-path ./data/sapsam/process_descriptions/ --example sapsam --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/domain/ground_truth/ --text-path ./data/domain/process_descriptions/ --example domain --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/pet/ground_truth/ --text-path ./data/pet/process_descriptions/ --example pet --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/realset/ground_truth/ --text-path ./data/realset/process_descriptions/ --example realset --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/sapsam/ground_truth/ --text-path ./data/sapsam/process_descriptions/ --example sapsam --direction t2t
screen poetry run python universal_pipeline.py --llm gpt --model-path ./data/mad/ground_truth/ --text-path ./data/mad/process_descriptions/ --example mad --direction t2t
screen poetry run python universal_pipeline.py --llm gemini --model-path ./data/mad/ground_truth/ --text-path ./data/mad/process_descriptions/ --example mad --direction t2t
exec bash
