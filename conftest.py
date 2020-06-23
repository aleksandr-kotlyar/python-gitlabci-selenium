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

import pytest
from selenium import webdriver
from selenium.webdriver import Remote


def pytest_addoption(parser):
    """ Parse pytest --option variables from shell """
    parser.addoption('--browser', help='Which test browser?',
                     default='chrome')
    parser.addoption('--local', help='local or CI?',
                     choices=['true', 'false'],
                     default='true')


@pytest.fixture(scope='session')
def test_browser(request):
    """ :returns Browser.NAME from --browser option """
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def local(request):
    """ :returns true or false from --local option """
    return request.config.getoption('--local')


@pytest.fixture(scope='function')
def remote_browser(test_browser, local) -> Remote:
    """ Select configuration depends on browser and host """
    if local != 'true' and local != 'false':
        raise ValueError(f'--local={local}". Driver could not be setup.\n'
                         'pass "true" if local execute\n'
                         'pass "false" if use CI service')
    cmd_executor = {
        'true': 'http://localhost:4444/wd/hub',
        'false': f'http://selenium__standalone-{test_browser}:4444/wd/hub'
    }
    if test_browser == 'firefox':
        driver = webdriver.Remote(
            options=webdriver.FirefoxOptions(),
            command_executor=cmd_executor[local])
    elif test_browser == 'chrome':
        driver = webdriver.Remote(
            options=webdriver.ChromeOptions(),
            command_executor=cmd_executor[local])
    else:
        raise ValueError(
            f'--browser="{test_browser}" is not chrome or firefox')
    yield driver
    driver.quit()
