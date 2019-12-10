from django.contrib import admin


from .models import *


admin.site.register(Patrimonio)
admin.site.register(PatrimonioEntrada)
admin.site.register(PatrimonioSaida)
admin.site.register(Ferramenta)
admin.site.register(FerramentaEntrada)
admin.site.register(FerramentaQuantidade)
admin.site.register(FerramentaSaida)
