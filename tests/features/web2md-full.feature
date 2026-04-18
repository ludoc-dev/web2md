# language: pt
# encoding: utf-8
Feature: Extração de Conteúdo Web com web2md
  Como desenvolvedor precisando extrair conteúdo web
  Quero converter páginas HTML em Markdown limpo
  Para alimentar LLMs com contexto otimizado (90% economia tokens)

  Critérios de Aceitação (baseados em pesquisa):
  - Extração bem-sucedida de conteúdo principal
  - Remoção de ruído (ads, navbars, sidebars)
  - Preservação de estrutura (headers, lists, links)
  - Formato Markdown válido
  - Performance aceitável (<5s para páginas simples)

  Background:
    Dado que estou no diretório do projeto web2md
    E que web2md está instalado

  @P1 @critical
  Cenário: Extração de artigo simples
    Dado que acesso uma URL de artigo simples
    Quando executo web2md na URL
    Então devo receber Markdown limpo
    E tempo de processamento < 5s
    E economia de tokens > 85%

    Exemplos:
      | URL                          | Resultado esperado                      |
      | https://example.com          | Markdown com conteúdo, sem ruído         |
      | https://httpbin.org/html     | Markdown com HTML convertido            |

  @P1 @critical
  Cenário: Remoção de ruído
    Dado que acesso página com elementos de ruído
    Quando executo web2md
    Então Markdown não deve conter elementos de ruído
    E apenas conteúdo principal deve estar presente

    Exemplos:
      | Elemento          | Resultado esperado   |
      | Ads               | Ausente do Markdown  |
      | Navbar           | Ausente do Markdown  |
      | Sidebar          | Ausente do Markdown  |
      | Footer           | Ausente do Markdown  |
      | Conteúdo principal | Presente no Markdown  |

  @P1 @critical
  Cenário: Preservação de estrutura
    Dado que acesso página com formatação complexa
    Quando executo web2md
    Então Markdown deve ter estrutura equivalente
    E formatação deve ser válida

    Exemplos:
      | Elemento HTML     | Resultado esperado         |
      | <h1>Título</h1>    | # Título                  |
      | <h2>Subtítulo</h2> | ## Subtítulo              |
      | <ul><li>Item</li></ul> | - Item                 |
      | <code>code</code> | `code`                     |
      | <a href="#">Link</a> | [Link](#)                |

  @P2 @javascript
  Cenário: Extração de página com JavaScript
    Dado que acesso uma URL de SPA
    Quando executo web2md com flag --js
    Então devo receber conteúdo renderizado
    E tempo de processamento < 10s

    Exemplos:
      | URL                        | Resultado esperado                         |
      | https://example.com/spa     | Markdown com conteúdo JS renderizado        |

  @P2 @economy
  Cenário: Economia de tokens
    Dado que página HTML tem aproximadamente 15.000 tokens
    Quando executo web2md
    Então Markdown resultante deve ter < 1.500 tokens
    E economia deve ser > 85%

  @P2 @structure
  Cenário: Preservação de code blocks
    Dado que página contém code blocks
    Quando executo web2md
    Então code blocks devem ser preservados
    E linguagem deve ser identificada

    Exemplos:
      | Código                           | Resultado esperado        |
      | <pre><code>def hello():</code></pre> | ```python\ndef hello():``` |
      | <code>console.log()</code>       | `console.log()`            |

  @P2 @links
  Cenário: Preservação de links
    Dado que página contém links
    Quando executo web2md
    Então links devem ser convertidos para formato Markdown

    Exemplos:
      | Link HTML                              | Markdown esperado          |
      | <a href="https://example.com">Link</a> | [Link](https://example.com) |
      | <a href="/internal">Interno</a>        | [Interno](/internal)        |

  @P3 @performance
  Cenário: Performance de extração
    Dado que acesso página simples
    Quando executo web2md
    Então processamento deve completar em < 5s
    E uso de memória deve ser razoável

  @P3 @output
  Cenário: Saída para arquivo
    Dado que especifico arquivo de saída
    Quando executo web2md com flag --out
    Então Markdown deve ser salvo no arquivo
    E arquivo deve ser válido

    Exemplos:
      | Arquivo saída | Resultado                              |
      | output.md     | Arquivo criado com Markdown válido     |
      | /tmp/test.md  | Arquivo criado no path especificado    |

  @P3 @piping
  Cenário: Pipe para outras ferramentas
    Dado que executo web2md sem --out
    Quando output é redirecionado
    Então Markdown deve ser impresso em stdout
    E pode ser usado em pipes

  @P3 @error_handling
  Cenário: Tratamento de erros
    Dado que acesso URL inválida
    Quando executo web2md
    Então erro deve ser reportado em stderr
    E código de saída deve ser não-zero

    Exemplos:
      | URL              | Resultado esperado           |
      | not-a-url        | Erro de URL inválida         |
      | https://404.example | Erro de conexão          |
