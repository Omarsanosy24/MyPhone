import csv

from django.core.management import BaseCommand

from apps.device import models


class Command(BaseCommand):
    help = "Dump devices DB into resources"

    data_folder = "resources/rawdata"

    first_headers = [
        "company",
        "category",
        "series",
        "product",
        "model",
        "imageUrl",
    ]
    last_headers = [
        "price",
    ]

    def handle(self, *args, **options):
        # self.stdout.write(self.style.SUCCESS("Data successfully loaded"))
        with open(f"{self.data_folder}/dump_items.csv", "w") as file:
            headers = self.get_headers()
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            self.write_rows(writer)

    def write_rows(self, writer):
        for model_variant in models.ModelVariant.objects.all():
            writer.writerow(
                dict(
                    company=model_variant.model.series.product.company.name,
                    category=model_variant.model.series.product.category.name,
                    product=model_variant.model.series.product.name,
                    series=model_variant.model.series.name,
                    model=model_variant.model.name,
                    **model_variant.variants,
                    price=model_variant.price,
                    imageUrl=model_variant.model.imageUrl,
                )
            )

    def get_headers(self):
        return self.first_headers + self._get_variants_groups() + self.last_headers

    def _get_variants_groups(self):
        groups = models.VariantGroup.objects.values_list("name", flat=True)
        return list(groups)
