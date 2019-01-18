# starter_repo
Repo to initialize class repositories from, setups initial CI/CD for gitlab as well

## regular files

* **Dockerfile** - Initial dockerfile to help us setup our environment
* **docker-compose.yml** - Initial starter docker-compose file
* **requirements.txt** - Blank requirements.txt file for us to add python package requirements into

## hidden files

* **.gitignore** - ignores python code & macOS generated files that don't need to be in the repo
* **.gitlab-ci.yml** - initial CI/CD pipeline file that will be used in CINS465 during class, should be modified to fit your project/code
* **.coveragerc** - provides initial settings for the coverage.py package to test our CI testing coverage and omit specific files/folders/lines that are problematic. This will need to be moved and modified to be useful, and will be introduced in class. 
