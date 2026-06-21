# MIT License
#
# Copyright (c) 2020 Aleksandr Kotlyar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import warnings
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver import Remote


def pytest_addoption(parser):
    """ Parse pytest --option variables from shell """
    parser.addoption('--browser', help='Which test browser?',
                     choices=['chrome', 'firefox'],
                     default='chrome')
    parser.addoption('--local', help='local or CI?',
                     choices=['true', 'false'],
                     default='true')
    parser.addoption('--selenium-url',
                     help='Remote Selenium URL. Overrides --local defaults.',
                     default=os.getenv('SELENIUM_REMOTE_URL'))
    parser.addoption('--artifacts-dir',
                     help='Directory for screenshots and page sources.',
                     default=os.getenv('TEST_ARTIFACTS_DIR',
                                       'test-artifacts'))


@pytest.fixture(scope='session')
def test_browser(request):
    """ :returns Browser.NAME from --browser option """
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def local(request):
    """ :returns true or false from --local option """
    return request.config.getoption('--local')


@pytest.fixture(scope='session')
def selenium_url(request, test_browser, local):
    """ :returns Selenium Remote URL from option or environment defaults """
    explicit_url = request.config.getoption('--selenium-url')
    if explicit_url:
        return explicit_url

    cmd_executor = {
        'true': 'http://localhost:4444',
        'false': 'http://selenium:4444'
    }
    return cmd_executor[local]


@pytest.fixture(scope='session')
def artifacts_dir(request):
    """ :returns directory for failed test diagnostics """
    path = Path(request.config.getoption('--artifacts-dir'))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _slugify(value):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', value).strip('_')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Store test reports on items so fixtures can inspect failures. """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f'rep_{report.when}', report)


@pytest.fixture(scope='function')
def remote_browser(request, test_browser, selenium_url, artifacts_dir) -> Remote:
    """ Select configuration depends on browser and host """
    if test_browser == 'firefox':
        driver = webdriver.Remote(
            options=webdriver.FirefoxOptions(),
            command_executor=selenium_url)
    elif test_browser == 'chrome':
        driver = webdriver.Remote(
            options=webdriver.ChromeOptions(),
            command_executor=selenium_url)
    else:
        raise ValueError(
            f'--browser="{test_browser}" is not chrome or firefox')
    try:
        yield driver
        report = getattr(request.node, 'rep_call', None)
        if report and report.failed:
            artifact_name = _slugify(request.node.nodeid)
            screenshot = artifacts_dir / f'{artifact_name}.png'
            page_source = artifacts_dir / f'{artifact_name}.html'
            try:
                driver.save_screenshot(str(screenshot))
                page_source.write_text(driver.page_source, encoding='utf-8')
            except Exception as error:
                warnings.warn(
                    pytest.PytestWarning(
                        f'Could not save browser diagnostics: {error}'),
                    stacklevel=2)
    finally:
        driver.quit()
