# Selenium with Docker and GitLab

## About
Python project template for those who want to quickly start running Selenium
tests in GitLab CI. The template is intentionally small: pytest creates a
remote browser session, GitLab starts a Selenium service, and failed tests save
diagnostic artifacts.

#### Browsers support
- Chrome (default)
- Firefox

## GitLab Usage
- To run tests with Chrome, run a pipeline with default variables.
- To run tests with Firefox, set GitLab variable `BROWSER=firefox`.

The pipeline waits for Selenium before starting tests and always publishes:
- `reports/junit.xml`
- screenshots for failed tests
- page sources for failed tests

Selenium readiness is checked by `scripts/wait_for_selenium.py`.

#### CI Triggers
- **Manual** "Run pipeline" from WebUI
- **Schedule** to start pipeline by cron
- **Push** commit to gitlab and pipeline will start automatically
- **Trigger** API endpoint to start pipeline

## Local Usage
Create and activate a Python environment, then install requirements:
```shell script
python3.14 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Run tests with a local Chrome Selenium service:
```shell script
docker run -d -p 4444:4444 --name selenium -v /dev/shm:/dev/shm selenium/standalone-chrome:latest
pytest --browser=chrome
docker stop selenium
docker rm selenium
```

Run tests with a local Firefox Selenium service:
```shell script
docker run -d -p 4444:4444 --name selenium -v /dev/shm:/dev/shm selenium/standalone-firefox:latest
pytest --browser=firefox
docker stop selenium
docker rm selenium
```

Use a custom Selenium Remote URL:
```shell script
pytest --browser=chrome --selenium-url=http://localhost:4444
```

Failed test diagnostics are saved to `test-artifacts/` by default. Override the
directory with:
```shell script
pytest --artifacts-dir=artifacts
```
