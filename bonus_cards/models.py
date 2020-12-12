from django.db import models


class BonusCard(models.Model):
    serial = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    expired_at = models.DateField()
    used_at = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=20,
                              choices=[
                                  ("not activated", "не активирована"),
                                  ("activated", "активирована"),
                                  ("expired", "просрочена")
                              ])
