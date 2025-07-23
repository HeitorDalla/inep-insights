<h1>Projeto Final ─ Analytics</h1>

<p align="justify">Este projeto teve como propósito consolidar e aplicar os conhecimentos adquiridos na capacitação em <b>Analytics</b> oferecida pela <code>Tata Consultancy Services</code>. Por meio da construção de pipelines de dados, da modularização do banco e do desenvolvimento de dashboards interativos, buscamos evidenciar as habilidades técnicas e a evolução profissional da equipe de desenvolvedores.</p>

<details>
    <summary>Entenda a persona</summary><br>
        <p align="justify"><b>Marta Oliveira</b>, 47 anos, é diretora de uma escola municipal em comunidade rural no município de Londrina-PR, com 20 anos de experiência na educação (8 deles como diretora) e formação em Pedagogia com especialização em Gestão Escolar.</p>
        <p align="justify">Ela enfrenta infraestrutura precária, baixo investimento público e, por consequência, desempenho comprometido de alunos e professores. Seu objetivo é construir, por meio de dashboards claros e comparativos (rural × urbano), uma narrativa baseada em dados oficiais do Censo Escolar para sensibilizar secretarias, ONGs e parceiros sobre a necessidade de políticas mais justas.</p>
</details>

<hr>

<h2>Tecnologias utilizadas</h2>
<ul>
  <li><strong>Python</strong> v3.13.5: Linguagem versátil que serve de base para todo o projeto, controlando fluxo e integração das bibliotecas.</li>
  <li><strong>NumPy</strong> v2.3.1: Oferece arrays rápidos e funções matemáticas vetorizadas para cálculos numéricos.</li>
  <li><strong>Pandas</strong> v2.3.1: Estrutura <i>DataFrame</i> que facilita carregar, limpar e explorar dados tabulares.</li>
  <li><strong>Plotly</strong> v6.2.0: Gera gráficos interativos que permitem explorar dados diretamente no navegador.</li>
  <li><strong>Streamlit</strong> v1.46.1: Transforma scripts Python em <i>dashboards web</i>.</li>
  <li><strong>streamlit-option-menu</strong> v0.4.0: Adiciona menus de navegação estilizados aos apps Streamlit.</li>
  <li><strong>MySQL</strong> v8.0.43: Banco de dados relacional que armazena e gerencia as informações do projeto.</li>
  <li><strong>mysql-connector-python</strong> v9.3.0: Conecta Python ao MySQL e executa consultas de forma direta.</li>
</ul>


<hr>

<h2>Estrutura do projeto</h2>

<pre>
PROJETO-FINAL/
├── .streamlit/
│   └── config.toml                     # configurações internas do Streamlit
├── csv/                      
│   └── ...¹
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css               # estilos globais da interface Streamlit
│   │   └── img/                        # imagem(ns) da interface do Streamlit
│   │       └── ...
│   ├── utils/                          # módulo de funções:
│   │   ├── filters.py                  # SQL para criação de filtros          
│   │   ├── formatters.py               # formata números em suas unidades de medidas (mil, milhões, etc.)
│   │   ├── graficos.py                 # plota gráficos
│   │   └── load_css.py                 # carrega o style.css
│   ├── views/
│   │   ├── analise_especifica_past/    # módulo de dashboards comparativos interativos
│   │   │   ├── corpo_docente.py
│   │   │   ├── infraestrutura.py
│   │   │   ├── material.py
│   │   │   └── saneamento_basico.py
│   │   ├── analise_especifica.py       # seção de dashboards interativos para análise comparativa dos dados
│   │   ├── analise_exploratoria.py     # integra submódulos de análise específica e apresenta dashboards comparativos em sua seção dedicada
│   │   ├── analise_geral.py            # seção de dashboards interativos para análise exploratória dos dados
│   └── app.py                          # script central que reúne e exibe todas as views modularizadas no Streamlit
├── src/
│   ├── data/                           # módulo de scripts resposável pelo ETL
│   │   ├── dados_tratados.py
│   │   └── data.py
│   └── database/                       # módulo de scripts que conecta, cria e popula o banco de dados
│       ├── create_database.py          # módulo de criação de todas as dimensões do banco de dados
│       ├── get_connection.py           # módulo que faz a conexão com o banco de dados
│       ├── inicializar_database.py     # módulo que faz a conexão, criação e população dos dados
│       └── populate_database.py        # módulo que faz a população dos dados
└── main.py                             # script central que processa dados, gera e popula o banco de dados
</pre>

