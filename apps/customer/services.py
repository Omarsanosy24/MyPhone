import faker

from apps.customer.models import Customer

fake = faker.Faker()


def create_customer(name):
    return Customer.objects.create(name=name, address=fake.address())
