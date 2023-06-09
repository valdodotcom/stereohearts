# stereohearts

# Rules
1. Pull latest version of 'master' and create a new branch before making any changes to code.
2. Create a pull request and discuss changes before merging into 'master'.
3. Follow naming conventions of variables at all times.
4. There are no branch protection rules on GitHub Free for private repositories so please & please again abeg wai. master branch is sacred.

# Conventions
1. DRF API functions are verbNoun (e.g. getRoutes, postNewReview).
2. view.py functions are verb_noun (e.g. register, login_user).
3. environment variables are UPPER_CASE (e.g. SITE_URL, SECRET).
4. all other variables are camel_case (e.g. display_name, username_or_email).

# Database Setup
1. Install PostgreSQL, making sure to install pgAdmin as well during the installation.
2. Create a database in pgAdmin using the same credentials as in the .env file.

# Installation Guide
Reach out to me for the .env file and any other help setting up the project. 
Outside of this project do the ff:
1. Install the package virtualenv: pip install virtualenv.
2. Create a virtual environment named 'venv' using this package.
3. Place the venv folder in the root of the project's directory
4. Activate the virtual environment
5. Make sure in your VS code you are using the venv python installation.

Now inside the project do the ff:
1. Run the command: pip install -r requirements.txt
2. Create a django superuser: python manage.py createsuperuser
3. At this point you should be ready to start work: python manage.py runserver
4. "Enjoy"
