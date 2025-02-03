import json
import numpy as np
from os import path as osp
from typing import List, Dict, Tuple, Union

class AZFAnswer:
    def __init__(self,
                 answer: str,
                 correct: bool):
        self.answer = answer
        self.correct = correct


    def get_json(self):
        return {'answer': self.answer, 'correct': self.correct}


    @staticmethod
    def from_json(json_dict) -> "AZFAnswer":
        try:
            answer = AZFAnswer(**json_dict)
        except:
            raise ValueError("Could not create a valid AZFAnswer from the provided json file")
        return answer



class AZFQuestion:
    def __init__(self,
                 id: int,
                 question: str,
                 answers: List[AZFAnswer]
                 ):
        if not isinstance(answers, list):
            raise TypeError(f"Expected parameter 'answers' to be of type list, but got {type(answers)}")
        if not len(answers) == 4:
            raise ValueError(f"Expected parameter 'answers' to have length 4, but got {len(answers)}")
        self.id = id
        self.question = question
        self.answers: List[AZFAnswer] = answers
        n_corrects = 0
        for answer in self.answers:
            if answer.correct:
                n_corrects += 1
        assert n_corrects == 1, f"Expected 1 correct answer but got {n_corrects}"


    def get_json(self) -> Dict:
        return {
            'id': self.id,
            'question': self.question,
            'answers': [answer.get_json() for answer in self.answers]
        }


    def get_answers(self) -> List[Tuple[str, bool]]:
        """
            Returns, in random order, answers and whether they are correct

            Returns
            -------
                A list of tuples (answer, correct)
        """
        indices = np.random.permutation(len(self.answers))
        return [(self.answers[idx].text, self.answers[idx].correct) for idx in indices]


    @staticmethod
    def from_json(json_dict: Dict) -> "AZFQuestion":
        try:
            id = json_dict['id']
            question = json_dict['question']
            answers = [AZFAnswer.from_json(answer) for answer in json_dict['answers']]
        except:
            raise ValueError("Could not create a valid AZFQuestion from the provided json file")
        azf_question = AZFQuestion(id, question, answers)
        return azf_question



class AZFQuestionnaire:
    def __init__(self,
                 random_order: bool,
                 questions: List[AZFQuestion] = None
                 ):
        if questions is None:
            self.questions = {}
        elif  not isinstance(questions, list):
            raise TypeError(f"Expected questions to be of type NoneType or list, but got {type(questions)}")
        else:
            self.questions = {
                question.id: question for question in questions
            }
        self.random_order = random_order
        self.indices = None
        self._setup_indices()
        self.current_index = 0


    def _setup_indices(self):
        if self.random_order:
            self.indices = np.random.permutation(len(self.questions))
        else:
            self.indices = np.arange(len(self.questions))


    def add_question(self, question: AZFQuestion):
        self.questions[question.id] = question
        self._setup_indices()
        self.current_index = 0


    def get_json(self):
        return [question.get_json() for _, question in self.questions.items()]


    def get_next_question(self) -> Union[None, AZFQuestion]:
        """
            Returns the next question. If no more question are available, returns None
        """
        if self.current_index >= len(self.questions):
            return None
        ids = list(self.questions.keys())
        question = self.questions[ids[self.indices[self.current_index]]]
        self.current_index += 1
        return question


    def get_previous_question(self) -> Union[None, AZFQuestion]:
        """
            Returns the previous question. If no more questions are available, returns None
        """
        if self.current_index <= -1:
            return None
        ids = list(self.questions.keys())
        question = self.questions[ids[self.indices[self.current_index]]]
        self.current_index -= 1
        return question


    def get_num_questions(self) -> int:
        return len(self.questions)


    def get_question_by_id(self, id: int) -> Union[AZFQuestion, None]:
        return self.questions.get(id, None)


    def reset_index(self):
        self.current_index = 0


    @staticmethod
    def from_json(json_fpath) -> "AZFQuestionnaire":
        if not osp.exists(json_fpath):
            raise ValueError(f"The provided json path does not exist: {json_fpath}")
        with open(json_fpath, 'r') as file:
            questions = json.load(file)
        questionnaire: AZFQuestionnaire = AZFQuestionnaire(True)
        for question in questions:
            questionnaire.add_question(AZFQuestion.from_json(question))
        return questionnaire
