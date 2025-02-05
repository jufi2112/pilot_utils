import os
import json
import random
from enum import Enum
from os import path as osp
from typing import Union, Set, Dict, List, Tuple
from pilot_utils.azf_trainer.src import AZFQuestionnaire, AZFQuestion

class QuestionFilter(Enum):
    ALL = "ALL"
    NOT_IGNORED = "NOT_IGNORED"
    IGNORED_ONLY = "IGNORED_ONLY"
    WATCHED_ONLY = "WATCHED_ONLY"


class AZFTrainerModel:
    def __init__(self,
                 n_questions: int,
                 fpath_questionnaire: str,
                 fpath_ignored: str,
                 fpath_watched: str,
                 question_mode: QuestionFilter = QuestionFilter.NOT_IGNORED
                 ):
        self.questionnaire = AZFQuestionnaire.from_json(fpath_questionnaire)
        self.max_questions = n_questions if n_questions > 0 else self.questionnaire.get_num_questions()
        self.max_questions = min(self.max_questions, self.questionnaire.get_num_questions())
        self.question_mode = question_mode
        self.fpath_ignored = fpath_ignored
        self.fpath_watched = fpath_watched
        self.questions_answered: Set[int] = set()
        self.indices_ignored: Set[int] = set(self._load_special_indices_from_file(self.fpath_ignored))
        self.indices_watched: Set[int] = set(self._load_special_indices_from_file(self.fpath_watched))

        # Contains the ids of all questions that should be shown
        self.question_ids: List[int] = self._filter_questionnaire()
        self.max_questions = len(self.question_ids)
        self.current_question_index = None

        # Contains all already shown questions and their user selection
        self.answer_history: Dict[int, Dict[str, Union[AZFQuestion, int, None]]] = {}


    def _load_special_indices_from_file(self, fpath: str) -> List[int]:
        if not osp.exists(fpath):
            return []
        with open(fpath, 'r') as file:
            indices = list(json.load(file))
        return indices


    def _filter_questionnaire(self) -> List[int]:
        """
            The returned list will contain the indices of the questions that should be shown in the
            current training.
        """
        filtered_qids = []
        for qid, _ in self.questionnaire:
            if self.question_mode == QuestionFilter.IGNORED_ONLY and qid not in self.indices_ignored:
                continue
            if self.question_mode == QuestionFilter.WATCHED_ONLY and qid not in self.indices_watched:
                continue
            if self.question_mode == QuestionFilter.NOT_IGNORED and qid in self.indices_ignored:
                continue
            filtered_qids.append(qid)
        filtered_qids = list(set(filtered_qids))
        random.shuffle(filtered_qids)
        return filtered_qids[:self.max_questions]


    def get_next_question(self) -> Union[Dict[str, Union[AZFQuestion, int, None]], None]:
        """
            Returns
            -------
                dict:
                    A dict with keys 'question' that contains the question and 'user_selection' that contains
                    an int representing the user selected answer, or None if no answer has yet been selected.
                    If no more questions are available, returns None
                int:
                    Number of the current question
                int:
                    Total number of questions
        """
        if self.max_questions == 0:
            return None, None, 0
        if self.current_question_index is None:
            self.current_question_index = 0
        else:
            self.current_question_index += 1
        if self.current_question_index >= self.max_questions:
            self.current_question_index = self.max_questions - 1
            return None, None, self.max_questions
        question: AZFQuestion = self.questionnaire.get_question_by_id(self.question_ids[self.current_question_index])
        if question is None:
            raise ValueError(f"The questionnaire does not contain a question with id {self.question_ids[self.current_question_index]}")

        if question.id not in self.answer_history.keys():
            # Unseen question, shuffle answers and save configuration
            random.shuffle(question.answers)
            self.answer_history[question.id] = {
                'question': question,
                'user_selection': None,
                'ignored': question.id in self.indices_ignored,
                'watched': question.id in self.indices_watched
            }
        return self.answer_history[question.id], self.current_question_index + 1, self.max_questions


    def get_previous_question(self) -> Union[Dict[str, Union[AZFQuestion, int, None]], None]:
        """
            Returns
            -------
                Dict:
                    A dict with keys 'question' that contains the question and 'user_selection' that contains
                    an int representing the user selected answer, or None if no answer has yet been selected.
                    If no more questions are available, returns None
                int:
                    Number of the current question
                int:
                    Total number of questions
        """
        if self.max_questions == 0:
            return None, None, 0
        if self.current_question_index is None:
            self.current_question_index = 0
        else:
            self.current_question_index -= 1
        if self.current_question_index < 0:
            self.current_question_index = 0
            return None, None, self.max_questions
        question: AZFQuestion = self.questionnaire.get_question_by_id(self.question_ids[self.current_question_index])
        if question is None:
            raise ValueError(f"The questionnaire does not contain a question with id {self.question_ids[self.current_question_index]}")

        if question.id not in self.answer_history.keys():
            random.shuffle(question.answers)
            self.answer_history[question.id] = {
                'question': question,
                'user_selection': None,
                'ignored': question.id in self.indices_ignored,
                'watched': question.id in self.indices_watched
            }
        return self.answer_history[question.id], self.current_question_index + 1, self.max_questions


    def set_ignored(self, question_id: int, ignore: bool):
        if ignore:
            self.indices_ignored.add(question_id)
            if question_id in self.answer_history.keys():
                self.answer_history[question_id]['ignored'] = True
        else:
            self.indices_ignored.discard(question_id)
            if question_id in self.answer_history.keys():
                self.answer_history[question_id]['ignored'] = False
        fname_tmp = self.fpath_ignored + ".tmp"
        with open(fname_tmp, 'w') as file:
            json.dump(list(self.indices_ignored), file)
        os.replace(fname_tmp, self.fpath_ignored)


    def add_to_watchlist(self, question_id: int, watch: bool):
        if watch:
            self.indices_watched.add(question_id)
            if question_id in self.answer_history.keys():
                self.answer_history[question_id]['watched'] = True
        else:
            self.indices_watched.discard(question_id)
            if question_id in self.answer_history.keys():
                self.answer_history[question_id]['watched'] = False
        fname_tmp = self.fpath_watched + ".tmp"
        with open(fname_tmp, 'w') as file:
            json.dump(list(self.indices_watched), file)
        os.replace(fname_tmp, self.fpath_watched)


    def add_user_selection(self, question_id: int, selection: int) -> int:
        """
            Returns:
            --------
                int: The position of the correct answer
        """
        self.questions_answered.add(question_id)
        if question_id in self.answer_history.keys():
            self.answer_history[question_id]['user_selection'] = selection
            correct = [idx for idx, answer in enumerate(self.answer_history[question_id]['question'].answers) if answer.correct][0]
            return correct
        else:
            raise KeyError(f"Could not find question {question_id} in answer history!")


    def all_questions_answered(self) -> bool:
        return len(self.questions_answered) == self.max_questions


    def get_exam_stats(self) -> Tuple[int, int, int]:
        """
            Returns exam statistics

            Returns
            -------
                int: Total number of questions
                int: Number of correctly answered questions
                int: Number of unanswered questions
        """
        n_correct = 0
        n_wrong = 0
        for _, data in self.answer_history.items():
            if data['user_selection'] is None:
                continue
            question = data['question']
            correct = [idx for idx, answer in enumerate(question.answers) if answer.correct][0]
            if data['user_selection'] == correct:
                n_correct += 1
            else:
                n_wrong += 1
        return self.max_questions, n_correct, self.max_questions - n_correct - n_wrong


    def add_wrong_answers_to_watchlist(self):
        """
            Adds all wrong answers to the watchlist
        """
        for qid, data in self.answer_history.items():
            if data['user_selection'] is None:
                continue
            question = data['question']
            correct = [idx for idx, answer in enumerate(question.answers) if answer.correct][0]
            if data['user_selection'] != correct:
                self.add_to_watchlist(qid, True)


    def add_unanswered_to_watchlist(self):
        """
            Adds all unanswered questions to the watchlist
        """
        seen_qids = []
        for qid, data in self.answer_history.items():
            seen_qids.append(qid)
            if data['user_selection'] is None:
                self.add_to_watchlist(qid, True)
        # Check which questions have not yet been visited at all (-> not in answer_history)
        for qid in self.question_ids:
            if qid not in seen_qids:
                self.add_to_watchlist(qid, True)
