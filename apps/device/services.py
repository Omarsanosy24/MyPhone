from collections import defaultdict
from . import models
from . import models as device
from . import utils


def get_or_create_model(*, company, category, product, series, model, **kwargs):
    company = models.Company.objects.get_or_create(name=company)[0]
    category = models.Category.objects.get_or_create(name=category)[0]
    product = models.Product.objects.get_or_create(
        name=product,
        categoryId=category.id,
        companyId=company.id,
    )[0]
    series = models.Series.objects.get_or_create(name=series, productId=product.id)[0]
    return models.Model.objects.get_or_create(name=model, seriesId=series.id)[0]


def get_or_create_model_variant(
    *, company, category, product, series, model, price, **variants
):
    model = get_or_create_model(
        company=company, category=category, product=product, series=series, model=model
    )
    variant = _get_or_create_model_variant(model, price, **variants)
    return variant


def _get_or_create_model_variant(model, price, **variants):
    values = []
    for name, value in variants.items():
        group = models.VariantGroup.objects.get_or_create(name=name.title())[0]
        value = models.VariantValue.objects.get_or_create(group=group, value=value)[0]
        values.append(value)
    model_variant = models.ModelVariant.objects.get_or_create(
        model=model,
        price=price,
    )[0]
    model_variant.values.set(values)
    return model_variant


def get_variants(model):
    model_variants = models.ModelVariant.objects.filter(model=model)
    groups = defaultdict(set)
    for item in model_variants:
        for value in item.values.all():
            groups[value.group.name].add(value.value)
    return {group: sorted(groups[group]) for group in groups}


def get_available_variants(model):
    values = []
    for dev in models.Device.objects.filter(model_variant__model=model):
        values.append({
            value.group.name: value.value
            for value in dev.model_variant.values.all()
        })
    return values


def create_device(model_variant):
    return device.Device.objects.create(
        model_variant=model_variant,
        imei=utils.generate_imei(),
        serial_number=utils.generate_serial_number(),
    )
