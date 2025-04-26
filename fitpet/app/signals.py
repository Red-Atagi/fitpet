from django.core.management import call_command
from django.db import connection
from .populate_static_data import load_data

def populate_static_models(sender, **kwargs):
    if connection.settings_dict['NAME']:  # Skip if database doesn't exist
        load_data('Clothing', 'clothing.json')
        load_data('Exercise', 'exercise.json')