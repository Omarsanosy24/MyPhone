from django.core.management import call_command

from apps.device import models


def test_json(db):
    call_command("loaddevices", format="json")
    assert models.Company.objects.count() >= 1
    assert models.Category.objects.count() >= 1
    assert models.Product.objects.count() >= 1
    assert models.Series.objects.count() >= 1
    assert models.Model.objects.count() >= 2


def test_csv(db):
    call_command("loaddevices", format="csv", minimal=True)
    assert models.Company.objects.count() >= 2
    assert models.Category.objects.count() >= 1
    assert models.Product.objects.count() >= 2
    assert models.Series.objects.count() >= 2
    assert models.Model.objects.count() >= 2
