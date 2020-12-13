from fpdf import FPDF
from io import BytesIO

from ..ferramenta.models import FerramentaSaida
from ..patrimonio1.models import PatrimonioSaida


class FichaPatrimonio(FPDF):

  def __init__(self, ordem_id, format1='A4', unit='mm', orientation='P'):
    super().__init__(orientation, unit, format1)

    self.set_auto_page_break(False)
    self.ordem_id = ordem_id
    self.add_page()
    self.set_font('Times', size=12)
    self.epw = self.w - 2 * self.l_margin
    self.th = self.font_size

    if FerramentaSaida.objects.filter(ordem__id=self.ordem_id).exists():
      self.ferramentas = FerramentaSaida.objects.filter(ordem__id=self.ordem_id)

    else:
      self.ferramentas = []

    if PatrimonioSaida.objects.filter(ordem__id=self.ordem_id).exists():
      self.patrimonios = PatrimonioSaida.objects.filter(ordem__id=self.ordem_id)

    else:
      self.patrimonios = []

    print(self.patrimonios)

    if self.ferramentas:
      self.data = self.ferramentas[0].data
      self.responsavel = self.ferramentas[0].user.get_full_name().title()
      self.responsavel_id = self.ferramentas[0].user.username
      self.colaborador = self.ferramentas[0].user_to.get_full_name().title()
      self.colaborador_id = self.ferramentas[0].user_to.username

    else:
      self.data = self.patrimonios[0].data
      self.responsavel = self.patrimonios[0].user.get_full_name().title()
      self.responsavel_id = self.patrimonios[0].username
      self.colaborador = self.patrimonios[0].user_to.get_full_name().title()
      self.colaborador_id = self.patrimonios[0].username

    self.cabecalho()
    self.termos_de_uso()
    self.tabelas()
    self.rodape()

  def cabecalho(self):

    cabecalho_texto = 'FICHA DE ENTREGA DE PATRIMÔNIO'

    self.cell(self.epw, self.th * 2, cabecalho_texto, align='C', border=1)
    self.ln(self.th * 2)
    self.set_font_size(8)

    data = self.data.strftime('%d/%m/%Y')
    hora = self.data.strftime('%H:%M:%S')
    colunas = [self.epw * .15, self.epw * .15, self.epw * .3, self.epw * .3, self.epw * .1]

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
    self.cell(colunas[2], linha, self.responsavel, align='C', border=1)
    self.cell(colunas[3], linha, self.colaborador, align='C', border=1)
    self.cell(colunas[4], linha, str(self.ordem_id), align='C', border=1)

    self.ln(0)
    self.set_font_size(8)
    linha = self.th * 4.5

    self.cell(colunas[0] + colunas[1], linha, '', align='C')
    self.cell(colunas[2], linha, '(%s)' % self.responsavel_id, align='C')
    self.cell(colunas[3], linha, '(%s)' % self.colaborador_id, align='C')

  def tabelas(self):
    self.ln(self.th * 4)
    linha = self.th * 1.5

    if self.ferramentas:

      colunas = [self.epw * .6, self.epw * .2, self.epw * .2]

      self.cell(colunas[0], linha, 'Ferramenta', align='L', border=1)
      self.cell(colunas[1], linha, 'Qtde', align='C', border=1)
      self.cell(colunas[2], linha, 'Check', align='C', border=1)
      self.ln(linha)

      for ferramenta in self.ferramentas:
        if self.get_y() >= (self.h - 60):
          self.add_page()
        self.cell(colunas[0], linha, ferramenta.ferramenta.nome, align='L', border=1)
        self.cell(colunas[1], linha, str(ferramenta.quantidade), align='C', border=1)
        self.cell(colunas[2], linha, '[     ]', align='C', border=1)
        self.ln(linha)

      self.ln(linha)

    if self.patrimonios:

      colunas = [self.epw * .6, self.epw * .2, self.epw * .2]

      self.cell(colunas[0], linha, 'Patrimônio', align='L', border=1)
      self.cell(colunas[1], linha, 'Código', align='C', border=1)
      self.cell(colunas[2], linha, 'Check', align='C', border=1)
      self.ln(linha)

      for patrimonio in self.patrimonios:
        if self.get_y() >= (self.h - 60):
          self.add_page()
        self.cell(colunas[0], linha, patrimonio.patrimonio.patrimonio.nome, align='L', border=1)
        self.cell(colunas[1], linha, str(patrimonio.patrimonio.codigo), align='C', border=1)
        self.cell(colunas[2], linha, '[     ]', align='C', border=1)
        self.ln(linha)

  def rodape(self):

    self.set_font_size(10)
    self.line(self.l_margin * 2, self.h - 40, self.w / 2 - self.r_margin, self.h - 40)
    self.line(self.w / 2 + self.r_margin, self.h - 40, self.w - self.r_margin * 2, self.h - 40)
    self.set_xy(self.l_margin * 2, self.h - 40)
    self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Responsável', align='C')
    self.set_xy(self.l_margin * 2, self.h - 40 + self.th * 2)
    self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, self.responsavel, align='C')
    self.set_xy(self.w / 2 + self.r_margin, self.h - 40)
    self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, 'Colaborador', align='C')
    self.set_xy(self.w / 2 + self.r_margin, self.h - 40 + self.th * 2)
    self.cell(self.w / 2 - self.r_margin * 3, self.th * 2, self.colaborador, align='C')

  def file(self):

    return BytesIO(self.output(dest='S').encode('latin-1'))

  def termos_de_uso(self):

    text = "Declaro para todos os fins de direito, conhecer as orientações contidas nesta Ficha de Entrega e " \
           "Controle de Equipamentos, Ferramentas, Uniformes e EPC. Recebi os equipamentos e/ou materiais, abaixo citados, gratuitamente em " \
           "conformidade com a legislação vigente (Portaria 3.214 do MTE, Art. 157 e 158, 166 e 167 da CLT, " \
           "Lei 6.514). Declaro ter sido treinado para o uso adequado dos Equipamentos, Ferramentas e EPC´s, " \
           "higienização, conservação e manutenção dos mesmos e que durante a execução do trabalho, atenderei as " \
           "normas internas e externas, procedimento, legislação vigente e orientação da Empresa. Estando assim, " \
           "de pleno acordo com as observações citadas abaixo:\n" \
           "a) Os Equipamentos, Ferramentas, Uniformes e EPC's deverão ser utilizados unicamente para a finalidade " \
           "a que se destinaram;\n" \
           "b) Responsabilizo-me integralmente pela guarda e conservação dos Equipamentos, Ferramentas, Uniformes e " \
           "EPC's que recebo;\n" \
           "c) Comunicar a Empresa, qualquer dano ou alteração que torne o equipamento impróprio para o uso, " \
           "para que possa receber outro;\n" \
           "d) Somente iniciar o serviço se estiver usando os Equipamentos, Ferramentas e EPC's indicado na tarefa " \
           "a realizar (Ordem de serviço, etc);\n" \
           "e) A falta de uso dos Equipamentos, Ferramentas, Uniformes e EPC's fornecidos pela Empresa constitui " \
           "em ato faltoso, sujeito a sanções disciplinares previstas na legislação (CLT Art. 482) e no regulamento " \
           "interno, aplicáveis ao assunto, inclusive à demissão por justa causa;\n" \
           "f) Responder perante a Empresa pelo custo integral, conforme previsto no paragrafo 1º do artigo 462 da " \
           "CLT, quando:\n" \
           "   1- Alegar perda ou extravio dos Equipamentos, Ferramentas, Uniformes e EPC's;\n" \
           "   2- Alterar o padrão recebido dos Equipamentos, Ferramentas, Uniformes e EPC's;\n" \
           "   3- Inutilizá-los por procedimento inadequado;\n" \
           "   4- Desligar-se da Empresa sem devolver os Equipamentos, Ferramentas, Uniformes e EPC's."

    self.ln(self.th * 4)
    self.multi_cell(self.epw, self.th, text, align="J")
