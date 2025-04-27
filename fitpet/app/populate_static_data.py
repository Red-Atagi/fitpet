import os
import json
from django.apps import apps
from django.db.utils import IntegrityError

def load_data(model_name, json_path):
    model = apps.get_model('app', model_name)
    full_path = os.path.join(os.path.dirname(__file__), 'data', json_path)

    with open(full_path, 'r') as f:
        entries = json.load(f)

    for entry in entries:
        # Prevent duplicate entries on repeated migrations
        obj, created = model.objects.get_or_create(**entry)
        if created:
            print(f"Created {model_name}: {entry}")
        else:
            print(f"{model_name} already exists: {entry}")