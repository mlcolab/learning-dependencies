# Inference of learning dependencies

## Setup
1. Install environment with conda:
```
conda create
conda activate LD-inference
```
1. Copy `.env.example` to `.env` and obtain a user key for the Wikifier to be able to link raw text entities to Wiki pages.

To add a dependency, call `conda install [PACKAGE_NAME]` and export the environment again `conda env export --from-history>environment.yml`.