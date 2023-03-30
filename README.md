# Prompting Large Language Models for Concept Dependency Graph Extraction
This research project by [Dominik Glandorf](https://github.com/dominikglandorf) and [Anastasiia Alekseeva](https://github.com/ana-alekseeva) tries to extract knowledge from LLMs and creates baseline for the evaluation from textbooks as well as Wikipedia.

## Report
The paper about the project can be found [here](https://github.com/mlcolab/learning-dependencies/blob/main/doc/paper.pdf).

## Setup
The project is based on Python. You can install the dependencies conveniently using [conda](https://docs.conda.io/en/latest/) by running within the cloned repository:
```
conda create
conda activate LD-inference
```

The analysis can be reproduced using the experiment files in the folder [/exp](https://github.com/mlcolab/learning-dependencies/tree/main/exp). To get Wikipedia article annotations for a textbook fulltime, copy `.env.example` to `.env`, obtain a user key for [Wikifier](https://wikifier.org) API.

The interactive dashboard is located in the subfolder [/dash](https://github.com/mlcolab/learning-dependencies/tree/main/dash) and can be started within the conda enviroment executing:
```
python app.py
```
