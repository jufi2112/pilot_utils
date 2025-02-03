import os
import json
import random
from enum import Enum
from os import path as osp
from typing import Union, Set, Dict, List, Tuple
from pilot_utils.azf_trainer.src import AZFQuestionnaire, AZFQuestion

class QuestionMode(Enum):
    ALL = "ALL"
    NO_DONE = "NO_DONE"
    WATCHED_ONLY = "WATCHED"
    DONE_ONLY = "DONE"

class AZFTrainerModel:
    def __init__(self,
                 n_questions: int,
                 fpath_questionnaire: str,
                 fpath_done: str,
                 fpath_watched: str,
                 question_mode: QuestionMode = QuestionMode.NO_DONE
                 ):
        self.max_questions = n_questions
        self.questionnaire = AZFQuestionnaire.from_json(fpath_questionnaire)
        self.question_mode = question_mode
        self.fpath_done = fpath_done
        self.fpath_watched = fpath_watched
        self.indices_done: Set[int] = {}
        self.indices_watched: Set[int] = {}
        self.answer_history: Dict[int, Dict[str, Union[AZFQuestion, int, None]]] = {}
        if osp.exists(self.fpath_done):
            self.indices_done = json.load(self.fpath_done)
        if osp.exists(self.fpath_watched):
            self.indices_watched = json.load(self.fpath_watched)


    def get_next_question(self) -> Union[Dict[str, Union[AZFQuestion, int, None]], None]:
        """
            Returns
            -------
                A dict with keys 'question' that contains the question and 'user_selection' that contains
                an int representing the user selected answer, or None if no answer has yet been selected.
                If no more questions are available, returns None
        """
        question: AZFQuestion = self.questionnaire.get_next_question()
        if question is not None and question.id in self.answer_history.keys():
            # If already seen in this training, show this question no matter if it does not correspond to the
            # filter criteria anymore
            return self.answer_history[question.id]
        while (question is not None):
            if self.question_mode == QuestionMode.NO_DONE and question.id in self.indices_done:
                question = self.questionnaire.get_next_question()
            elif self.question_mode == QuestionMode.WATCHED_ONLY and question.id not in self.indices_watched:
                question = self.questionnaire.get_next_question()
            elif self.question_mode == QuestionMode.DONE_ONLY and question.id not in self.indices_done:
                question = self.questionnaire.get_next_question()
            else:
                # Valid question
                break
        if question is None:
            return None
        if question.id not in self.answer_history.keys():
            if len(self.answer_history) == self.max_questions:
                return None
            # Unseen question, shuffle answers and save configuration for later
            # Shuffle order of answers
            random.shuffle(question.answers)
            self.answer_history[question.id] = {
                'question': question,
                'user_selection': None,
                'done': question.id in self.indices_done,
                'watched': question.id in self.indices_watched
            }
        return self.answer_history[question.id]


    def get_previous_question(self) -> Union[Dict[str, Union[AZFQuestion, int, None]], None]:
        """
            Returns
            -------
                A dict with keys 'question' that contains the question and 'user_selection' that contains
                an int representing the user selected answer, or None if no answer has yet been selected.
                If no more questions are available, returns None
        """
        question: AZFQuestion = self.questionnaire.get_previous_question()
        if question is not None and question.id in self.answer_history.keys():
            return self.answer_history[question.id]
        while (question is not None):
            if self.question_mode == QuestionMode.NO_DONE and question.id in self.indices_done:
                question = self.questionnaire.get_previous_question()
            elif self.question_mode == QuestionMode.WATCHED_ONLY and question.id not in self.indices_watched:
                question = self.questionnaire.get_previous_question()
            elif self.question_mode == QuestionMode.DONE_ONLY and question.id not in self.indices_done:
                question = self.questionnaire.get_previous_question()
            else:
                break
        if question is None:
            return None
        if question.id not in self.answer_history.keys():
            random.shuffle(question.answers)
            self.answer_history[question.id] = {
                'question': question,
                'user_selection': None,
                'done': question.id in self.indices_done,
                'watched': question.id in self.indices_watched
            }
        return self.answer_history[question.id]


    def set_done(self, index: int, is_done: bool):
        if is_done:
            self.indices_done.add(index)
            if index in self.answer_history.keys():
                self.answer_history[index]['done'] = True
        else:
            self.indices_done.discard(index)
            if index in self.answer_history.keys():
                self.answer_history[index]['done'] = False
        fname_tmp = self.fpath_done + ".tmp"
        with open(fname_tmp, 'w') as file:
            json.dump(self.indices_done, file)
        os.replace(fname_tmp, self.fpath_done)


    def set_watched(self, index: int, is_watched: bool):
        if is_watched:
            self.indices_watched.add(index)
            if index in self.answer_history.keys():
                self.answer_history[index]['watched'] = True
        else:
            self.indices_watched.discard(index)
            if index in self.answer_history.keys():
                self.answer_history[index]['watched'] = False
        fname_tmp = self.fpath_watched + ".tmp"
        with open(fname_tmp, 'w') as file:
            json.dump(self.indices_watched, file)
        os.replace(fname_tmp, self.fpath_watched)


    def add_user_selection(self, index: int, selection: int) -> int:
        """
            Returns:
            --------
                int: The position of the correct answer
        """
        if index in self.answer_history.keys():
            self.answer_history[index]['user_selection'] = selection
            correct = [idx for idx, answer in enumerate(self.answer_history[index]['question'].answers) if answer.correct][0]
            return correct
        else:
            raise KeyError(f"Could not find question {index} in answer history!")
