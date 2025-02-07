# AZF Theory Trainer

This software offers multiple functions:
- Extract questions from an official pdf published by the Bundesnetzagentur
   - [Link](https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/Funkzeugnisse/Flugfunk/start.html) to the official website
- Once the questions have been extracted, you can start your training or simulate an examination:
    - In training mode, you can freely select the number of questions that you will see and you will get instant feedback on whether your selected answer was correct
    - In examination mode, you will have 30 minutes to answer 40 questions. The threshold for passing is 75%. Feedback is only given after the exam is "handed in"
        - Tip: From the evaluation menu that appears after finishing the exam, you can return to the question-view and see the feedback for each question.
    - You can bookmark tricky questions for further inspection or hide well-known questions such that they will no longer be shown in training mode
    - Questions and ordering of answers will be randomized in each run
    - Bookmarked and hidden questions can be viewed from the main menu


## Installation
For the time being, you have to install the base pilot_utils package and, from within `pilot_utils/azf_trainer` run `python azf_trainer.py`. In the future, a single executable file will be made available. Stay tuned.
