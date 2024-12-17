import os, sys
import json
import logging
import argparse
import csv

sys.path.append("./data/")
sys.path.append("./model_evaluation")
sys.path.append("./round_trip")

import bpmn_similarity
from text_evaluation import text_similarity

from round_trip.m2t.prompt_engineering import bpmn_desc
from round_trip.t2m.prompt_engineering import json_desc, json_format

from round_trip.llm_connect.gen_ai_llm_call import generate_gpt_with_timeout
from round_trip.m2t.create_description import generate_prompt_gpt as generate_prompt_gpt_m2t
from round_trip.t2m.create_model import generate_prompt_gpt as generate_prompt_gpt_t2m

from round_trip.llm_connect.gen_ai_llm_call import generate_gemini_with_timeout
from round_trip.m2t.create_description import generate_prompt_gemini as generate_prompt_gemini_m2t
from round_trip.t2m.create_model import generate_prompt_gemini as generate_prompt_gemini_t2m

def generate_artefacts_with_gemini(direction, model, description):
    if direction == 'm2m':
        gen_text = generate_gemini_with_timeout(
            system_prompt_gemini_m2t,
            examples_m2t,
            "Here is the model: " + str(model),
            temp_in,
            response_format=False
        )
        if gen_text is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {model_file}')
            continue

        gen_model = generate_gemini_with_timeout(
            system_prompt_gemini_t2m,
            examples_t2m,
            "Here is the textual description: " + gen_text,
            temp_out,
            response_format=True
        )
        if gen_model is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {model_file}')
            continue
    elif direction == 't2t':
        gen_model = generate_gemini_with_timeout(
            system_prompt_gemini_t2m,
            examples_t2m,
            "Here is the texual description: " + str(description),
            temp_in,
            response_format=True
        )

        if gen_model:
            print(json.loads(gen_model)['pools'])
        if gen_model is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {model_file}')
            continue

        gen_text = generate_gemini_with_timeout(
            system_prompt_gemini_m2t,
            examples_m2t,
            "Here is the model: " + str(gen_model),
            temp_out,
            response_format=False
        )
        if gen_text is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {model_file}')
            continue
    return gen_text, gen_model

def generate_artefacts_with_gpt(direction, model, description):
    if direction == 'm2m':
        gen_text = generate_gpt_with_timeout(
            system_prompt_m2t,
            user_prompt_m2t,
            assistant_prompt_m2t,
            "Here is the model: " + str(model),
            temp_in,
            response_format=False
        )
        if gen_text is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {file}')
            continue

        gen_model = generate_gpt_with_timeout(
            system_prompt_t2m,
            user_prompt_t2m,
            assistant_prompt_t2m,
            "Here is the textual description: " + gen_text,
            temp_out,
            response_format=True
        )
        if gen_model is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {file}')
            continue

    elif direction == 't2t':
        gen_model = generate_gpt_with_timeout(
            system_prompt_t2m,
            user_prompt_t2m,
            assistant_prompt_t2m,
            "Here is the texual description: " + str(description),
            temp_in,
            response_format=True
        )
        if gen_model is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {file}')
            continue
        gen_text = generate_gpt_with_timeout(
            system_prompt_m2t,
            user_prompt_m2t,
            assistant_prompt_m2t,
            "Here is the model: " + str(gen_model),
            temp_out,
            response_format=False
        )
        if gen_text is None:
            logger.info(f'Skipping iteration {j + 1} due to timeout for file: {file}')
            continue
    return gen_text, gen_model


