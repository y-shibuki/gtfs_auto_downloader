PYTHON_VERSION := $(shell cat .python-version)

install:
	poetry env use $(PYTHON_VERSION)
	poetry install

run_crawler:
	nohup python main.py > log/out.log 2> log/error.log &