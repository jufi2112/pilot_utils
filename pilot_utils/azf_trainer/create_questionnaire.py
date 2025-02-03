import os
import json
import argparse

from os import path as osp
from pilot_utils.azf_trainer.src import parse_azf_questionnaire, AZFQuestionnaire

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parses the AZF questionnaire from a provided PDF document.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the PDF document that contains the AZF questionnaire")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output path to where the questionnaire should be saved to as json file")
    args = parser.parse_args()

    if not osp.isfile(args.input):
        raise ValueError(f"The provided pdf file does not exist: {args.input}")
    input_file = args.input
    output_file = args.output
    if osp.splitext(output_file)[1] != '.json':
        output_file += '.json'
    questionnaire: AZFQuestionnaire = parse_azf_questionnaire(input_file)
    with open(output_file, 'w') as file:
        json.dump(questionnaire.get_json(), file, indent=4)
    print("Finished")
