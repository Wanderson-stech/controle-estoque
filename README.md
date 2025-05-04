# controle-estoque
Sistema de Controle de Estoque
Este projeto é um sistema simples de controle de estoque feito em Python, usando arquivos JSON para armazenar dados e um terminal interativo para gerenciar usuários e produtos.

Funcionalidades
Cadastro de usuários com perfis (admin e comum)

Autenticação de login

Cadastro e listagem de produtos

Registro de entradas e saídas no estoque

Logs de operações gravados em arquivo logs.txt

Pré-requisitos
Python 3 instalado no computador.
Verifique com:

bash
Copiar
Editar
python --version
Como rodar
Baixe os arquivos

Coloque todos os arquivos .py e .json (se precisar, os JSON vazios são só {}) na mesma pasta.

Instale bibliotecas necessárias
Não usamos nada externo, só as bibliotecas padrão. Então, não precisa instalar nada extra!

Rode o sistema
No terminal:

bash
Copiar
Editar
python nome_do_arquivo.py
Faça login
Use o usuário e senha padrão (se não mudou no código):

Usuário: admin

Senha: admin123

Como testar
Cadastrar produtos
→ Acesse com admin e escolha a opção de cadastrar produto.

Simular entrada/saída
→ Faça movimentações para ver o estoque mudando.

Checar os logs
→ Veja no arquivo logs.txt se os registros estão sendo gravados.

Criar novos usuários
→ Apenas admins podem criar outros usuários.

Estrutura dos arquivos
main.py → Código principal do sistema

users.json → Armazena usuários

products.json → Armazena produtos

logs.txt → Guarda histórico de operações
