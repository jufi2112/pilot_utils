import os
import sys
import json
import argparse
import importlib.util
from os import path as osp
from pilot_utils.azf_trainer.src import AZFTrainingController
from pilot_utils.azf_trainer.ui import AZFTrainerMainWindow

from PyQt6.QtWidgets import QApplication

def get_package_root():
    spec = importlib.util.find_spec('pilot_utils')
    if spec is None or spec.origin is None:
        return None
    return osp.dirname(osp.dirname(spec.origin))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AZF Theory Trainer")
    parser.add_argument('-q', '--questions', type=str, required=False, default=None, help="Non-standard path to the questions.json file")
    parser.add_argument('-w', '--watched', type=str, required=False, default=None, help="Non-standard path to the watched.json file")
    parser.add_argument('-d', '--done', type=str, required=False, default=None, help="Non-standard path to the done.json file")
    args = parser.parse_args()
    if args.questions is None:
        questions_fpath = osp.join(get_package_root(), 'pilot_utils', 'azf_trainer', 'data', 'questionnaire.json')
    else:
        questions_fpath = args.questions
    if args.watched is None:
        watched_fpath = osp.join(get_package_root(), 'pilot_utils', 'azf_trainer', 'data', 'watched.json')
    else:
        watched_fpath = args.watched
    if args.done is None:
        done_fpath = osp.join(get_package_root(), 'pilot_utils', 'azf_trainer', 'data', 'done.json')
    else:
        done_fpath = args.done
    

    app = QApplication([])
    window = AZFTrainerMainWindow()
    window.show()
    controller: AZFTrainingController = AZFTrainingController(window,
                                                              questions_fpath,
                                                              done_fpath,
                                                              watched_fpath)
    sys.exit(app.exec())
