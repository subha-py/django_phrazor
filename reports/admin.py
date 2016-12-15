from django.contrib import admin
from reports.models import (
    Report,
    Narrative,
    Segment,
    Text,
    Branch,
    Condition,
    Datavar,
    Synonym,
    SynonymVariation
)
# Register your models here.
admin.site.register(Report)
admin.site.register(Narrative)
admin.site.register(Segment)
admin.site.register(Text)
admin.site.register(Branch)
admin.site.register(Condition)
admin.site.register(Datavar)
admin.site.register(Synonym)
admin.site.register(SynonymVariation)






