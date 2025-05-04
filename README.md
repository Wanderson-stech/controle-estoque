Sistema de Controle de Estoque
Este projeto é um Sistema de Controle de Estoque desenvolvido com Python, utilizando o banco de dados SQLite para armazenar informações de usuários, produtos e logs. A aplicação possui uma interface gráfica construída com o Tkinter, permitindo que os usuários possam adicionar, visualizar e movimentar os produtos do estoque.

Funcionalidades
Login de usuários: Usuários podem fazer login com um nome de usuário e senha. O sistema tem um usuário admin padrão, com permissões especiais.

Cadastro de produtos: Permite adicionar novos produtos ao estoque.

Movimentação de estoque: Permite aumentar ou diminuir a quantidade de um produto no estoque.

Visualização do estoque: Exibe uma lista de todos os produtos com suas quantidades.

Logs de ações: Registra todas as ações realizadas (login, adição de produto, movimentações) para controle e auditoria.

Tecnologias Utilizadas
Python 3.x

Tkinter: Para a interface gráfica do usuário (GUI).

SQLite: Banco de dados local para armazenar usuários, produtos e logs.

Como Usar
1. Instalar Dependências
Este projeto utiliza apenas Python 3.x e a biblioteca Tkinter, que geralmente já vem instalada com o Python. Caso não tenha o Tkinter, instale-o utilizando:

bash
Copiar
Editar
pip install tk
2. Executar o Programa
Clone ou baixe o repositório.

Execute o arquivo principal:

bash
Copiar
Editar
python main.py
3. Login
Ao iniciar o programa, será exibida a tela de login. O usuário admin padrão é:

Usuário: admin

Senha: admin123

4. Funcionalidades da Tela Principal
Após o login, a tela principal exibirá as seguintes opções, dependendo do perfil do usuário (comum ou admin):

Adicionar Produto: Permite adicionar novos produtos ao estoque.

Visualizar Estoque: Exibe todos os produtos com suas respectivas quantidades.

Movimentar Estoque: Permite adicionar ou remover unidades de um produto específico.

Ver Logs: Exibido apenas para administradores, mostra os logs de ações realizadas.

5. Encerrando o Programa
Para sair da aplicação, basta clicar no botão Sair na tela principal.

Estrutura do Banco de Dados
O sistema utiliza um banco de dados SQLite com três tabelas principais:

usuarios: Armazena os dados dos usuários.

id: Identificador único do usuário.

username: Nome de usuário.

password: Senha do usuário.

perfil: Perfil do usuário (admin ou comum).

produtos: Armazena os dados dos produtos no estoque.

id: Identificador único do produto.

nome: Nome do produto.

quantidade: Quantidade em estoque.

logs: Armazena um histórico de ações realizadas no sistema.

id: Identificador único do log.

usuario: Usuário que realizou a ação.

acao: Descrição da ação realizada.

data: Data e hora da ação.

Funcionalidades Adicionais
Logs de Ação: Cada login, adição de produto e movimentação no estoque são registrados no banco de dados para controle.

Validação de Entrada: O sistema valida se os campos estão preenchidos corretamente, garantindo que não haja erros durante a execução.
