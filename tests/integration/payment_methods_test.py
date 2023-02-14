def test_stripe(client):
    assert False
    rp = client.post('/api/stripe.....')
    assert rp.status == 200
    assert rp.data == {
        "message": "Ok"
    }
