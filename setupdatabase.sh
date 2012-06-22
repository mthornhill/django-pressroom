rm pressroom.db
bin/django syncdb --noinput --all
bin/django migrate --fake
bin/django createsuperuser --username=pressroom --email=admin@example.com --noinput
bin/django set_fake_passwords
bin/django runscript -v2 --traceback load_data
bin/django collectstatic --noinput
bin/django rebuild_index --noinput
bin/django createinitialrevisions
