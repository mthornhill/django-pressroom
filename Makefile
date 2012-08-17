clean:
	@find . -name "*.pyc" -delete

test: clean
	@django-admin.py test --settings=pressroom.testsettings -v 2