<p align="justify">Alguns arquivos e diretórios foram omitidos por não serem essenciais para entendimento da estrutura do projeto.</p>
<p align="justify">1 ─ O <em>dataset</em> não está disponível no <i>GitHub</i> devido ao seu tamanho elevado. Contudo, é possível baixá‑lo diretamente por meio do seguinte link: <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar" target="_blank">www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar</a>.</p>

<hr>

<h2>Funcionalidades</h2>

<h3>Streamlit Menu</h3>
<img src="./frontend/assets/img/menu.gif" alt="texto alternativo"/>
<ul>
  <li><strong>About</strong>: Exibe a lista dos desenvolvedores da aplicação e o link para o site oficial do Streamlit.</li>
  <li><strong>Get Help</strong>: Redireciona o usuário para a documentação do projeto (GitHub correspondente).</li>
  <li><strong>Report a Bug</strong>: Envia o usuário diretamente à seção de “Issues” do GitHub.</li>
</ul>

<h3>Análise Exploratória</h3>
<img src="./frontend/assets/img/anal-exploratoria.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de região, estado e município, com opção “Todos”.</li>
  <li><strong>KPIs dinâmicos</strong>: total de escolas, matrículas, média de profissionais por escola e número de escolas com água potável, alimentação e internet.</li>
  <li><strong>Heatmap de correlação</strong>: mostra o coeficiente de Pearson entre as principais variáveis.</li>
  <li><strong>Guia interativo</strong>: painel expansível que orienta sobre a interpretação do heatmap.</li>
</ul>


<h3>Análise Geral</h3>
<img src="./frontend/assets/img/anal-geral.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de regiãoe e estado, com opção “Todos”.</li>
  <li><strong>Gráfico de velocímetro:</strong> compara score (infraestrutura + saneamento) rural vs urbano, com zonas de criticidade e indicador de gap coloridas.</li>
  <li><strong>KPIs dinâmicos:</strong> quantidades e percentuais de escolas e matrículas rurais e urbanas;</li>
  <li><strong>Gráficos de barras lado a lado:</strong> percentuais de escolas com infraestrutura e saneamento por localização.</li>
  <li><strong>Distribuição de matrículas:</strong> gráfico de barras comparando níveis de ensino (educação infantil, fundamental, médio, etc.) entre rural e urbano;</li>
  <li><strong>Dispersão entre infraestrutura e densidade de matrículas:</strong> scatter plot mostrando relação entre infraestrutura e número de matrículas por localização.</li>
  <li><strong>Boxplot de profissionais:</strong> distribuição do total de profissionais em áreas rurais e urbanas;</li>
  <li><strong>Insights dinâmicos:</strong> observações geradas conforme filtros aplicados;</li>
  <li><strong>Explicações interativas:</strong> expanders embaixo de cada gráfico detalhando interpretação.</li>
</ul>


<h3>Análise Específica ─ Saneamento Básico</h3>
<img src="./frontend/assets/img/anal-espc-saneamento.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de região, estado, município e tipo de localização (Rural/Urbana).</li>
  <li><strong>Indicador da Escola de Marta:</strong> KPI "Sim"/"Não" para o saneamento selecionado via dropdown.</li>
  <li><strong>Comparativo Rural vs Urbano:</strong> gráfico de barras lado a lado usando o mesmo filtro de saneamento.</li>
</ul>

