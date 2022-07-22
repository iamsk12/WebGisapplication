from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from app1.models import PointVect, vect


class Admin(LeafletGeoAdmin):
    # fields to show in admin listview
    list_display = ('gid','name', 'geom')


# register models in the admin site
admin.site.register(PointVect, Admin)
admin.site.register(vect, Admin)