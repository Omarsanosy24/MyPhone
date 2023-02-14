from django.core.management import call_command

from apps.core.models import User
from apps.customer.services import create_customer
from apps.order.models import Order


def test_create_order_with_lines(client, db):
    call_command("loaddata", "resources/fixtures/full.json")
    customer = create_customer("Him")
    client.force_login(User.objects.get(username="admin"))
    rp = client.post(
        '/api/orders/with-lines',
        data={
            "type": "s",
            "customer": f"/api/customers/{customer.id}",
            "lines": [
                {
                    "model_variant": "/api/device/models-variants/3",
                    "quantity": 2,
                },
                {
                    "model_variant": "/api/device/models-variants/23",
                    "quantity": 1,
                },
            ]
        }
    )
    assert rp.status_code == 201
    order = Order.objects.get(pk=rp.data["id"])
    assert order.line_set.count() == 2
