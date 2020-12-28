#!/usr/bin/env python
import os
import sys

from kubernetes.config import load_kube_config

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    from django.core.management import execute_from_command_line

    import logging

    logging.basicConfig()

    if not os.environ.get("USING_CYPRESS", False):
        load_kube_config(context="agones")

    execute_from_command_line(sys.argv)
