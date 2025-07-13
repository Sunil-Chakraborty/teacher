import os
import subprocess

# Suppress GLib warnings
os.environ['G_MESSAGES_DEBUG'] = ''
os.environ['G_MESSAGES_PREFIXED'] = ''

# Run Django server
subprocess.run(['python', 'manage.py', 'runserver'])