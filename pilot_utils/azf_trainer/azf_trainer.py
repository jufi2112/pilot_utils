import sys
import argparse
from os import path as osp
from pilot_utils.azf_trainer.src import AZFTrainingController
from pilot_utils.azf_trainer.ui import AZFTrainerMainWindow

from PyQt6.QtWidgets import QApplication

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return osp.dirname(sys.executable)
    else:
        return osp.dirname(osp.abspath(__file__))



if __name__ == '__main__':
    print("Copyright (C) 2025  Julien Fischer")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it for non-commercial purposes")
    parser = argparse.ArgumentParser(description="AZF Theory Trainer")
    parser.add_argument('-q', '--questions', type=str, required=False, default=None, help="Non-standard path to the questions.json file")
    parser.add_argument('-w', '--watched', type=str, required=False, default=None, help="Non-standard path to the watched.json file")
    parser.add_argument('-d', '--done', type=str, required=False, default=None, help="Non-standard path to the done.json file")
    args = parser.parse_args()
    if args.questions is None:
        questions_fpath = osp.join(get_base_dir(), 'azf_trainer_data', 'questionnaire.json')
    else:
        questions_fpath = args.questions
    if args.watched is None:
        watched_fpath = osp.join(get_base_dir(), 'azf_trainer_data', 'bookmarks.json')
    else:
        watched_fpath = args.watched
    if args.done is None:
        done_fpath = osp.join(get_base_dir(), 'azf_trainer_data', 'hidden.json')
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
