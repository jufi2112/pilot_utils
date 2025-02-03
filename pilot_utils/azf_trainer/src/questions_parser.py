import re
import pdfplumber
import pymupdf

from typing import Union
from pilot_utils.azf_trainer.src import AZFAnswer, AZFQuestion, AZFQuestionnaire


def parse_azf_questionnaire(pdf_path: str) -> AZFQuestionnaire:
    """
        Parses the provided pdf document and returns the contained questionnaire
    """
    header_text = 'Prüfungsfragen im Prüfungsteil "Kenntnisse" bei Prüfungen zum Erwerb AZF und AZF E'
    questionnaire = AZFQuestionnaire(True)

    question_id = None
    question_text = None
    answers = []

    doc = pymupdf.open(pdf_path)
    for page in doc:
        blocks = page.get_text('blocks')
        header = blocks[0][4].strip()
        if header != header_text:
            print(f"Skipping page based on header.")
            continue
        for block in blocks:
            block_text = block[4].strip()
            text = block_text.split('\n', 1)
            # Ignore header / footer
            if not text[0].strip().isdigit() and text[0].strip() not in ['A', 'B', 'C', 'D']:
                continue

            id = text[0].strip()
            text = text[1].strip().replace("\n", "")

            if question_id is None:
                question_id = int(id)
                question_text = text
                continue
            else:
                answer = AZFAnswer(text, id == 'A')
                answers.append(answer)

                if len(answers) == 4:
                    question = AZFQuestion(question_id, question_text, answers)
                    questionnaire.add_question(question)
                    question_id = None
                    question_text = None
                    answers = []
    return questionnaire
