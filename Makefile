.PHONY: docs
init:
	pip install -r requirements-dev.txt

test:
	pytest tests

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg sdproperty.egg-info
