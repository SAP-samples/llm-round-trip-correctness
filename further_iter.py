import os, sys
import json
import logging
import argparse
import csv


def main_pipeline(llm, direction, model_path, text_path, example):
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger("{}Logger".format(llm.upper()))
    if example == 'pet':
        path_to_json = "./data/prompt_ex_json_pet.json"
        path_to_text = "./data/prompt_ex_text_pet.txt"
    elif example == 'real_set':
        path_to_json = "./data/prompt_ex_json_real_set.json"
        path_to_text = "./data/prompt_ex_text_real_set.txt"
    else:
        path_to_json = "./data/prompt_ex_json_sapsam.json"
        path_to_text = "./data/prompt_ex_text_sapsam.txt"

    t2t_eval_1 = {}
    t2t_eval_2 = {}
    m2m_eval_1 = {}
    m2m_eval_2 = {}
    artefacts = {}
    temp_in = 1
    temp_out = 0
    iterations = 3


    reportname = './iter_results/report_{}_{}_{}.json'.format(llm,example,direction)
    with open(reportname) as f:
        irep = json.load(f)
    final = {}
    metrics = ['ms1','ms2','ts1','ts2']
    for m in metrics:
        for l in range(0,iterations)
            temp = []
            for fi in irep:
                temp.append(iterations[fi][m][l])


    reportname = './iter_results/report_{}_{}_{}.json'.format(llm,example,direction)
    with open(reportname, 'w') as outfile:
        json.dump(results, outfile, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process models and text with retries and timeout.")
    parser.add_argument('--llm', type=str, required=True, help='Select llm mode: gpt or gemini')
    parser.add_argument('--model-path', type=str, required=False, default='no', help='Path to the models directory')
    parser.add_argument('--text-path', type=str, required=False, default='no', help='Path to the text descriptions directory')
    parser.add_argument('--example', type=str, required=True, help='pet or real_set')
    parser.add_argument('--direction', type=str, required=True, help='m2m or t2t')

    args = parser.parse_args()
    llm = args.llm.lower()
    direction = args.direction.lower()
    model_path = args.model_path
    text_path = args.text_path
    example = args.example.lower()
    if llm == 'gpt' or llm == 'gemini':
        if direction == 'm2m' and os.path.isdir(model_path):
            if not os.path.isdir(text_path):
                text_path = 'no'
            main_pipeline(llm, direction, model_path, text_path, example)
        elif direction == 't2t' and os.path.isdir(text_path):
            if not os.path.isdir(model_path):
                model_path = 'no'
            main_pipeline(llm, direction, model_path, text_path, example)
        else:
            print('Please check the direction of the pipeline (only m2m or t2t are acceptable) or check provided directories!!!')
    else:
        print('Please check selected llm model (only gpt or gemini are acceptable)!!!')
