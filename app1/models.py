from msilib.schema import Class
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class vect(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    geom = geomodels.MultiPolygonField(srid=0)
    
    class Meta:
        managed = False
        db_table = "ne_10m_parks_and_protected_lands_area"
        
class PointVect(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    geom = geomodels.PointField(srid=0)
    
    class Meta:
        managed = False
        db_table = "ne_10m_parks_and_protected_lands_point"

    # Password@1234
class MapData():
    showVector = models.BooleanField()
    geom = []