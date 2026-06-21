# Changelog

## Unreleased
 - Added Selenium service readiness check in GitLab CI.
 - Added reusable Selenium readiness check script.
 - Added Docker Compose setup for local Selenium service.
 - Added JUnit report and failed-test diagnostic artifacts in GitLab CI.
 - Added pytest markers for browser, external, and smoke tests.
 - Added configurable Selenium Remote URL and artifacts directory.
 - Removed GitHub traffic badge workflow.
 - Updated README local and GitLab usage instructions.

## 3.0.0 (planned, not released)
 - Add execution in GitHub Actions.

## 2.2.0 (Released 16.05.2020)
 - Totally updated About in README.
 - Added documentation for fixtures.
 - Compacted condition tree in remote browser fixture at x2 times.

## 2.1.0 (Released 09.03.2020)
 - Added execution on localhost selenium hub.
 - Added README.

## 2.0.0 (Released 08.03.2020)
 - Added LICENSE for using.
 - Added Firefox job.
 - Added --browser option for selecting chrome or firefox to run tests in. Default is chrome.
 - Renamed fixture 'browser' to 'remote_browser'.

## 1.0.0 (Released 08.03.2020)
 - Bump version for release.

## 0.1.1
 - Fixed: throw chrome Options() to Remote webdriver.

## 0.1.0
 - Created simple gitlab-ci testing project with selenium, remote standalone-chrome and one selenium test in ci job.
