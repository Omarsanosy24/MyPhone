from apps.customer.models import Customer
from apps.customer.services import create_customer


def test_soft_delete(db):
    customer = create_customer("Me")
    assert not customer.is_deleted
    assert Customer.objects.filter(name="Me").exists()
    customer.delete()
    assert customer.is_deleted
    assert not Customer.objects.filter(name="Me").exists()
    assert Customer.all_objects.filter(name="Me").exists()
