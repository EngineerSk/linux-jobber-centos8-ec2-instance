=================
eskayoriadescrumy
=================


A sample project that created to test django application deployment on EC2 instance of CentOS 8 AMI
(Amazon Machine Image) using Amazon Web Service.

Detailed documentation is in the docs.

Quick start
===========

1. Add 'eskayoriadescrumy' to your INSTALLED_APPS setting like this::

	INSTALLED_APPS = [
		...

		'eskayoriadescrumy',
	]

2. Include the eskayoriadescrumy URLconf in your project urls.py like this::

	path('eskayoriadescrumy/', include('eskayoriadescrumy.urls'))

3. Run 'python manage.py migrate' to create the eskayoriadescrumy models.

4. Start the development server and visit http://127.0.0.1:8000/admin/ to create a scrumy app instance 
   of eskayo riadescrumy (you'll need the admin app enabled)

5. Visit http://127.0.0.1/eskayoriadescrumy/ to create your scrumy app