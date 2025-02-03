import json
from enum import Enum
from typing import Union, Set
from pilot_utils.azf_trainer.src import AZFQuestionnaire, AZFQuestion

class QuestionMode(Enum):
    ALL = "ALL"
    NO_DONE = "NO_DONE"
    WATCHED_ONLY = "WATCHED"
    DONE_ONLY = "DONE"

class AZFTrainerModel:
    def __init__(self,
                 fpath_questionnaire: str,
                 fpath_done: str = None,
                 fpath_watched: str = None,
                 question_mode: QuestionMode = QuestionMode.NO_DONE
                 ):
        self.questionnaire = AZFQuestionnaire.from_json(fpath_questionnaire)
        self.question_mode = question_mode
        self.fpath_done = fpath_done
        self.fpath_watched = fpath_watched
        if self.fpath_done is None:
            if self.question_mode == QuestionMode.DONE_ONLY:
                raise ValueError("Questionnaire should provide done-only questions but no corresponding file path was given")
            self.indices_done: Set[int] = {}
        else:
            self.indices_done = json.load(self.fpath_done)
        if self.fpath_watched is None:
            if self.question_mode == QuestionMode.WATCHED_ONLY:
                raise ValueError("Questionnaire should provide watched-only questions but no cooresponding file path was given!")
            self.indices_watched: Set[int] = {}
        else:
            self.indices_watched = json.load(self.fpath_watched)


    def get_next_question(self) -> Union[AZFQuestion, None]:
        question: AZFQuestion = self.questionnaire.get_next_question()
        if question is None:
            return None
        if self.question_mode == QuestionMode.ALL:
            return question
        if self.question_mode == QuestionMode.NO_DONE:
            if question.id in self.indices_done:
                return self.get_next_question()
            return question
        if self.question_mode == QuestionMode.WATCHED_ONLY:
            if question.id in self.indices_watched:
                return question
            else:
                return self.get_next_question()
        if self.question_mode == QuestionMode.DONE_ONLY:
            if question.id in self.indices_done:
                return question
            else:
                return self.get_next_question()


    def get_previous_question(self) -> Union[AZFQuestion, None]:
        question: AZFQuestion = self.questionnaire.get_previous_question()
        if question is None:
            return None
        if self.question_mode == QuestionMode.ALL:
            return question
        if self.question_mode == QuestionMode.NO_DONE:
            if question.id in self.indices_done:
                return self.get_previous_question()
            return question
        if self.question_mode == QuestionMode.WATCHED_ONLY:
            if question.id in self.indices_watched:
                return question
            else:
                return self.get_previous_question()
        if self.question_mode == QuestionMode.DONE_ONLY:
            if question.id in self.indices_done:
                return question
            else:
                return self.get_previous_question()


    def mark_as_done(self, index: int):
        if index in self.indices_done:
            return
        self.indices_done.append(index)