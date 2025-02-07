# Descrição

Este script foi desenvolvido para buscar informações de contato (emails e telefones) de entidades culturais a partir de uma planilha CSV. O processo é realizado através de uma busca no Google, seguida da análise das páginas encontradas, extraindo as informações de contato diretamente do texto da página.

O script começa buscando o nome da entidade cultural na planilha e, se as informações de contato (email ou telefone) estiverem faltando, ele tenta buscar essas informações em páginas relacionadas à entidade na web.

O script é projetado para lidar com a limitação de requisições (Rate Limit) e tentativas de reexibição de conteúdo, com várias tentativas e pausas entre as requisições, evitando sobrecarga nos servidores de destino.

### Funcionalidades

- **Busca no Google**: Utiliza o nome da entidade para realizar uma busca no Google e coletar links relevantes.
- **Extração de informações**: Analisa as páginas encontradas, extraindo emails e números de telefone utilizando expressões regulares.
- **Controle de Profundidade**: Limita a profundidade de navegação nos links encontrados, evitando sobrecarga no script e servidores.
- **Tolerância a falhas**: Reintenta as requisições e coleta as informações mesmo em caso de falhas temporárias de rede ou limitação de requisições (Rate Limit).
- **Atualização do CSV**: Atualiza a planilha CSV com as informações de contato encontradas.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `requests`: Para realizar as requisições HTTP.
  - `beautifulsoup4`: Para analisar e extrair informações de páginas HTML.
  - `re`: Para usar expressões regulares para capturar emails e números de telefone.
  - `pandas`: Para manipulação de arquivos CSV.
  
Você pode instalar as dependências utilizando o `pip`:

```bash
pip install -r requirements.txt
```

## Como usar

1. **Preparar os dados**: O script espera um arquivo CSV com as colunas `nome_entidade_coletivo_cultural`, `email_publico`, e `telefone_publico`. Essas colunas devem conter as informações das entidades culturais, sendo que o email e telefone podem estar ausentes ou com o valor "Não Informado".
   
   Exemplo de estrutura do CSV:
   ```csv
   nome_entidade_coletivo_cultural,email_publico,telefone_publico
   "Entidade 1", "Não Informado", "Não Informado"
   "Entidade 2", "contato@entidade2.com", "(83) 99999-9999"
   ```

2. **Rodar o script**: Execute o script Python. O script buscará as informações de contato para as entidades cuja coluna de `email_publico` ou `telefone_publico` estiverem faltando.

   ```bash
   python script.py
   ```

3. **Resultado**: O script criará um arquivo CSV chamado `updated_contacts.csv` com as informações de contato atualizadas. Este arquivo conterá as colunas `email_publico` e `telefone_publico` preenchidas com os novos dados coletados (se encontrados).

## Parâmetros

- **max_depth** (padrão: 4): Define a profundidade máxima de links a serem seguidos a partir da página de busca do Google.
- **retries** (padrão: 6): Número de tentativas para cada requisição falha (exemplo, erro de rede ou limitação de requisição).
- **delay** (padrão: 10 segundos): Tempo de espera entre tentativas de requisição, usado para evitar sobrecarga e limitações de requisição (Rate Limiting).
  
Esses parâmetros podem ser ajustados diretamente na função `fetch_contact_info` ou alterados diretamente no código.

## Funcionamento Interno

1. **Busca no Google**: O nome da entidade cultural é usado para fazer uma busca no Google por "nome da entidade contato". A busca é feita via requisição HTTP, e as URLs relevantes são extraídas dos resultados.
   
2. **Análise das páginas**: O script visita os links extraídos dos resultados da busca, faz requisições HTTP e utiliza o BeautifulSoup para extrair o texto da página. As expressões regulares são usadas para identificar emails e números de telefone no texto.

3. **Limitações e falhas**: O script implementa mecanismos para lidar com falhas, como requisições limitadas, erros de rede e timeouts, com tentativas automáticas.

## Exemplo de Execução

Suponha que você tenha o seguinte arquivo CSV (`dados.csv`):

```csv
nome_entidade_coletivo_cultural,email_publico,telefone_publico
"Teatro X", "Não Informado", "Não Informado"
"Orquestra Y", "orquestra@exemplo.com", "(83) 12345-6789"
```

Ao executar o script, se a entidade "Teatro X" tiver as informações de contato ausentes, o script buscará essas informações na web e atualizará a planilha. O arquivo de saída (`updated_contacts.csv`) seria gerado assim:

```csv
nome_entidade_coletivo_cultural,email_publico,telefone_publico
"Teatro X", "teatrox@contato.com", "(83) 98765-4321"
"Orquestra Y", "orquestra@exemplo.com", "(83) 12345-6789"
```

## Atenção

- **Uso responsável**: O script faz várias requisições HTTP, o que pode ser interpretado como scraping agressivo se não for utilizado com cautela. Use com responsabilidade e evite sobrecarregar os servidores de destino.
- **Limitações de acesso**: O Google pode aplicar limites de requisição (Rate Limit). Se o script falhar devido a isso, ele tentará novamente após um intervalo de tempo.

## Contato

Em caso de dúvidas ou problemas, entre em contato com o mantedor do repositorio.
