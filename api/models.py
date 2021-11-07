from django.db import models

from api.managers import BaseModelManager

# Create your models here.

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True


class CarBrand(BaseModel):
    name = models.CharField(max_length=50, db_index=True, null=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CarModel(BaseModel):
    car_type = (
        ('sedan', 'SEDAN'),
        ('micro', 'MICRO'),
        ('suv', 'SUV'),
        ('coupe', 'COUPE'),
        ('minivan', 'MINI VAN'),
        ('van', 'VAN')
    )
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True, null=True)
    type = models.CharField(choices=car_type, default='micro', max_length=20, db_index=True)

    class Meta:
        ordering = ['brand', 'name']
    
    def __str__(self):
        return self.brand + '->' + self.name


class CarRegistrationNumber(BaseModel):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, db_index=True, null=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=50, db_index=True, null=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CarCity(BaseModel):
    car = models.ForeignKey(CarRegistrationNumber , on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Booking(BaseModel):
    status_type = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'completed'),
    )
    car = models.ForeignKey(CarCity, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    since = models.DateTimeField(default=None, null=True,db_index=True)
    upto = models.DateTimeField(default=None, null=True,db_index=True)
    status = models.CharField(choices=status_type, default='booked', max_length=20, db_index=True)
    created_by = models.PositiveSmallIntegerField(default=None)

    class Meta:
        ordering = ['-created']
