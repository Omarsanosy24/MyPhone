import csv
import json
import random
from itertools import product

from django.core.management import BaseCommand

from apps.device import models, services
from apps.device.services import create_device


class Command(BaseCommand):
    help = "Load devices resources into DB"

    data_folder = "resources/rawdata"

    relations = [
        "company",
        "category",
        "product",
        "series",
        "model",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "format",
            nargs="?",
            type=str,
            choices=["json", "csv"],
            default="csv",
        )
        parser.add_argument(
            "--minimal",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if options["format"] == "json":
            self.handle_json(*args, **options)
            self.add_variants()
        else:
            self.handle_csv(*args, **options)
        self.generate_devices()
        self.stdout.write(self.style.SUCCESS("Data successfully loaded"))

    def handle_csv(self, *args, **options):
        data = self.get_csv()
        for row in data:
            if options["minimal"]:
                if not any(model in str(row) for model in {"S7", "XS"}):
                    continue
            self.stdout.write(
                self.style.NOTICE(f"Loading {row} variants"),
            )
            services.get_or_create_model_variant(**row)

    def get_csv(self):
        with open(f"{self.data_folder}/items.csv") as file:
            return list(csv.DictReader(file))

    def get_json(self):
        with open(f"{self.data_folder}/db.json") as file:
            return json.load(file)

    def handle_json(self, *args, **options):
        data = self.get_json()
        for company in data["companies"]:
            self._make(models.Company, **company)
        for company in data["categories"]:
            self._make(models.Category, **company)
        for product in data["products"]:
            self._make(models.Product, **product)
        for series in data["series"]:
            self._make(models.Series, **series)
        for model in data["models"]:
            self._make(models.Model, **model)

    def add_variants(self):
        storage = models.VariantGroup.objects.get_or_create(name="Storage")[0]
        color = models.VariantGroup.objects.get_or_create(name="Color")[0]
        g128 = models.VariantValue.objects.get_or_create(group=storage, value="128G")[0]
        g256 = models.VariantValue.objects.get_or_create(group=storage, value="256G")[0]
        red = models.VariantValue.objects.get_or_create(group=color, value="Red")[0]
        blue = models.VariantValue.objects.get_or_create(group=color, value="Blue")[0]
        for model in models.Model.objects.all():
            self._add_variants(model, blue, g128, g256, red)

    def generate_devices(self):
        models_variants_ids = models.ModelVariant.objects.only("id")
        n = len(models_variants_ids)
        models_variants_1 = random.choices(models_variants_ids, k=n // 20)
        models_variants_2 = random.choices(models_variants_ids, k=n // 20)
        for model_variant in models_variants_1 + models_variants_2:
            create_device(model_variant)

    def _add_variants(self, model, blue, g128, g256, red):
        self.stdout.write(
            self.style.NOTICE(f"Loading {model} variants"),
        )
        for variant in product([g128, g256], [red, blue]):
            model_variant = models.ModelVariant.objects.create(
                model=model,
                price=random.randint(100, 1001),
            )
            model_variant.values.set(variant)

    def _make(self, model, **fields):
        fields = dict(self._rewrite_fields(fields))
        self.stdout.write(
            self.style.NOTICE(f"Creating {model.__name__}(**{fields})"),
        )
        try:
            return model.objects.get_or_create(**fields)[0]
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"{err}"))

    def _rewrite_fields(self, fields):
        for k, v in fields.items():
            if k in self.relations:
                k += "Id"
            yield k, v
