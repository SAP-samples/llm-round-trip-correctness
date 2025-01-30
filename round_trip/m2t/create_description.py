# from llm_connect.ask_models import ask_gpt
import json

def generate_prompt_gemini(path_to_json, path_to_text):


    with open(path_to_json, "r") as input_file:
        input_json = json.load(input_file)

    with open(path_to_text, "r") as output_file:
        output_description = output_file.read().strip()


    system_prompt = (
        """
        You are a BPMN2.0 expert who can convert textual information to a BPMN model in JSON and vice versa.
        Given an input BPMN model in JSON format with the usual elements (tasks, events, gateways, pools containing lanes, sequence flows, and possibly message flows)
        describe the process from beginning to end accurately in the order that it happens.
        The text should read fluently in the appropriate language. Do not refer to the actual element types but stay true to the model.
        Use sequence flows to determine the order of process elements and, if there are any message flows, describe the communications that have taken place.
        A paragraph of text suffices. The text should be so detailed and accurate so that the original process model can be reconstructed from it.
        Here is an example. Follow the logic of the example when generating text.
        """)

    examples = [f"input: {input_json}, output: {output_description}"]

    return system_prompt, examples

def generate_prompt_gpt(path_to_json, path_to_text):


    with open(path_to_json, "r") as input_file:
        input_json = json.load(input_file)

    with open(path_to_text, "r") as output_file:
        output_description = output_file.read().strip()


    system_prompt = (
        """
        You are a BPMN2.0 expert who can convert textual information to a BPMN model in JSON and vice versa.
        Given an input BPMN model in JSON format with the usual elements (tasks, events, gateways, pools containing lanes, sequence flows, and possibly message flows)
        describe the process from beginning to end accurately in the order that it happens.
        The text should read fluently in the appropriate language. Do not refer to the actual element types but stay true to the model.
        Use sequence flows to determine the order of process elements and, if there are any message flows, describe the communications that have taken place.
        A paragraph of text suffices. The text should be so detailed and accurate so that the original process model can be reconstructed from it.
        Here is an example. Follow the logic of the example when generating text.
        """)


    user_prompt, assistant_prompt = f"{input_json}", f"{output_description}"

    return system_prompt, user_prompt, assistant_prompt


