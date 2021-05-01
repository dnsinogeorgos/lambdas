env:
	if [ ! -d venv ]; then python3 -m venv venv; fi

install:
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

lint:
	venv/bin/pylint *.py
	venv/bin/flake8 *.py

test:
	venv/bin/coverage run -m unittest *_test.py
	venv/bin/coverage report -m

format:
	venv/bin/black *.py

clean:
	rm -rf venv __pycache__ .coverage

all: env install lint test
