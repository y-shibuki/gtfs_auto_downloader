PYTHON_VERSION := $(shell cat .python_version)

install:
	poetry env use $(PYTHON_VERSION)
	poetry install
	poetry run pip install -r requirements.txt

run_crawler:
	nohup python main.py > log/out.log 2> log/error.log &