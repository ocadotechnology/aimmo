from django.apps import apps
from django.db import models
from django.test import TestCase


class TestModels(TestCase):
    def test_models_on_delete(self):
        aimmo_models = apps.get_app_config("aimmo").get_models()

        for model in aimmo_models:
            remote_fields = self._get_model_remote_fields(model)

            for field in remote_fields:
                if model.__name__ == "Game" and (
                    field.name == "owner" or field.name == "main_user"
                ):
                    assert field.remote_field.on_delete == models.SET_NULL
                elif model.__name__ == "Game" and field.name == "worksheet":
                    assert field.remote_field.on_delete == models.PROTECT
                else:
                    assert field.remote_field.on_delete == models.CASCADE

    def _get_model_remote_fields(self, model):
        return [
            field
            for field in model._meta.get_fields()
            if isinstance(field, models.ForeignKey)
            or isinstance(field, models.OneToOneField)
        ]
