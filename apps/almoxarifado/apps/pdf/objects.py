from fpdf import FPDF
from io import BytesIO
from calendar import monthrange

from django.db.models import Count

from apps.almoxarifado.models import MaterialEntrada, MaterialSaida
from ..cont.models import OntSaida, OntDevolucao


class FichaMateriais(FPDF):

    def __init__(self, ordem, format1='A4', unit='mm', orientation='P'):
        super().__init__(orientation, unit, format1)

        self.set_auto_page_break(False)
        self.ordem = ordem
        self.add_page()
        self.set_font('Times', size=12)
        self.epw = self.w - 2 * self.l_margin
        self.th = self.font_size
        self.cabecalho()
        self.tabela()
        if self.ordem.tipo == 1:
            self.rodape()
            
    def cabecalho(self):

        if self.ordem.tipo == 0:
            cabecalho_texto = 'FICHA DE ENTRADA DE MATERIAIS NO ALMOXARIFADO'
            cabecalho_fornecedor_tecnico = 'Fornecedor:'
            fornecedor_tecnico = str(self.ordem.almoxarifado_ordem_entrada.first().fornecedor.nome)
            fornecedor_tecnico_id = self.ordem.almoxarifado_ordem_entrada.first().fornecedor.cnpj

        else:
            cabecalho_texto = 'FICHA DE SAÍDA DE MATERIAIS DO ALMOXARIFADO'
            cabecalho_fornecedor_tecnico = 'Técnico:'
            fornecedor_tecnico = self.ordem.almoxarifado_ordem_saida.first().user_to.get_full_name().title()
            fornecedor_tecnico_id = self.ordem.almoxarifado_ordem_saida.first().user_to.username

        self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
        self.ln(self.th * 2)
        self.set_font_size(8)

        data = self.ordem.data.strftime('%d/%m/%Y')
        hora = self.ordem.data.strftime('%H:%M:%S')
        colunas = [self.epw * .15, self.epw * .15, self.epw * .3, self.epw * .3, self.epw * .1]
        responsavel = self.ordem.user.get_full_name().title()
        responsavel_id = self.ordem.user.username
        
        linha = self.th * .8
        
        self.cell(colunas[0], linha, 'Data:', align='L')
        self.cell(colunas[1], linha, 'Hora:', align='L')
        self.cell(colunas[2], linha, 'Responsável:', align='L')
        self.cell(colunas[3], linha, cabecalho_fornecedor_tecnico, align='L')
        self.cell(colunas[4], linha, 'ID:', align='L')
        
        self.ln(0)
        self.set_font_size(10)
        linha = self.th * 3
        
        self.cell(colunas[0], linha, data, align='C', border=1)
        self.cell(colunas[1], linha, hora, align='C', border=1)
        self.cell(colunas[2], linha, responsavel, align='C', border=1)
        self.cell(colunas[3], linha, fornecedor_tecnico, align='C', border=1)
        self.cell(colunas[4], linha, str(self.ordem.id), align='C', border=1)

        self.ln(0)
        self.set_font_size(8)
        linha = self.th * 4.5

        self.cell(colunas[0] + colunas[1], linha, '', align='C')
        self.cell(colunas[2], linha, '(%s)' % responsavel_id, align='C')
        self.cell(colunas[3], linha, '(%s)' % fornecedor_tecnico_id, align='C')
            
    def tabela(self):

        colunas = [self.epw * .5, self.epw * .2, self.epw * .1, self.epw * .2]

        self.ln(self.th * 4)
        linha = self.th * 1.5

        self.cell(colunas[0], linha, 'Material', align='L', border=1)
        self.cell(colunas[1], linha, 'Código', align='C', border=1)
        self.cell(colunas[2], linha, 'Qtde', align='C', border=1)
        self.cell(colunas[3], linha, 'Check', align='C', border=1)

        if self.ordem.tipo == 0:
            materiais = MaterialEntrada.objects.filter(ordem=self.ordem)

        else:
            materiais = MaterialSaida.objects.filter(ordem=self.ordem)

        for material in materiais:
            self.ln(linha)
            if self.get_y() >= (self.h - 60):
                self.add_page()
            self.cell(colunas[0], linha, material.material.material, align='L', border=1)
            self.cell(colunas[1], linha, str(material.material.codigo), align='C', border=1)
            self.cell(colunas[2], linha, str(material.quantidade), align='C', border=1)
            self.cell(colunas[3], linha, '[     ]', align='C', border=1)

    def rodape(self):

        self.set_font_size(10)
        responsavel = self.ordem.user.first_name + ' ' + self.ordem.user.last_name
        tecnico = self.ordem.almoxarifado_ordem_saida.first().user_to.first_name + ' ' + \
            self.ordem.almoxarifado_ordem_saida.first().user_to.last_name
        self.line(self.l_margin * 2, self.h - 40, self.w/2 - self.r_margin, self.h - 40)
        self.line(self.w/2 + self.r_margin, self.h - 40, self.w - self.r_margin * 2, self.h - 40)
        self.set_xy(self.l_margin * 2, self.h - 40)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, 'Responsável', align='C')
        self.set_xy(self.l_margin * 2, self.h - 40 + self.th * 2)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, responsavel.title(), align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Colaborador', align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40 + self.th * 2)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, tecnico.title(), align='C')

    def file(self):

        return BytesIO(self.output(dest='S').encode('latin-1'))


