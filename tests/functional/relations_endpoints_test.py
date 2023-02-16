from django.core.management import call_command

from apps.device import models


def test_company_products(client, db):
    call_command("loaddata", "resources/fixtures/mini")
    rp = client.get("/api/device/companies/2/products")
    assert rp.status_code == 200
    assert set(p["name"] for p in rp.data) == {"Galaxy"}


def test_product_series(client, db):
    call_command("loaddata", "resources/fixtures/mini")
    rp = client.get("/api/device/products/2/series")
    assert rp.status_code == 200
    assert set(s["name"] for s in rp.data) == {"S"}


def test_series_models(client, db):
    call_command("loaddata", "resources/fixtures/mini")
    rp = client.get("/api/device/series/2/models")
    assert rp.status_code == 200
    assert "S7" in set(s["name"] for s in rp.data)