<h3>Análise Específica ─ Infraestrutura</h3>
<img src="./frontend/assets/img/anal-espc-infraestrutura.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de região, estado, município e tipo de localização (Rural/Urbana).</li>
  <li><strong>Indicador da Escola de Marta:</strong> KPI "Sim"/"Não" para a infraestrutura selecionada via dropdown.</li>
  <li><strong>Comparativo Rural vs Urbano:</strong> gráfico de barras lado a lado usando o mesmo filtro de infraestrutura.</li>
  <li><strong>Gráficos de transporte escolar público (infraestrutura):</strong>
    <ul>
      <li><strong>Escola de Marta:</strong> número de alunos usando transporte escolar público.</li>
      <li><strong>Boxplot:</strong> dispersão do uso de transporte entre rural e urbano.</li>
      <li><strong>Histograma de frequência:</strong> quantidade de escolas por número de alunos usuários, comparando rural e urbano.</li>
    </ul>
  </li>
</ul>

<h3>Análise Específica ─ Materiais</h3>
<img src="./frontend/assets/img/anal-espc-material.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de região, estado, município e tipo de localização (Rural/Urbana).</li>
  <li><strong>Explicação interativa:</strong> expander ao início da página descrevendo quais materiais estão avaliados.</li>
  <li><strong>Indicador da Escola de Marta:</strong> KPI "Sim"/"Não" para o material selecionado via dropdown.</li>
  <li><strong>Comparativo Rural vs Urbano:</strong> gráfico de barras lado a lado usando o mesmo filtro de material.</li>
</ul>

<h3>Análise Específica ─ Corpo Docente</h3>
<img src="./frontend/assets/img/anal-espc-corpo-docente.gif" alt="texto alternativo"/>
<ul>
  <li><strong>Filtros em cascata</strong>: seleção hierárquica de região, estado, município e tipo de localização (Rural/Urbana).</li>
  <li><strong>Visão geral dos profissionais:</strong> expander inicial com detalhes dos profissionais selecionados.</li>
  <li><strong>Comparativo por profissional:</strong>
    <ul>
      <li><strong>Gráfico de barras esquerdo:</strong> número na Escola de Marta e média em áreas rural e urbana, conforme o profissional escolhido.</li>
      <li><strong>Gráfico de barras direito:</strong> média de profissionais nas três localizações (escola de Marta exibe valor total).</li>
    </ul>
  </li>
  <li><strong>Distribuição e médias gerais:</strong>
    <ul>
      <li><strong>Gráfico de pizza:</strong> distribuição percentual de profissionais na Escola de Marta.</li>
      <li><strong>Gráfico de barras:</strong> média de profissionais em rural vs. urbano.</li>
    </ul>
  </li>
  <li><strong>Relação segurança vs. total de profissionais:</strong> gráfico de disperção mostrando correlação entre número de profissionais de segurança e o total nas três localizações.</li>
  <li><strong>Explicação interativa:</strong> expander ao final, orientando a interpretação do gráfico de relação.</li>
</ul>

<hr>

<h2>Como rodar esse projeto em seu ambiente</h2>

<h3>Pré‑requisitos:</h3>
<ul>
  <li><strong>Python ≥ 3.8</strong> (recomendado 3.13.3)</li>
  <li><strong>Git</strong> instalado</li>
  <li><strong>pip</strong> (gerenciador de pacotes Python)</li>
  <li><strong>MySQL</strong> instalado e em execução</li>
  <li><strong>Navegador moderno</strong> (Chrome, Firefox, Edge etc.)</li>
</ul>

<h3>Passo a passo:</h3>
<ol>
  <li>
    <strong>Instalar o Git</strong><br>
    <ul>
      <li><b>Windows:</b> baixe em <a href="https://git-scm.com/downloads" target="_blank">git-scm.com/downloads</a> e execute o instalador.</li>
      <li><b>macOS:</b> abra o Terminal e rode <code>brew install git</code> (via Homebrew).</li>
      <li><b>Linux:</b> use <code>sudo apt update && sudo apt install git</code> (Debian/Ubuntu) ou o gerenciador da sua distro.</li>
    </ul>
    Verifique com:  
    <pre><code>git --version</code></pre>
  </li><br>

  <li>
    <strong>Clonar o repositório</strong><br>
    <pre><code>git clone https://github.com/HeitorDalla/projeto-final.git
