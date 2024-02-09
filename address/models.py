from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    psgc_code = models.CharField(max_length=255, unique=True)
    region_code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=255, unique=True)
    province_code = models.CharField(max_length=255, unique=True)
    psgc_code = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class City_Municipality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    psgc_code = models.CharField(max_length=255, unique=True)
    city_municipality_code = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Barangay(models.Model):
    name = models.CharField(max_length=255, unique=True)
    barangay_code = models.CharField(max_length=255, unique=True)
    city_municipality = models.ForeignKey(City_Municipality, on_delete=models.PROTECT)

    def __str__(self):
        return self.name