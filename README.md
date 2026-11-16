# Lab 10 - Jenkins CI/CD Pipeline for a Python Project

EECE 435L - Nadim Matta

A small Python project (`app.py`) that a Jenkins pipeline lints, tests, measures,
scans and deploys. The pipeline is defined in `Jenkinsfile_Nadim_Matta`.

## Pipeline stages

| Stage | What it does |
|---|---|
| Setup | Creates a virtual environment and installs `requirements.txt` |
| Lint | `flake8` on the source and tests |
| Test | `pytest`, results published as JUnit |
| Coverage | `coverage.py` run + report (fails under 90%), XML and HTML reports archived |
| Security Scan | `bandit` on `app.py` and `deploy.py`; any finding fails the build |
| Deploy | `deploy.py` copies the app to `$JENKINS_HOME/deployments/Python-CI-CD` and smoke-tests it |

Tools are called as `python -m <tool>` so the pipeline also works on Windows
machines where Device Guard blocks the `.exe` launchers pip creates in the venv.

## Run locally

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
python -m flake8 app.py deploy.py tests
python -m pytest
python -m coverage run -m pytest && python -m coverage report
python -m bandit app.py deploy.py
python deploy.py --target deploy
```

## Jenkins job

Pipeline job `Python-CI-CD`, "Pipeline script from SCM", Git
`https://github.com/ntm05/Lab10-Nadim-Matta.git`, branch `*/main`,
Script Path `Jenkinsfile_Nadim_Matta`.
