# language: pt
# encoding: utf-8
Feature: Extração de Conteúdo Web com web2md
  Como desenvolvedor precisando extrair conteúdo web
  Quero converter páginas HTML em Markdown limpo
  Para alimentar LLMs com contexto otimizado (90% economia tokens)

  Critérios de Aceitação:
  - Extração bem-sucedida de conteúdo principal
  - Remoção de ruído (ads, navbars, sidebars)
  - Preservação de estrutura (headers, lists, links)
  - Formato Markdown válido
  - Performance aceitável (<5s para páginas simples)

  Cenário: Extração de artigo simples
    Dado que acesso uma URL de artigo
    Quando executo web2md na URL
    Então devo receber Markdown limpo
    E tempo de processamento < 5s

    Exemplos:
      | URL                          | Resultado esperado                      |
      | https://example.com/article    | Markdown com artigo, sem ruído         |
      | https://blog.example.com/post    | Markdown com post, preservar formatação |
      | https://docs.example.com/guide   | Markdown com docs, estrutura mantida   |

  Cenário: Extração de página com JavaScript
    Dado que acesso uma URL de SPA
    Quando executo web2md com --js
    Então devo receber conteúdo renderizado
    E tempo de processamento < 10s

    Exemplos:
      | URL                        | Resultado esperado                         |
      | https://spa.example.com     | Markdown com conteúdo JS renderizado        |
      | https://app.example.com     | Markdown com dados dinâmicos extraídos    |

  Cenário: Extração de documentação oficial
    Dado que preciso de documentação atualizada
    Quando acesso docs oficiais (Anthropic, OpenAI)
    Quando executo web2md --js
    Então devo receber docs completas
    E tamanho 90% menor que HTML original

    Exemplos:
      | URL                                          | Resultado esperado                          |
      | docs.anthropic.com/en/api/getting-started    | Markdown com docs, 90% economia de tokens |
      | platform.openai.com/docs/introduction      | Markdown com docs, estrutura preservada     |

  Cenário: Remoção de ruído
    Dado que acesso página com ads e navegação
    Quando executo web2md
    Então devo receber Markdown limpo
    E sem elementos de ruído

    Exemplos:
      | Elemento          | Resultado esperado   |
      | Ads               | Ausente do Markdown  |
      | Navbar           | Ausente do Markdown  |
      | Sidebar          | Ausente do Markdown  |
      | Footer           | Ausente do Markdown  |
      | Conteúdo principal | Presente no Markdown  |

  Cenário: Preservação de estrutura
    Dado que acesso página com formatação complexa
    Quando executo web2md
    Então devo receber Markdown estruturado
    E headers, lists, code blocks preservados

    Exemplos:
      | Elemento HTML     | Resultado esperado         |
      | <h1>Título</h1>    | # Título                  |
      | <ul><li>Item</li></ul> | - Item                     |
      | <code>code</code> | `code`                     |
      | <a href="#">Link</a> | [Link](#)                |