class FichaOnts(FPDF):

    def __init__(self, ordem, format1='A4', unit='mm', orientation='P'):
        super().__init__(orientation, unit, format1)

        self.set_auto_page_break(False)
        self.ordem = ordem

        for i in range(2):
            self.add_page()
            self.set_font('Times', size=12)
            self.epw = self.w - 2 * self.l_margin
            self.th = self.font_size
            self.cabecalho()
            self.tabela()
            if self.ordem.tipo == 1:
                self.rodape()

    def cabecalho(self):

        cabecalho_texto = 'FICHA DE SAÍDA DE MATERIAIS DO ALMOXARIFADO'
        cabecalho_fornecedor_tecnico = 'Técnico:'
        fornecedor_tecnico = self.ordem.saida_ordem_ont.first().user_to.get_full_name().title()
        fornecedor_tecnico_id = self.ordem.saida_ordem_ont.first().user_to.username

        self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
        self.ln(self.th * 2)
        self.set_font_size(8)

        data = self.ordem.data.strftime('%d/%m/%Y')
        hora = self.ordem.data.strftime('%H:%M:%S')
        colunas = [self.epw * .15, self.epw * .15, self.epw * .3, self.epw * .3, self.epw * .1]
        responsavel = self.ordem.user.get_full_name().title()
        responsavel_id = self.ordem.user.username

        linha = self.th * .8

        self.cell(colunas[0], linha, 'Data:', align='L')
        self.cell(colunas[1], linha, 'Hora:', align='L')
        self.cell(colunas[2], linha, 'Responsável:', align='L')
        self.cell(colunas[3], linha, cabecalho_fornecedor_tecnico, align='L')
        self.cell(colunas[4], linha, 'ID:', align='L')

        self.ln(0)
        self.set_font_size(10)
        linha = self.th * 3

        self.cell(colunas[0], linha, data, align='C', border=1)
        self.cell(colunas[1], linha, hora, align='C', border=1)
        self.cell(colunas[2], linha, responsavel, align='C', border=1)
        self.cell(colunas[3], linha, fornecedor_tecnico, align='C', border=1)
        self.cell(colunas[4], linha, str(self.ordem.id), align='C', border=1)

        self.ln(0)
        self.set_font_size(8)
        linha = self.th * 4.5

        self.cell(colunas[0] + colunas[1], linha, '', align='C')
        self.cell(colunas[2], linha, '(%s)' % responsavel_id, align='C')
        self.cell(colunas[3], linha, '(%s)' % fornecedor_tecnico_id, align='C')

    def tabela(self):

        colunas = [self.epw * .3, self.epw * .2, self.epw * .3, self.epw * .2]

        self.ln(self.th * 4)
        linha = self.th * 1.5

        self.cell(colunas[0], linha, 'Modelo de ONT', align='L', border=1)
        self.cell(colunas[1], linha, 'Seção', align='L', border=1)
        self.cell(colunas[2], linha, 'Código', align='C', border=1)
        self.cell(colunas[3], linha, 'Check/Contrato', align='C', border=1)

        materiais = OntSaida.objects.filter(ordem=self.ordem)

        for material in materiais:
            self.ln(linha)
            if self.get_y() >= (self.h - 60):
                self.add_page()
            self.cell(colunas[0], linha, material.ont.modelo.nome, align='L', border=1)
            self.cell(colunas[1], linha, material.ont.secao.nome, align='L', border=1)
            self.cell(colunas[2], linha, str(material.ont.codigo), align='C', border=1)
            self.cell(colunas[3], linha, '', align='C', border=1)

    def rodape(self):

        self.set_font_size(10)
        responsavel = self.ordem.user.first_name + ' ' + self.ordem.user.last_name
        tecnico = self.ordem.saida_ordem_ont.first().user_to.first_name + ' ' + \
            self.ordem.saida_ordem_ont.first().user_to.last_name
        self.line(self.l_margin * 2, self.h - 40, self.w/2 - self.r_margin, self.h - 40)
        self.line(self.w/2 + self.r_margin, self.h - 40, self.w - self.r_margin * 2, self.h - 40)
        self.set_xy(self.l_margin * 2, self.h - 40)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, 'Responsável', align='C')
        self.set_xy(self.l_margin * 2, self.h - 40 + self.th * 2)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, responsavel.title(), align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Colaborador', align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40 + self.th * 2)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, tecnico.title(), align='C')

    def file(self):

        return BytesIO(self.output(dest='S').encode('latin-1'))


