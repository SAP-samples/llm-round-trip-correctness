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

from round_trip.t2m.prompt_engineering import json_desc
from round_trip.llm_connect.gen_ai_llm_call import generate_gpt_with_timeout
from round_trip.m2t.create_description import generate_prompt_gpt as generate_prompt_gpt_m2t
from round_trip.t2m.create_model import generate_prompt_gpt as generate_prompt_gpt_t2m

from round_trip.llm_connect.gen_ai_llm_call import generate_gemini_with_timeout
from round_trip.m2t.create_description import generate_prompt_gemini as generate_prompt_gemini_m2t
from round_trip.t2m.create_model import generate_prompt_gemini as generate_prompt_gemini_t2m

thold = 0.75
thold = 0.99
model1 = open('../round-trip/examples/round/model1.json', 'r').read()
model2 = open('../round-trip/examples/round/model2.json', 'r').read()

text1 = open('../round-trip/examples/round/text1.txt', 'r').read()
text2 = open('../round-trip/examples/round/text2.txt', 'r').read()



sim1 = text_similarity.sts_bert(text1, text2)
sim2 = text_similarity.text_similarity_alternative(text1,text2, threshold=thold)

sim3 = bpmn_similarity.calculate_similarity_scores(json.loads(model1), json.loads(model2), method="dice", similarity_threshold=thold)[0]["overall"]
sim4 = bpmn_similarity.calculate_similarity_alternative(json.loads(model1), json.loads(model2), method="dice", similarity_threshold=thold)["overall"]
#sim3 = bpmn_similarity.calculate_similarity_scores(json.loads(model1), json.loads(model2), method="dice", similarity_threshold=0.99)[0]["overall"]
#sim4 = bpmn_similarity.calculate_similarity_alternative(json.loads(model1), json.loads(model2), method="dice", similarity_threshold=0.99 )["overall"]

print(sim1,sim2)
print(sim3,sim4)

