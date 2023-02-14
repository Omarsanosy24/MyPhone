from rest_framework_nested import routers

from apps.device import views as device_views
from apps.customer import views as customer_views
from apps.order import views as order_views
from apps.core import views as core_views

router = routers.DefaultRouter(trailing_slash=False)

# Device
router.register(r"device/companies", device_views.Company)
router.register(r"device/categories", device_views.Category)
router.register(r"device/products", device_views.Product)
router.register(r"device/series", device_views.Series)
router.register(r"device/models", device_views.Model)
router.register(r"device/variants-groups", device_views.VariantGroup)
router.register(r"device/variants-values", device_views.VariantValue)
router.register(r"device/models-variants", device_views.ModelVariant)
router.register(r"device/devices", device_views.Device)

router.register(r"users", core_views.UserViewSet)

router.register(r"customers", customer_views.CustomerViewSet)
router.register(r"lines", order_views.LineViewSet)
router.register(r"orders", order_views.OrderViewSet)
