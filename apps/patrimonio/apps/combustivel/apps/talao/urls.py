from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/combustivel/talao/',
        views.index,
        name='patrimonio_combustivel_talao'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/',
        views.cadastros,
        name='patrimonio_combustivel_talao_cadastros'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/combustivel/',
        views.cadastrar_combustivel,
        name='patrimonio_combustivel_talao_cadastrar_combustivel'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/posto/',
        views.cadastrar_posto,
        name='patrimonio_combustivel_talao_cadastrar_posto'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/talao/',
        views.cadastrar_talao,
        name='patrimonio_combustivel_talao_cadastrar_talao'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/beneficiario/',
        views.cadastrar_beneficiario,
        name='patrimonio_combustivel_talao_cadastrar_beneficiario'
    ),
    path(
        'patrimonio/combustivel/talao/cadastros/veiculo/',
        views.cadastrar_veiculo,
        name='patrimonio_combustivel_talao_cadastrar_veiculo'
    ),
    path(
        'patrimonio/combustivel/talao/taloes/',
        views.taloes,
        name='patrimonio_combustivel_talao_taloes'
    ),
    path(
        'patrimonio/combustivel/talao/taloes/entrega/',
        views.entregar_talao,
        name='patrimonio_combustivel_talao_entregar_talao'
    ),
    path(
        'patrimonio/combustivel/talao/taloes/devolucao/',
        views.devolucao_talao,
        name='patrimonio_combustivel_talao_devolucao_talao'
    ),
    path(
        'patrimonio/combustivel/talao/vales/',
        views.vales,
        name='patrimonio_combustivel_talao_vales'
    ),
    path(
        'patrimonio/combustivel/talao/vales/entrega-1/',
        views.entregar_vale_1,
        name='patrimonio_combustivel_talao_entregar_vale_1'
    ),
    path(
        'patrimonio/combustivel/talao/vales/entrega-2/',
        views.entregar_vale_2,
        name='patrimonio_combustivel_talao_entregar_vale_2'
    ),
    path(
        'patrimonio/combustivel/talao/vales/edicao/',
        views.vales_buscar_vale_entregue,
        name='patrimonio_combustivel_talao_vales_buscar_vale_entregue'
    ),
    path(
        'patrimonio/combustivel/talao/vales/edicao/<int:vale_id>/',
        views.vales_editar_entrega,
        name='patrimonio_combustivel_talao_vales_editar_entrega'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/',
        views.consultas,
        name='patrimonio_combustivel_talao_consultas'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/taloes',
        views.consulta_talao,
        name='patrimonio_combustivel_talao_consultar_talao'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/taloes/<int:talao>',
        views.consulta_talao_detalhe,
        name='patrimonio_combustivel_talao_consultar_talao_detalhe'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/usuario/taloes/',
        views.consulta_meu_talao,
        name='patrimonio_combustivel_talao_consultar_meu_talao'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/usuario/vales/',
        views.consulta_meu_vale,
        name='patrimonio_combustivel_talao_consultar_meu_vale'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/funcionarios/',
        views.consulta_funcionarios,
        name='patrimonio_combustivel_talao_consultar_funcionarios'
    ),
    path(
        'patrimonio/combustivel/talao/consultas/vales/',
        views.consulta_vales,
        name='patrimonio_combustivel_talao_consultar_vales'
    ),
    path(
        'patrimonio/combustivel/talao/relatorios/',
        views.relatorios,
        name='patrimonio_combustivel_talao_relatorios'
    ),
    path(
        'patrimonio/combustivel/talao/relatorios/mes',
        views.relatorio_mes,
        name='patrimonio_combustivel_talao_relatorio_mes'
    ),
    path(
        'patrimonio/combustivel/talao/relatorios/geral',
        views.relatorio_geral,
        name='patrimonio_combustivel_talao_relatorio_geral'
    ),
    path(
        'patrimonio/combustivel/talao/relatorios/geral/<str:user>',
        views.relatorio_geral_detalhe,
        name='patrimonio_combustivel_talao_relatorio_geral_detalhe'
    ),

    # path(
    #     'patrimonio/combustivel/menu-cadastros/cadastro-talao/',
    #     views.view_cadastrar_talao,
    #     name='gc_cadastro_talao'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-cadastros/cadastro-combustivel/',
    #     views.view_cadastrar_combustivel,
    #     name='gc_cadastro_combustivel'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-cadastros/cadastro-posto/',
    #     views.view_cadastrar_posto,
    #     name='gc_cadastro_posto'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-consultas/consulta-taloes/',
    #     views.view_taloes,
    #     name='gc_consulta_taloes',
    # ),
    # path(
    #     'patrimonio/combustivel/menu-consultas/consulta-meus-taloes/',
    #     views.view_meus_taloes,
    #     name='gc_consulta_meus_taloes',
    # ),
    # path(
    #     'patrimonio/combustivel/menu-consultas/consulta-taloes/talao=<int:talao_id>/',
    #     views.view_talao,
    #     name='gc_consulta_talao'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-consultas/consulta-meus-taloes/talao=<int:talao_id>/',
    #     views.view_meu_talao,
    #     name='gc_consulta_meu_talao'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-consultas/consulta-meus-vales/',
    #     views.view_meus_vales,
    #     name='gc_consulta_meus_vales'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-relatorios/mensal/',
    #     views.view_relatorio_mensal,
    #     name='gc_relatorio_mensal'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-relatorios/beneficiarios/',
    #     views.view_relatorio_beneficiarios,
    #     name='gc_relatorio_beneficiarios'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-relatorios/beneficiarios/<str:funcionario>/',
    #     views.view_relatorio_beneficiarios_detalhe,
    #     name='gc_relatorio_beneficiarios_detalhe'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-taloes/entrega-talao/',
    #     views.view_entrega_talao,
    #     name='gc_entrega_talao'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-vales/entrega-vale-1/',
    #     views.view_entrega_vale_1,
    #     name='gc_entrega_vale_1'
    # ),
    # path(
    #     'patrimonio/combustivel/menu-vales/entrega-vale-2/',
    #     views.view_entrega_vale_2,
    #     name='gc_entrega_vale_2'
    # ),
]