cd caminho/do/diretorio</code></pre>
  </li><br>

  <li>
    <strong>Criar e ativar ambiente virtual</strong><br>
    <pre><code>python -m venv venv</code></pre>
    <strong>Linux/macOS:</strong>  
    <pre><code>source venv/bin/activate</code></pre>
    <strong>Windows (PowerShell):</strong>  
    <pre><code>.\venv\Scripts\Activate.ps1</code></pre>
  </li><br>

  <li>
    <strong>Instalar dependências</strong><br>
    <pre><code>pip install -r requirements.txt</code></pre>
    (Confira <code>requirements.txt</code> para mais detalhes.)  
  </li><br>

  <li>
    <strong>Instalar e iniciar o MySQL</strong><br>
    <ul>
      <li><em>Windows:</em> baixe o MySQL Installer em <a href="https://dev.mysql.com/downloads/installer/" target="_blank">dev.mysql.com</a> e siga o assistente.</li>
      <li><em>macOS:</em> instale via Homebrew: <code>brew install mysql</code> e depois <code>brew services start mysql</code>.</li>
      <li><em>Linux:</em> em Debian/Ubuntu: <code>sudo apt update && sudo apt install mysql-server</code>, em seguida <code>sudo systemctl start mysql</code>.</li>
    </ul>
    Verifique com:  
    <pre><code>mysql --version</code></pre>
  </li><br>

  <li>
    <strong>Configurar credenciais no get_connection.py</strong><br>
    Abra o arquivo <code>database/get_connection.py</code> e atualize as variáveis:
    <pre><code>HOST = "localhost"
USER = "seu_usuario"
PASSWORD = "sua_senha"
DATABASE = "nome_do_banco"</code></pre>
  </li><br>

  <li>
    <strong>Inicializar e popular o banco de dados</strong><br>
    Na raiz do projeto, execute:
    <pre><code>python main.py</code></pre>
    Este script criará o banco de dados local.
  </li><br>

  <li>
    <strong>Executar o Streamlit</strong><br>
    Ainda com o ambiente virtual ativado, rode:
    <pre><code>streamlit run frontend/app.py</code></pre>
  </li><br>

  <li>
    <strong>Acessar no navegador</strong><br>
    O Streamlit abrirá automaticamente. Se não, visite:
    <pre><code>http://localhost:8501</code></pre>
  </li>
</ol>

<hr>

<h2>⚠️ Importante</h2>

<p align="justify">
Este projeto utiliza dados públicos reais disponibilizados pelo <a href="https://www.gov.br/inep/pt-br" target="_blank">Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira</a> (INEP), provenientes de fontes oficiais como o <a href="https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar" target="_blank">Censo Escolar</a>.<br><br>
Ressaltamos que não são utilizados dados sensíveis, pessoais ou que possam ferir a privacidade, integridade ou reputação de indivíduos ou instituições. Todas as informações tratadas são de domínio público e foram utilizadas estritamente com fins educacionais, analíticos e de interesse coletivo.<br><br>
Portanto, assegura-se que nenhuma informação apresentada representa risco à segurança física ou digital de qualquer pessoa ou organização.
</p>

<hr>

<h2>Contribuições</h2>
<p align="justify">Este projeto está aberto para contribuições via <i>issues</i>. Se você encontrou um <i>bug</i>, deseja sugerir uma melhoria ou tem dúvidas sobre o funcionamento, siga as instruções abaixo:</p>
<ol>
    <li>Verifique se já existe uma <i>issue</i> sobre o assunto. Caso sim, adicione um comentário nela.</li>
    <li>Se não houver, abra uma nova <i>issue</i> com uma descrição clara e objetiva.</li>
</ol>

<hr>

<h2>Licença e Autoria</h2>
<p align="justify">Este projeto foi desenvolvido por <a href="https://www.linkedin.com/in/dev-matheusvn/">Matheus Nellessen</a>, <a href="https://www.linkedin.com/in/fl%C3%A1vialuisa/">Flávia Luisa</a> e <a href="https://www.linkedin.com/in/heitordallavilla/">Heitor Dalla</a>, e está licenciado sob a licença MIT. Veja o <a href="./LICENSE">documento</a> para mais detalhes.</p>
