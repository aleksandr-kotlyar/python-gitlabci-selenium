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
    parser.addoption('--browser',
                     help='Which test browser?',
                     default='chrome')


@pytest.fixture(scope='session')
def test_browser(request):
    return request.config.getoption('--browser')


@pytest.fixture(scope='function')
def remote_browser(test_browser) -> Remote:
    """ Select configuration depends on browser """
    if test_browser == 'firefox':
        driver = webdriver.Remote(
            options=webdriver.FirefoxOptions(),
            command_executor='http://selenium__standalone-firefox:4444/wd/hub'
        )
        return driver

    elif test_browser == 'chrome':
        driver = webdriver.Remote(
            options=webdriver.ChromeOptions(),
            command_executor='http://selenium__standalone-chrome:4444/wd/hub'
        )
        return driver

    else:
        raise ValueError(f'--browser={test_browser} is not chrome or firefox')
