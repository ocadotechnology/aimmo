#!/usr/bin/env python
import os
import sys

from kubernetes.config import load_kube_config

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    import logging

    logging.basicConfig()

    if os.environ.get("LOAD_KUBE_CONFIG", "1") == "1":
        load_kube_config(context="agones")

    execute_from_command_line(sys.argv)
