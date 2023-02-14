from django.core.management import call_command


def test_search_model(client, db):
    call_command("loaddata", "resources/fixtures/mini.json")
    rp = client.get("/api/device/models?search=S7")
    results = rp.data["results"]
    names = set(model["name"] for model in results)
    assert names == {"S7", "S7 Active", "S7 Edge"}


def test_search_model_variant(client, db):
    call_command("loaddata", "resources/fixtures/mini.json")
    rp = client.get("/api/device/models-variants?search=XS+Max+Red")
    results = rp.data["results"]
    names = set(model["str"] for model in results)
    assert names >= {
        "Apple iPhone XS Max Red 256G",
        "Apple iPhone XS Max Red 128G",
    }
