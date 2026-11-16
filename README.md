# Lab 10 - Jenkins CI/CD Pipeline for a Python Project

EECE 435L - Nadim Matta

A small Python project (`app.py`) built, linted, tested and deployed by a Jenkins
pipeline defined in `Jenkinsfile_Nadim_Matta`.

## Run locally

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
flake8 app.py
python -m pytest
python app.py
```

## Jenkins job

Pipeline job `Python-CI-CD`, "Pipeline script from SCM", Git, branch `main`,
Script Path `Jenkinsfile_Nadim_Matta`.
