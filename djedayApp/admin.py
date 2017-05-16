from django.contrib import admin
from .models import Planet, Djeday, Candidates, SpisokVoprosov, Voprosi, Otveti


class VItemsInline(admin.TabularInline):
    model = Voprosi


class SVAdmin(admin.ModelAdmin):
    inlines = [VItemsInline, ]

    list_display = ['code', ]
    class Meta:
        model = SpisokVoprosov


admin.site.register(SpisokVoprosov, SVAdmin)
admin.site.register(Planet)
admin.site.register(Djeday)
admin.site.register(Candidates)
admin.site.register(Otveti)

# admin.site.register(SpisokVoprosov)
