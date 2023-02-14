from django.core.management import call_command


def test_products_list(client, db):
    call_command("loaddata", "resources/fixtures/mini.json")
    rp = client.get("/api/device/products")
    product_one = rp.data["results"][0]
    assert "company" in product_one
    assert "category" in product_one
    assert "companyInfo" in product_one
    assert "categoryInfo" in product_one
    assert "name" in product_one["categoryInfo"]
    assert "name" in product_one["companyInfo"]
