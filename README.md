<h1 align="center">
  constel web
</h1>

<p align="center">
  <a href="#tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#tecnologias">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#almoxarifado">Almoxarifado</a>
</p>

<br>

## Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- [Python](https://www.python.org/)
- [Javascript](https://www.javascript.com/)
- [Django](https://www.djangoproject.com/)
- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [Heroku](https://www.heroku.com/)
- [Bootstrap](https://getbootstrap.com/)

Extras:

- [Selenium](https://www.selenium.dev/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

## Projeto
<p style="text-align: justify">
O <strong>constel web</strong> é um projeto que visa automatizar a gestão de processos. 
Atualmente o projeto atua em dois setores, são eles almoxarifado e patrimônio.
</p>

### Arquitetura

```
+---apps
|   +---almoxarifado
|   |   +---apps
|   |   |   +---cont
|   |   |   |   +---api
|   |   |   |   +---api2
|   |   |   +---lista_saida
|   |   |   +---pdf
|   +---patrimonio
|   |   +---apps
|   |   |   +---combustivel
|   |   |   |   +---apps
|   |   |   |   |   +---talao
|   |   |   +---ferramenta
|   |   |   +---patrimonio1
+---constel
|   +---apps
|   |   +---controle_acessos
+---staticfiles
+---venv_web_constel
\---web_constel
    +---settings
```

## Almoxarifado

<p style="text-align: justify">
Neste setor o sistema realiza a gestão completa dos materias, documentando todo seu fluxo
(entradas, estoque e saídas). O sistema apresenta consultas com intuito de facilitar o
controle aumentar o rendimento dos processos do setor. Além disso, o sistema conta com
um controle especial das <bold>ONT's</bold><sup>(1)</sup> com a aplicação <a href="#Cont2">Cont2</a>.
</p>

>**_ONT<sup>(1)</sup>_** (Optical Network Terminal) ou Terminal de Rede Óptica; são aparelhos são
>instalados em residências de desejam ter acesso a internet via fibra óptica.

### Cont2

<p style="text-align: justify">
Esta aplicação realiza a gestão completa e individual das ONT's que passam pelo almoxarifado,
isso inclui atividades como: entrada, estoque, saída, aplicação e devolução. O sistema utiliza uma aplicação externa 
para realizar <bold>web scraping</bold><sup>(2)</sup> utilizando o <bold>Selenium</bold><sup>(3)</sup> para realizar a
busca do local e sinal dos equipamentos em tempo real em um site de domínio de outra empresa. A comunicação com a
aplicação externa é realizadada através de web socket (consultas) e API (registros no banco de dados).
</p>

>**_Web scraping<sup>(2)</sup>_** Web Scraping é uma técnica utilizada para extrair rapidamente
>informações de sites e exportá-las para planilhas com o intuito de fazer análises e gerar insights
>para tomadas de decisão.
>(Fonte: [ResultadosDigitais](https://resultadosdigitais.com.br/blog/web-scraping/))

>**_Selenium<sup>(3)</sup>_** é um conjunto de ferramentas de código aberto multiplataforma, usado para
>testar aplicações web pelo browser de forma automatizada. Ele executa testes de funcionalidades da
>aplicação web e testes de compatibilidade entre browser e plataformas diferentes. O Selenium suporta
>diversas linguagens de programação, como por exemplo C#, Java e Python, e vários navegadores web como
>o Chrome e o Firefox.
>(Fonte: [TreinaWeb](https://www.treinaweb.com.br/blog/o-que-e-selenium/))

*continua...*

---

by **Gabriel Sá** | Analista de desenvolvimento

teste