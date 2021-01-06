# Selenium with Docker and GitLab

![GitHub statistics](https://raw.githubusercontent.com/aleksandr-kotlyar/python-gitlabci-selenium/traffic-2021/traffic-python-gitlabci-selenium/in_2021.svg)
![GitHub views](https://raw.githubusercontent.com/aleksandr-kotlyar/python-gitlabci-selenium/traffic-2021/traffic-python-gitlabci-selenium/views.svg)
![GitHub views per week](https://raw.githubusercontent.com/aleksandr-kotlyar/python-gitlabci-selenium/traffic-2021/traffic-python-gitlabci-selenium/views_per_week.svg)
![GitHub clones](https://raw.githubusercontent.com/aleksandr-kotlyar/python-gitlabci-selenium/traffic-2021/traffic-python-gitlabci-selenium/clones.svg)
![GitHub clones per week](https://raw.githubusercontent.com/aleksandr-kotlyar/python-gitlabci-selenium/traffic-2021/traffic-python-gitlabci-selenium/clones_per_week.svg)

## About
Python project template for those who want to quickly start running their Selenium tests in GitLabCI. The template will be helpful enough for the first time if you just starting new test automation project and need a simple CI or even if you are new to GitLab, Docker, Selenium but need to run Selenium tests in CI.
#### Browsers support
- Chrome (default)
- Firefox
## GitLab Usage
- To run job with Chrome just run pipeline with one of the Triggers
- To run job with Firefox set GitLab variable BROWSER=firefox and run pipeline with one of the Triggers 
#### CI Triggers
- **Manual** "Run pipeline" from WebUI
- **Schedule** to start pipeline by cron
- **Push** commit to gitlab and pipeline will start automatically
- **Trigger** API endpoint to start pipeline
## Local Usage
Prepare
```shell script
docker run -d -p 4444:4444 --net grid --name selenium-hub selenium/hub:3.141.59
docker run -d --net grid -e HUB_HOST=selenium-hub --name chrome -v /dev/shm:/dev/shm selenium/node-chrome
docker run -d --net grid -e HUB_HOST=selenium-hub --name firefox -v /dev/shm:/dev/shm selenium/node-firefox
```
Run tests
```shell script
# tests on Chrome
pytest
# or
pytest --browser=chrome
# tests on Firefox 
pytest --browser=firefox
```
End of work
```shell script
docker stop selenium-hub chrome firefox
```