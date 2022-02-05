from .models import Configuration

config:Configuration = Configuration.load()
"""Editable configuration file"""