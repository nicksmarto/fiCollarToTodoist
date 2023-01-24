This python script uses the pytryfi library to query a Fi dog collar's battery, and if below a configurable percentage, create a task in Todoist using Todoist's REST API.

Basic installation instructions:

1) Install requirements using:
pip install -r requirements.txt

2) Edit config.py.dist with your APIs keys and Todoist parameters, and remove the '.dist'

3) Schedule CRON job for fiToTodist.py

That's it!