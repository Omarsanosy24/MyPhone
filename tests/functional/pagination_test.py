def test_company(client, db):
    rp = client.get("/api/device/companies")
    assert rp.status_code == 200
    data = rp.data
    assert isinstance(data, dict)
    assert isinstance(data["results"], list)
    assert isinstance(data["count"], int)
    assert "count" in data
    assert isinstance(data["count"], int)
    assert "previous" in data
    assert "next" in data
    rp = client.get("/api/device/companies?nopagination")
    assert rp.status_code == 200
    data = rp.data
    assert "count" not in data
    assert "previous" not in data
    assert "next" not in data
    assert isinstance(data, list)
