cleanpyc:
	@find . -name "*.pyc" -exec rm -rf {} \;

test:
	coverage run tests/manage.py test tags

coverage:
	coverage html
