env:
	if [ ! -d venv ]; then python3 -m venv venv; fi

install:
	venv/bin/pip install --quiet --upgrade pip && \
		venv/bin/pip install -qr requirements.txt

lint:
	venv/bin/pylint --disable=R *.py

test:
	venv/bin/coverage run -m unittest *_test.py && \
		venv/bin/coverage report -m

format:
	venv/bin/black *.py

clean:
	rm -rf venv __pycache__ .coverage

all: env install lint test
