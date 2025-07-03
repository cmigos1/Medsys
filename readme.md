# Medsys - Sistema de Gestão de Clínicas

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-3.2%2B-green.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-lightgrey.svg)

O **Medsys** é um sistema de gestão de clínicas e consultórios médicos, desenvolvido em Django, que visa otimizar e organizar o fluxo de trabalho de profissionais da saúde. A plataforma permite o gerenciamento completo de pacientes, agendamentos, prontuários eletrônicos e muito mais, com uma interface intuitiva e segura.

## Funcionalidades Principais

O sistema conta com três níveis de acesso, cada um com suas próprias funcionalidades:

### Administrador
- **Dashboard completo:** Visualização de todas as métricas do sistema, como total de pacientes, médicos, consultas do dia e prontuários.
- **Gestão de Pacientes:** Cadastro, edição e visualização de todos os pacientes da clínica.
- **Gestão de Consultas:** Acesso a todas as consultas, podendo agendar, editar, cancelar e confirmar.
- **Gestão de Prontuários:** Acesso a todos os prontuários registrados no sistema.
- **Painel de Administração do Django:** Acesso completo ao painel de administração para gerenciamento de usuários, especialidades, médicos e outros dados do sistema.

### Médico
- **Dashboard personalizado:** Métricas focadas em suas atividades, como total de pacientes atendidos, consultas do dia, pacientes em espera e total de prontuários criados.
- **Minhas Consultas:** Visualização e gerenciamento apenas das suas consultas.
- **Meus Prontuários:** Cadastro, edição e visualização apenas dos prontuários de suas consultas.
- **Agenda:** Visualização da sua agenda de consultas.
- **Impressão de Prontuários:** Geração de uma versão para impressão do prontuário do paciente.

### Recepcionista
- **Dashboard focado na recepção:** Métricas como total de pacientes, consultas do dia, consultas pendentes e médicos ativos.
- **Gestão de Pacientes:** Cadastro, edição e visualização de todos os pacientes da clínica.
- **Gestão de Consultas:** Acesso a todas as consultas, podendo agendar, editar, cancelar e confirmar.
- **Agenda:** Visualização da agenda completa da clínica.

## Tecnologias Utilizadas

- **Backend:** Python com o framework Django
- **Frontend:** HTML5, CSS3, Bootstrap 5 e JavaScript
- **Banco de Dados:** SQLite (configuração padrão, mas pode ser alterado)
- **Controle de Versão:** Git e GitHub

## Instalação e Execução

Para executar o projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/cmigos1/Medsys.git](https://github.com/cmigos1/Medsys.git)
    cd Medsys
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário (administrador):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

7.  Acesse o sistema em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Papéis e Permissões dos Usuários

-   **Administrador:** Tem acesso irrestrito a todas as funcionalidades do sistema.
-   **Médico:** Acessa apenas os dados de seus pacientes e consultas, garantindo a privacidade e a segurança das informações.
-   **Recepcionista:** Gerencia o fluxo de pacientes e agendamentos, mas não tem acesso aos detalhes clínicos dos prontuários.

