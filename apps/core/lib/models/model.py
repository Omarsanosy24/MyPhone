from safedelete.models import SafeDeleteModel


class BaseModel(SafeDeleteModel):
    class Meta:
        abstract = True
