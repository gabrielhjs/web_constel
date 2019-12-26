from django.core.management.color import no_style
from django.db import connection

from constel.models import *
from apps.almoxarifado.models import *
from apps.almoxarifado.apps.lista_saida.models import *
from apps.patrimonio.apps.ferramenta.models import *
from apps.patrimonio.apps.combustivel.apps.talao.models import *
from apps.patrimonio.apps.patrimonio1.models import *


def sync():

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [
        UserType,
        Veiculo,
        Fornecedor,
        Material,
        MaterialQuantidade,
        Ordem,
        MaterialEntrada,
        MaterialSaida,
        Lista,
        Item,
        Ferramenta,
        FerramentaQuantidade,
        FerramentaEntrada,
        FerramentaSaida,
        Talao,
        Vale,
        Combustivel,
        Posto,
        CadastroTalao,
        EntregaTalao,
        EntregaVale,
        Patrimonio,
        PatrimonioEntrada,
        PatrimonioSaida,
    ])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)
