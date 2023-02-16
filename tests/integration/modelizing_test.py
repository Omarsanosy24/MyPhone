from apps.customer import models as customer
from apps.customer.services import create_customer
from apps.device import models as device
from apps.device import services
from apps.device.services import create_device
from apps.order import models as order


def test_variant(db):
    storage = device.VariantGroup.objects.create(name="Storage")
    g128 = device.VariantValue.objects.create(group=storage, value="128G")

    color = device.VariantGroup.objects.create(name="Color")
    blue = device.VariantValue.objects.create(group=color, value="Blue")
    red = device.VariantValue.objects.create(group=color, value="Red")

    s7 = services.get_or_create_model(
        company="Samsung",
        category="Smartphone",
        product="Galaxy",
        series="S",
        model="S7",
    )

    s7variant = device.ModelVariant.objects.create(model=s7, price=1)
    s7variant.variant.set([g128, blue])
    s7variant.save()
    assert device.ModelVariant.valid_variants([g128, blue])
    assert not device.ModelVariant.valid_variants([red, blue])
    words = "Samsung Galaxy S S7 128G Blue".split()
    s = str(s7variant)
    for word in words:
        assert word in s


def test_get_variants(db):
    xs = services.get_or_create_model(
        company="Apple",
        category="Smartphone",
        product="iPhone",
        series="iPhone",
        model="XS",
    )

    storage = device.VariantGroup.objects.create(name="Storage")
    g128 = device.VariantValue.objects.create(group=storage, value="128G")
    g256 = device.VariantValue.objects.create(group=storage, value="256G")

    color = device.VariantGroup.objects.create(name="Color")
    blue = device.VariantValue.objects.create(group=color, value="Blue")
    red = device.VariantValue.objects.create(group=color, value="Red")

    xs_variant1 = device.ModelVariant.objects.create(model=xs, price=120)
    xs_variant1.variant.set([g256, blue])

    assert services.get_variants(xs) == {
        "Storage": [
            "256G",
        ],
        "Color": [
            "Blue",
        ],
    }

    assert services.get_available_variants(xs) == []
    create_device(xs_variant1)
    assert services.get_available_variants(xs) == [
        {
            "Color": "Blue",
            "Storage": "256G",
            "price": 120,
            "id": xs_variant1.id,
        },
    ]

    xs_variant2 = device.ModelVariant.objects.create(model=xs, price=80)
    xs_variant2.variant.set([g128, red])
    create_device(xs_variant2)

    assert services.get_variants(xs) == {
        "Storage": [
            "128G",
            "256G",
        ],
        "Color": [
            "Blue",
            "Red",
        ],
    }
    assert services.get_available_variants(xs) == [
        {
            "Color": "Blue",
            "Storage": "256G",
            "price": 120,
            "id": xs_variant1.id,
        },
        {
            "Color": "Red",
            "Storage": "128G",
            "price": 80,
            "id": xs_variant2.id,
        },
    ]


def test_device(db):
    a10 = services.get_or_create_model_variant(
        company="Samsung",
        category="Smartphone",
        product="Galaxy",
        series="A",
        model="10",
        price=130,
    )
    dev = device.Device.objects.create(
        imei=(imei := "12354839547389"),
        serial_number=(n := "uheacura123"),
        model_variant=a10,
    )
    words = f"Samsung Galaxy A {imei}".split()
    s = str(dev)
    for w in words:
        assert w in s


def test_order(db):
    a10 = services.get_or_create_model_variant(
        company="Samsung",
        category="Smartphone",
        product="Galaxy",
        series="A",
        model="10",
        storage="128G",
        price=150,
    )
    xs = services.get_or_create_model_variant(
        company="Apple",
        category="Smartphone",
        product="iPhone",
        series="iPhone",
        model="XS",
        color="Blue",
        price=200,
    )
    o = order.Order.objects.create(customer=create_customer("Him"))
    one_xs = order.Line.objects.create(model_variant=xs, quantity=1, order=o)
    two_a10 = order.Line.objects.create(model_variant=a10, quantity=2, order=o)
    assert o.price == 500