class FichaOntsDefeito(FPDF):

    def __init__(self, ordem, format1='A4', unit='mm', orientation='P'):
        super().__init__(orientation, unit, format1)

        self.set_auto_page_break(False)
        self.ordem = ordem

        for i in range(1):
            self.add_page()
            self.set_font('Times', size=12)
            self.epw = self.w - 2 * self.l_margin
            self.th = self.font_size
            self.cabecalho()
            self.tabela()
            if self.ordem.tipo == 1:
                self.rodape()

    def cabecalho(self):

        cabecalho_texto = 'FICHA DE DEVOLUÇÃO DE ONT\'S'
        cabecalho_fornecedor_tecnico = 'Fornecedor:'
        fornecedor_tecnico = str(self.ordem.devolucao_ordem_ont.first().fornecedor.nome)
        fornecedor_tecnico_id = str(self.ordem.devolucao_ordem_ont.first().fornecedor.cnpj)

        self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
        self.ln(self.th * 2)
        self.set_font_size(8)

        data = self.ordem.data.strftime('%d/%m/%Y')
        hora = self.ordem.data.strftime('%H:%M:%S')
        colunas = [self.epw * .15, self.epw * .15, self.epw * .3, self.epw * .3, self.epw * .1]
        responsavel = self.ordem.user.get_full_name().title()
        responsavel_id = self.ordem.user.username

        linha = self.th * .8

        self.cell(colunas[0], linha, 'Data:', align='L')
        self.cell(colunas[1], linha, 'Hora:', align='L')
        self.cell(colunas[2], linha, 'Responsável:', align='L')
        self.cell(colunas[3], linha, cabecalho_fornecedor_tecnico, align='L')
        self.cell(colunas[4], linha, 'ID:', align='L')

        self.ln(0)
        self.set_font_size(10)
        linha = self.th * 3

        self.cell(colunas[0], linha, data, align='C', border=1)
        self.cell(colunas[1], linha, hora, align='C', border=1)
        self.cell(colunas[2], linha, responsavel, align='C', border=1)
        self.cell(colunas[3], linha, fornecedor_tecnico, align='C', border=1)
        self.cell(colunas[4], linha, str(self.ordem.id), align='C', border=1)

        self.ln(0)
        self.set_font_size(8)
        linha = self.th * 4.5

        self.cell(colunas[0] + colunas[1], linha, '', align='C')
        self.cell(colunas[2], linha, '(%s)' % responsavel_id, align='C')
        self.cell(colunas[3], linha, '(%s)' % fornecedor_tecnico_id, align='C')

    def tabela(self):

        colunas = [self.epw * .3, self.epw * .2, self.epw * .3, self.epw * .2]

        self.ln(self.th * 4)
        linha = self.th * 1.5

        self.cell(colunas[0], linha, 'Modelo de ONT', align='L', border=1)
        self.cell(colunas[1], linha, 'Seção', align='L', border=1)
        self.cell(colunas[2], linha, 'Código', align='C', border=1)
        self.cell(colunas[3], linha, 'Check', align='C', border=1)

        materiais = OntDevolucao.objects.filter(ordem=self.ordem)

        for material in materiais:
            self.ln(linha)
            if self.get_y() >= (self.h - 60):
                self.add_page()
            self.cell(colunas[0], linha, material.ont.modelo.nome, align='L', border=1)
            self.cell(colunas[1], linha, material.ont.secao.nome, align='L', border=1)
            self.cell(colunas[2], linha, str(material.ont.codigo), align='C', border=1)
            self.cell(colunas[3], linha, '', align='C', border=1)

    def rodape(self):

        self.set_font_size(10)
        responsavel = self.ordem.user.first_name + ' ' + self.ordem.user.last_name
        tecnico = self.ordem.devolucao_ordem_ont.first().fornecedor.nome
        self.line(self.l_margin * 2, self.h - 40, self.w/2 - self.r_margin, self.h - 40)
        self.line(self.w/2 + self.r_margin, self.h - 40, self.w - self.r_margin * 2, self.h - 40)
        self.set_xy(self.l_margin * 2, self.h - 40)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, 'Responsável da Constel', align='C')
        self.set_xy(self.l_margin * 2, self.h - 40 + self.th * 2)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, responsavel.title(), align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Responsável do fornecedor', align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40 + self.th * 2)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, tecnico.title(), align='C')

    def file(self):

        return BytesIO(self.output(dest='S').encode('latin-1'))


