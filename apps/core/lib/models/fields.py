from django.db.models import ForeignKey, CASCADE


class BaseForeignKey(ForeignKey):
    def __init__(self, to, on_delete=CASCADE, *args, **kwargs):
        super().__init__(to, on_delete, *args, **kwargs)

    def get_attname(self):
        return f"{self.name}Id"
