.PHONY: clean register publish

clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +

register:
	python3 setup.py register

publish:
	python3 setup.py sdist upload
	python3 setup.py bdist_wheel upload
	rm -fr build dist .egg iquery.egg-info
