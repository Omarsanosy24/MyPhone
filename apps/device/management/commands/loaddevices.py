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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._variants = []

    def add_arguments(self, parser):
        parser.add_argument(
            "target",
            nargs="?",
            type=str,
            choices=["base", "new", "others"],
            default="new",
        )
        parser.add_argument(
            "--minimal",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        target = options["target"]
        if target == "base":
            self.handle_base(*args, **options)
            self.add_variants()
        elif target == "new":
            self.handle_new(*args, **options)
        elif target == "others":
            self.handle_others(*args, **options)
        self.generate_devices()
        self.stdout.write(self.style.SUCCESS("Data successfully loaded"))

    def handle_new(self, *args, **options):
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

    def handle_base(self, *args, **options):
        data = self.get_json()
        for company in data["companies"]:
            self._make(models.Company, **company)
        for company in data["categories"]:
            self._make(models.Category, **company)
        for product_ in data["products"]:
            self._make(models.Product, **product_)
        for series in data["series"]:
            self._make(models.Series, **series)
        for model in data["models"]:
            self._make(models.Model, **model)

    def add_variants(self):
        for model in models.Model.objects.all():
            self._add_variants(model)

    def get_variants_values(self):
        if self._variants:
            return self._variants
        storage = models.VariantGroup.objects.get_or_create(name="storage")[0]
        storages = [
            models.VariantValue.objects.get_or_create(group=storage, name="128G")[0],
            models.VariantValue.objects.get_or_create(group=storage, name="256G")[0],
        ]
        state = models.VariantGroup.objects.get_or_create(name="state")[0]
        states = [
            models.VariantValue.objects.get_or_create(group=state, name=name)[0]
            for name in ("New", "A", "B", "C", "D", "Dead")
        ]
        carrier = models.VariantGroup.objects.get_or_create(name="carrier")[0]
        carriers = [
            models.VariantValue.objects.get_or_create(group=carrier, name=name)[0]
            for name in ("Unlocked", "Other", "Verizon", "AT&T", "Mobile", "Sprint")
        ]
        color = models.VariantGroup.objects.get_or_create(name="color")[0]
        colors = [
            models.VariantValue.objects.get_or_create(group=color, name="Red")[0],
            models.VariantValue.objects.get_or_create(group=color, name="Blue")[0],
        ]
        self._variants = carriers, storages, states, colors
        return self._variants

    def generate_devices(self):
        models_variants_ids = models.ModelVariant.objects.only("id")
        n = len(models_variants_ids)
        models_variants_1 = random.choices(models_variants_ids, k=n // 20)
        models_variants_2 = random.choices(models_variants_ids, k=n // 20)
        for model_variant in models_variants_1 + models_variants_2:
            create_device(model_variant)

    def _add_variants(self, model):
        self.stdout.write(
            self.style.NOTICE(f"Loading {model} variants"),
        )
        for variant in product(*self.get_variants_values()):
            model_variant = models.ModelVariant.objects.create(
                model=model,
                price=random.randint(100, 1001),
            )
            model_variant.variant.set(variant)

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

    def handle_others(self, *args, **options):
        with open(f"{self.data_folder}/others.json") as file:
            data = json.load(file)
        for company_name, products in data.items():
            company = self._make(models.Company, name=company_name)
            for product_name, spec in products.items():
                category_name = spec["category"]
                category = self._make(models.Category, name=category_name)
                product_ = self._make(
                    models.Product,
                    companyId=company.id,
                    categoryId=category.id,
                    name=product_name,
                )
                for series_name, models_ in spec["series"].items():
                    series = self._make(
                        models.Series, name=series_name, productId=product_.id
                    )
                    for model_name in models_:
                        model: models.Model = self._make(
                            models.Model, name=model_name, seriesId=series.id,
                        )
                        self._add_variants(model)
