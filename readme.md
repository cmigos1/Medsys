
# Medsys

**Medsys** é um sistema de prontuário eletrônico desenvolvido com Django, projetado para auxiliar clínicas e consultórios na gestão de pacientes, consultas e registros médicos.

## 🩺 Funcionalidades

- Cadastro e gerenciamento de pacientes
- Registro de consultas e histórico médico
- Interface web responsiva utilizando templates HTML
- Banco de dados SQLite integrado
- Scripts para popular a base de dados com informações de exemplo

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Django
- HTML/CSS
- SQLite

## 📁 Estrutura do Projeto

```
Medsys/
├── clinica/           # Aplicativo para gestão de dados da clínica
├── prontuario/        # Aplicativo para registros médicos
├── templates/         # Templates HTML para a interface do usuário
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── db.sqlite3         # Banco de dados SQLite
├── manage.py          # Script de gerenciamento do Django
├── populate_db.py     # Script para popular o banco de dados
└── .vscode/           # Configurações do VSCode
```

## ⚙️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/cmigos1/Medsys.git
   cd Medsys
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. (Opcional) Popule o banco de dados com dados de exemplo:
   ```bash
   python populate_db.py
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

7. Acesse o sistema em: [http://localhost:8000](http://localhost:8000)