class FichaOntsManutencao(FPDF):

    def __init__(self, ordem, format1='A4', unit='mm', orientation='P'):
        super().__init__(orientation, unit, format1)

        self.set_auto_page_break(False)
        self.ordem = ordem

        for i in range(1):
            self.add_page()
            self.set_font('Times', size=12)
            self.epw = self.w - 2 * self.l_margin
            self.th = self.font_size
            self.cabecalho()
            self.tabela()

    def cabecalho(self):

        self.set_font_size(10)
        # self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
        self.image('apps\\almoxarifado\\apps\\pdf\\assets\\copel_telecom.jpg', h=4*self.th, w=self.epw*.2)
        self.set_xy(self.epw*.2 + self.l_margin, self.t_margin)
        self.image('apps\\almoxarifado\\apps\\pdf\\assets\\titulo.jpg', h=4*self.th, w=self.epw*.5)
        self.set_xy(self.l_margin, self.t_margin)
        self.cell(h=4 * self.th, w=self.epw * .2, border=1)
        self.cell(h=4 * self.th, w=self.epw * .5, border=1)
        self.set_xy(self.epw * .7 + self.l_margin, self.t_margin)
        self.multi_cell(self.epw*.3, self.th, 'Copel Telecomunicações', align='L', border='LTR')
        self.set_xy(self.epw * .7 + self.l_margin, self.t_margin + self.th)
        self.multi_cell(self.epw*.3, self.th, 'R: José Izidoro Biazetto, 158', align='L', border='LR')
        self.set_xy(self.epw * .7 + self.l_margin, self.t_margin + self.th*2)
        self.multi_cell(self.epw * .3, self.th, 'Bloco A - Mossunguê', align='L', border='LR')
        self.set_xy(self.epw * .7 + self.l_margin, self.t_margin + self.th*3)
        self.multi_cell(self.epw * .3, self.th, 'Departamento de manutenção', align='L', border='LRB')

        self.th = self.th + 2

        self.cell(self.epw*.3, self.th, 'EMPRESA PARCEIRA', border=1)
        self.cell(self.epw*.7, self.th, 'Copel / Winikes Engenharia Elétrica LTDA (Constel)', border=1)
        self.ln(self.th)
        self.cell(self.epw * .3, self.th, 'RESPONSÁVEL', border=1)
        self.cell(self.epw * .7, self.th, f'Copel / {self.ordem.user.get_full_name().title()}', border=1)
        self.ln(self.th)
        self.cell(self.epw * .3, self.th, 'PERÍODO TRIAGEM', border=1)
        self.cell(self.epw * .35, self.th, f'DE: 01/{self.ordem.data.strftime("%m/%Y")}', border=1)
        self.cell(
            self.epw * .35,
            self.th,
            f'ATÉ: {monthrange(self.ordem.data.year, self.ordem.data.month)[1]}/{self.ordem.data.strftime("%m/%Y")}',
            border=1
        )
        self.ln(self.th)
        self.cell(self.epw * .3, self.th, 'IDENTIFICAÇÃO', border=1)
        self.cell(self.epw * .7, self.th, str(self.ordem.id), border=1)

    def tabela(self):

        materiais = OntSaida.objects.filter(ordem=self.ordem).order_by('ont__modelo__nome', 'ont__codigo')

        modelos = materiais.values(
            'ont__modelo__nome'
        ).annotate(
            quantidade=Count('ont')
        ).order_by(
            '-quantidade'
        )

        print(modelos)

        self.ln(2 * self.th)

        self.cell(self.epw*.25, self.th, 'Modelo de ONT', align='C', border=1)
        self.cell(self.epw*.25, self.th, 'Quantidade', align='C', border=1)
        self.ln(self.th)

        for modelo in modelos:
            self.cell(self.epw*.25, self.th, modelo['ont__modelo__nome'], align='C', border=1)
            self.cell(self.epw*.25, self.th, str(modelo['quantidade']), align='C', border=1)
            self.ln(self.th)

        colunas = [self.epw * .5, self.epw * .5]

        self.ln(self.th)

        self.cell(colunas[0], self.th, 'Modelo de ONT', align='C', border=1)
        self.cell(colunas[1], self.th, 'Serial', align='C', border=1)

        for material in materiais:
            self.ln(self.th)
            if self.get_y() >= (self.h - self.b_margin - 2*self.th):
                self.add_page()
            self.cell(colunas[0], self.th, material.ont.modelo.nome.upper(), align='C', border=1)
            self.cell(colunas[1], self.th, str(material.ont.codigo).upper(), align='C', border=1)

    def file(self):

        return BytesIO(self.output(dest='S').encode('latin-1'))
