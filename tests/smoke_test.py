from rest_framework.authtoken.models import Token

from apps.core.models import User


def test_smoke(client):
    rp = client.get("/smoke")
    assert rp.status_code == 200
    assert rp.data == {"smoke": True}


def test_private_smoke(client, db):
    rp = client.get("/private-smoke")
    assert rp.status_code >= 400
    admin = User.objects.create(username="admin")
    token = Token.objects.create(user=admin)
    rp = client.get("/private-smoke", HTTP_AUTHORIZATION=f"Token {token}")
    assert rp.status_code == 200
    assert rp.data == {"smoke": True}


def test_current_user(client, db):
    rp = client.get("/api/me")
    assert rp.data == {}
    admin = User.objects.create(username="admin")
    client.force_login(admin)
    rp = client.get("/api/me")
    data = rp.data["data"]
    assert data["username"] == "admin"
