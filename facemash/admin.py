from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'admin_image')

    class Media:
        css = {
            "all": ('bower_components/dropzone/dist/dropzone.css',
                    'facemash/css/dropzone.css',)
        }
        js = ('bower_components/dropzone/dist/dropzone.js',
              'facemash/js/load_dropzone.js',)
