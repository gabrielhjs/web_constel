from fpdf import FPDF
from io import BytesIO


class FichaPatrimonio(FPDF):

    def __init__(self, data, format1='A4', unit='mm', orientation='P'):
        super().__init__(orientation, unit, format1)

        self.set_auto_page_break(False)
        self.data = data
        self.add_page()
        self.set_font('Times', size=12)
        self.epw = self.w - 2 * self.l_margin
        self.th = self.font_size
        self.cabecalho()
        self.tabela()
        self.rodape()
            
    def cabecalho(self):

        cabecalho_texto = 'FICHA DE ENTREGA DE PATRIMÔNIO'

        self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
        self.ln(self.th * 2)
        self.set_font_size(8)

        data = self.data.data.strftime('%d/%m/%Y')
        hora = self.data.data.strftime('%H:%M:%S')
        colunas = [self.epw * .15, self.epw * .15, self.epw * .3, self.epw * .3, self.epw * .1]
        responsavel = self.data.user.get_full_name().title()
        responsavel_id = self.data.user.username
        colaborador = self.data.user_to.get_full_name().title()
        colaborador_id = self.data.user_to.username
        
        linha = self.th * .8
        
        self.cell(colunas[0], linha, 'Data:', align='L')
        self.cell(colunas[1], linha, 'Hora:', align='L')
        self.cell(colunas[2], linha, 'Responsável:', align='L')
        self.cell(colunas[3], linha, 'Colaborador:', align='L')
        self.cell(colunas[4], linha, 'ID:', align='L')
        
        self.ln(0)
        self.set_font_size(10)
        linha = self.th * 3
        
        self.cell(colunas[0], linha, data, align='C', border=1)
        self.cell(colunas[1], linha, hora, align='C', border=1)
        self.cell(colunas[2], linha, responsavel, align='C', border=1)
        self.cell(colunas[3], linha, colaborador, align='C', border=1)
        self.cell(colunas[4], linha, str(self.data.id), align='C', border=1)

        self.ln(0)
        self.set_font_size(8)
        linha = self.th * 4.5

        self.cell(colunas[0] + colunas[1], linha, '', align='C')
        self.cell(colunas[2], linha, '(%s)' % responsavel_id, align='C')
        self.cell(colunas[3], linha, '(%s)' % colaborador_id, align='C')
            
    def tabela(self):

        colunas = [self.epw * .5, self.epw * .2, self.epw * .1, self.epw * .2]

        self.ln(self.th * 4)
        linha = self.th * 1.5

        self.cell(colunas[0], linha, 'Patrimônio', align='L', border=1)
        self.cell(colunas[1], linha, 'Código', align='C', border=1)
        self.cell(colunas[2], linha, 'Qtde', align='C', border=1)
        self.cell(colunas[3], linha, 'Check', align='C', border=1)

        self.ln(linha)
        if self.get_y() >= (self.h - 60):
            self.add_page()
        self.cell(colunas[0], linha, self.data.patrimonio.patrimonio.nome, align='L', border=1)
        self.cell(colunas[1], linha, str(self.data.patrimonio.codigo), align='C', border=1)
        self.cell(colunas[2], linha, str(1), align='C', border=1)
        self.cell(colunas[3], linha, '[     ]', align='C', border=1)

    def rodape(self):

        self.set_font_size(10)
        responsavel = self.data.user.get_full_name().title()
        colaborador = self.data.user_to.get_full_name().title()
        self.line(self.l_margin * 2, self.h - 40, self.w/2 - self.r_margin, self.h - 40)
        self.line(self.w/2 + self.r_margin, self.h - 40, self.w - self.r_margin * 2, self.h - 40)
        self.set_xy(self.l_margin * 2, self.h - 40)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, 'Responsável', align='C')
        self.set_xy(self.l_margin * 2, self.h - 40 + self.th * 2)
        self.cell(self.w/2 - self.r_margin * 3, self.th * 2, responsavel, align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Colaborador', align='C')
        self.set_xy(self.w/2 + self.r_margin, self.h - 40 + self.th * 2)
        self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, colaborador, align='C')

    def file(self):

        return BytesIO(self.output(dest='S').encode('latin-1'))
