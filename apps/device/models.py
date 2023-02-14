from django.core import validators

from apps.core.lib import models


class ModelWithName(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=32,
        unique=True,
    )

    def __str__(self):
        return self.name


class ModelWithNameAndImage(ModelWithName):
    class Meta:
        abstract = True

    imageUrl = models.CharField(
        max_length=128,
    )


class Company(ModelWithNameAndImage):
    pass


class Category(ModelWithNameAndImage):
    pass


class Product(ModelWithNameAndImage):
    company = models.ForeignKey(
        Company,
    )
    category = models.ForeignKey(
        Category,
    )

    def __str__(self):
        return f"{self.company} {self.name}"


class Series(ModelWithNameAndImage):
    product = models.ForeignKey(
        Product,
    )

    def __str__(self):
        if self.product.name == self.name:
            return str(self.product)
        return f"{self.product} {self.name}"


class Model(ModelWithNameAndImage):
    series = models.ForeignKey(
        Series,
    )

    def __str__(self):
        return f"{self.series} {self.name}"


class VariantGroup(ModelWithName):
    pass


class VariantValue(models.Model):
    group = models.ForeignKey(
        VariantGroup,
    )
    value = models.CharField(
        max_length=32,
    )

    def __str__(self):
        return f"{self.group}: {self.value}"


class ModelVariant(models.Model):
    model = models.ForeignKey(
        Model,
    )
    values = models.ManyToManyField(
        VariantValue,
    )
    price = models.FloatField()

    def __str__(self):
        s = str(self.model)
        for variant in self.values.only("value").order_by("group__name"):
            s = f"{s} {variant.value}"
        return s

    @property
    def variants(self):
        return {value.group.name: value.value for value in self.values.all()}

    @staticmethod
    def valid_variants(variants: list[VariantValue]) -> bool:
        groups = set(v.group.id for v in variants)
        return len(variants) == len(groups)


class Device(models.Model):
    class Meta:
        unique_together = [("serial_number", "model_variant")]

    model_variant = models.ForeignKey(
        ModelVariant,
    )
    imei = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            validators.MinLengthValidator(15),
        ],
    )
    serial_number = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return f"{self.model_variant} [{self.imei}]"
