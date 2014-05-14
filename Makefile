cleanpyc:
	@find . -name "*.pyc" -exec rm -rf {} \;

test:
	python tests/manage.py test tags
