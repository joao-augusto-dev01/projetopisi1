# LinkShield

## Descrição
Este é um aplicativo em Python para validar URLs e números de telefone, armazenar histórico de URLs e telefones validados, bem como gerenciar cadastros de e-mails e senhas. O 
sistema também permite adicionar e remover URLs e números de telefone de arquivos externos.

## Funcionalidades
- **Cadastro de Email e Senha**: Permite registrar credenciais e armazená-las em um dicionário.
- **Validação de URLs**: Verifica se uma URL pertence a uma lista segura e categoriza o tipo de serviço.
- **Validação de Telefones**: Confere se um número de telefone segue um formato correto e verifica DDDs.
- **Gerenciamento de URLs e Telefones**:
  - Adição de URLs seguras em um arquivo.
  - Remoção de URLs do arquivo.
  - Adição e remoção de números de telefone.
- **Histórico de Validações**:
  - Visualização do histórico de URLs e telefones validados.
  - Limpeza do histórico de URLs e telefones.
- **Visualização de URLs Disponíveis**: Exibe a lista de URLs categorizadas no sistema.

## Tecnologias Utilizadas
- **Python 3**
- **Módulos:**
  - `os` para manipulação do terminal.
  - `re` para expressões regulares na validação de emails e telefones.
  - `pydantic` para validação de URLs.
  - `urllib.parse` para manipulação de URLs.

## Como Executar o Projeto
1. Certifique-se de ter o **Python 3** instalado em seu sistema.
2. Instale a dependência `pydantic`, se ainda não tiver instalada:
   ```sh
   pip install pydantic
   ```
3. Salve o código em um arquivo Python (ex: `validador.py`).
4. Execute o programa no terminal ou prompt de comando:
   ```sh
   python validador.py
   ```

## Estrutura do Projeto
```
/
|-- validador.py  # Arquivo principal do código
|-- urls.txt      # Arquivo contendo URLs adicionadas manualmente
|-- numeros.txt   # Arquivo contendo números de telefone adicionados
```

## Possíveis Melhorias Futuras
- Implementação de interface gráfica (GUI) para maior usabilidade.
- Integração com APIs de segurança para verificar URLs maliciosas.
- Armazenamento de cadastros em um banco de dados.
- Expansão das categorias de URLs seguras.

## Autor
Desenvolvido por [João Augusto].