def main_pipelin(llm, direction, model_path, text_path, example):
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger("GPTLogger")
    if example == 'pet':
        path_to_json = "./data/prompt_ex_json_pet.json"
        path_to_text = "./data/prompt_ex_text_pet.txt"
    else:
        path_to_json = "./data/prompt_ex_json_real_set.json"
        path_to_text = "./data/prompt_ex_text_real_set.txt"

    system_prompt_m2t, user_prompt_m2t, assistant_prompt_m2t = generate_prompt_gpt_m2t(path_to_json, path_to_text, bpmn_desc)
    system_prompt_t2m, user_prompt_t2m, assistant_prompt_t2m = generate_prompt_gpt_t2m(path_to_json, path_to_text, json_desc)

    t2t_eval_1 = {}
    t2t_eval_2 = {}
    m2m_eval_1 = {}
    m2m_eval_2 = {}
    artefacts = {}
    temp_in = 1
    temp_out = 0.1
    iterations = 3

    if direction == 'm2m':
         files_to_iterate = os.listdir(model_path)
    elif direction == 't2t':
         files_to_iterate = os.listdir(text_path)

    logger.info('Starting the processing of models and texts')

    for i, file in enumerate(files_to_iterate):  # Use enumerate for progress tracking
        logger.info(f'Processing file: {file}')
        print('--------------------------{}/{}-----------------------------------'.format(i,len(files_to_iterate)))
        try:
            if model_path != 'no':
                with open(os.path.join(model_path, file), "r") as infile:
                    model = json.load(infile)
            else:
                model = ''

            if text_path != 'no':
                with open(os.path.join(text_path, file.replace(".json", ".txt")), "r") as file:
                    description = file.read()
            else:
                description = ''

            text_eval_1 = []
            text_eval_2 = []
            model_eval_1 = []
            model_eval_2 = []
            artefacts[file] = {}

            for j in range(iterations):
                logger.info(f'Iteration {j + 1} for file: {file}')
                if llm == 'gpt':
                    gen_text, gen_model = generate_artefacts_with_gpt(direction, model, description)
                elif llm == 'gemini':
                    gen_text, gen_model = generate_artefacts_with_gemini(direction, model, description)

                artefacts[file][j] = {'text':gen_text,'model':json.loads(gen_model)}

                try:
                    if description:
                        text_eval_1.append(text_similarity.sts_bert(description, gen_text))
                        text_eval_2.append(text_similarity.text_similarity_alternative(description, gen_text, threshold=0.75))

                    if model:
                        model_eval_1.append(
                            bpmn_similarity.calculate_similarity_scores(
                                model, json.loads(gen_model), method="dice", similarity_threshold=0.75
                            )[0]["overall"]
                        )
                        model_eval_2.append(
                            bpmn_similarity.calculate_similarity_alternative(
                                model, json.loads(gen_model), method="dice", similarity_threshold=0.75
                            )["overall"]
                        )

                except Exception as e:
                    logger.error(f"Error during calculations in iteration {j + 1} for file {file}: {e}")
                    continue

            if description:
                if text_eval_1:
                    t2t_eval_1[file] = sum(text_eval_1) / len(text_eval_1)
                if text_eval_2:
                    t2t_eval_2[file] = sum(text_eval_2) / len(text_eval_2)

            if model:
                if model_eval_1:
                    m2m_eval_1[model_file] = sum(model_eval_1) / len(model_eval_1)
                if model_eval_2:
                    m2m_eval_2[model_file] = sum(model_eval_2) / len(model_eval_2)

        except Exception as e:
            logger.error(f"An error occurred while processing file {file}: {e}")


    logger.info('Completed processing all models and texts')

    # Write results to CSV
    with open('./results/gpt_'+ example + '_' + direction + '.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['model_name', 't2t_eval_1','t2t_eval_2', 'm2m_eval_1', 'm2m_eval_2'])  # Header

        for model_name in files_to_iterate:
            csv_writer.writerow([
                model_name,
                t2t_eval_1.get(model_name, 'N/A'),
                t2t_eval_2.get(model_name, 'N/A'),
                m2m_eval_1.get(model_name, 'N/A'),
                m2m_eval_2.get(model_name, 'N/A')
            ])

    with open('./generated_artefacts/report_gpt_'+ example + '_' + direction + '.json', 'w') as outfile:
        json.dump(artefacts, outfile, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process models and text with retries and timeout.")
    parser.add_argument('--llm', type=str, required=True, help='Select llm mode: gpt or gemini')
    parser.add_argument('--model-path', type=str, required=True, help='Path to the models directory')
    parser.add_argument('--text-path', type=str, required=True, help='Path to the text descriptions directory')
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
