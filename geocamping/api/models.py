from django.contrib.gis.db import models


class Bungalow(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=254)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "bungalows"


class Cottage(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cottages"


class Facility(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "facilities"
        verbose_name_plural = 'Facilities'


class Service(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    subtype = models.CharField(max_length=20, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "services"


class Slot(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "slots"


class Zone(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    geom = models.MultiPolygonField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "zones"
