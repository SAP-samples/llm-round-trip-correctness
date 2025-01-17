import os, sys
import time
import json
import logging
import argparse
import csv

sys.path.append("./data/")
sys.path.append("./model_evaluation")
sys.path.append("./round_trip")

import bpmn_similarity
from text_evaluation import text_similarity

from round_trip.t2m.prompt_engineering import json_desc
from round_trip.llm_connect.gen_ai_llm_call import generate_gpt_with_timeout
from round_trip.m2t.create_description import generate_prompt_gpt as generate_prompt_gpt_m2t
from round_trip.t2m.create_model import generate_prompt_gpt as generate_prompt_gpt_t2m

from round_trip.llm_connect.gen_ai_llm_call import generate_gemini_with_timeout
from round_trip.m2t.create_description import generate_prompt_gemini as generate_prompt_gemini_m2t
from round_trip.t2m.create_model import generate_prompt_gemini as generate_prompt_gemini_t2m


class Prompt:
    def __init__(self, llm, path_to_json, path_to_text, json_desc,temp_in,temp_out):
        self.temp_in = temp_in
        self.temp_out = temp_out
        if llm == 'gemini':
            self.system_prompt_gemini_t2m, self.examples_t2m = generate_prompt_gemini_t2m(path_to_json, path_to_text, json_desc)
            self.system_prompt_gemini_m2t, self.examples_m2t = generate_prompt_gemini_m2t(path_to_json, path_to_text)
        elif llm == 'gpt':
            self.system_prompt_t2m, self.user_prompt_t2m, self.assistant_prompt_t2m = generate_prompt_gpt_t2m(path_to_json, path_to_text, json_desc)
            self.system_prompt_m2t, self.user_prompt_m2t, self.assistant_prompt_m2t = generate_prompt_gpt_m2t(path_to_json, path_to_text)

def generate_artefacts_with_gemini(prompt, direction, model, description):
    gen_text = ''
    gen_model = ''
    if direction == 'm2m':
        gen_text = generate_gemini_with_timeout(
            prompt.system_prompt_gemini_m2t,
            prompt.examples_m2t,
            "Here is the model: " + str(model),
            prompt.temp_in,
            response_format=False
        )

        if gen_text:
            gen_model = generate_gemini_with_timeout(
                prompt.system_prompt_gemini_t2m,
                prompt.examples_t2m,
                "Here is the textual description: " + gen_text,
                prompt.temp_out,
                response_format=True
            )
    elif direction == 't2t':
        gen_model = generate_gemini_with_timeout(
            prompt.system_prompt_gemini_t2m,
            prompt.examples_t2m,
            "Here is the texual description: " + str(description),
            prompt.temp_in,
            response_format=True
        )

        if gen_model:
            gen_text = generate_gemini_with_timeout(
                prompt.system_prompt_gemini_m2t,
                prompt.examples_m2t,
                "Here is the model: " + str(gen_model),
                prompt.temp_out,
                response_format=False
            )
    return gen_text, gen_model

def generate_artefacts_with_gpt(prompt, direction, model, description):
    gen_text = ''
    gen_model = ''
    if direction == 'm2m':
        gen_text = generate_gpt_with_timeout(
            prompt.system_prompt_m2t,
            prompt.user_prompt_m2t,
            prompt.assistant_prompt_m2t,
            "Here is the model: " + str(model),
            prompt.temp_in,
            response_format=False
        )
        if gen_text:
            gen_model = generate_gpt_with_timeout(
                prompt.system_prompt_t2m,
                prompt.user_prompt_t2m,
                prompt.assistant_prompt_t2m,
                "Here is the textual description: " + gen_text,
                prompt.temp_out,
                response_format=True
            )
    elif direction == 't2t':
        gen_model = generate_gpt_with_timeout(
            prompt.system_prompt_t2m,
            prompt.user_prompt_t2m,
            prompt.assistant_prompt_t2m,
            "Here is the texual description: " + str(description),
            prompt.temp_in,
            response_format=True
        )
        if gen_model:
            gen_text = generate_gpt_with_timeout(
                prompt.system_prompt_m2t,
                prompt.user_prompt_m2t,
                prompt.assistant_prompt_m2t,
                "Here is the model: " + str(gen_model),
                prompt.temp_out,
                response_format=False
            )
    return gen_text, gen_model

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

    if direction == 'm2m':
         files_to_iterate = os.listdir(model_path)
    elif direction == 't2t':
         files_to_iterate = os.listdir(text_path)

    logger.info('Starting the processing of models and texts')

    reportname = './generated_artefacts/report_{}_{}_{}.json'.format(llm,example,direction)
    with open(reportname) as f:
        generated_artefacts = json.load(f)

    results = {}
    for i, file in enumerate(files_to_iterate):  # Use enumerate for progress tracking
        logger.info(f'Processing file: {file}')
        print('--------------------------{}/{}-----------------------------------'.format(i,len(files_to_iterate)))
        try:
            if model_path != 'no':
                split_file = '{}.json'.format(file.split('.')[0])
                with open(os.path.join(model_path, split_file), "r") as infile:
                    model = json.load(infile)
            else:
                model = ''

            if text_path != 'no':
                split_file = '{}.txt'.format(file.split('.')[0])
                with open(os.path.join(text_path, split_file), "r") as infile:
                    description = infile.read()
            else:
                description = ''

            results[file] = {}

            for j in range(iterations):
                logger.info(f'Iteration {j + 1} for file: {file}')
                gen_text = generated_artefacts[file][str(j)]['text']
                gen_model = generated_artefacts[file][str(j)]['model']

                if not gen_text:
                    continue
                if not gen_model:
                    continue

                try:
                    if description:
                        start = time.time()
                        text_eval_1 = text_similarity.sts_bert(description, gen_text)
                        end  = time.time() - start
                        logger.info(f'test1 {end}')

                        start = time.time()
                        text_eval_2 = text_similarity.text_similarity_alternative(description, gen_text, threshold=0.75)
                        end  = time.time() - start
                        logger.info(f'test2 {end}')
                    else:
                        text_eval_1, text_eval_2 = 'N\A'
                    if model:
                        start = time.time()
                        model_eval_1 = bpmn_similarity.calculate_similarity_scores( model, gen_model, method="dice", similarity_threshold=0.75)[0]["overall"]
                        end  = time.time() - start
                        logger.info(f'test3 {end}')

                        start = time.time()
                        model_eval_2 = bpmn_similarity.calculate_similarity_alternative( model, gen_model, method="dice", similarity_threshold=0.75)["overall"]
                        end  = time.time() - start
                        logger.info(f'test4 {end}')
                    else:
                        model_eval_1, model_eval_2 = 'N\A'

                    results[file][j] = [text_eval_1,text_eval_2,model_eval_1,model_eval_2]

                except Exception as e:
                    logger.error(f"Error during calculations in iteration {j + 1} for file {file}: {e}")
                    continue

        except Exception as e:
            logger.error(f"An error occurred while processing file {file}: {e}")


    logger.info('Completed processing all models and texts')

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
