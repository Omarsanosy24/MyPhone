from django.core import validators

from apps.core.lib import models
from apps.order.lib import generate_order_reference


class Order(models.Model):
    type = models.CharField(
        max_length=1,
        choices=(
            ("b", "Buy"),
            ("s", "Sell"),
            ("r", "Repair"),
        ),
    )
    reference = models.CharField(
        max_length=16,
        unique=True,
        editable=False,
        default=generate_order_reference,
    )
    customer = models.ForeignKey(
        "customer.Customer",
        null=True,
    )

    def get_price(self):
        return sum(line.sub_total for line in self.line_set.all())

    price = property(get_price)

    def __str__(self):
        return f"{self.get_type_display()} Order [reference: {self.reference}]"


class Line(models.Model):
    model_variant = models.ForeignKey("device.ModelVariant")
    quantity = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
        ],
    )
    order = models.ForeignKey(
        Order,
    )

    def get_sub_total(self):
        return self.model_variant.price * self.quantity

    sub_total = property(get_sub_total)

    def __str__(self):
        return f"{self.quantity} x {self.model_variant}"
