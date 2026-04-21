# 🎵 Maestro - Conexões Musicais

O **Maestro** é uma aplicação web desenvolvida como projeto integrador do SENAC TECH, com o objetivo de conectar alunos, professores e escolas em um ambiente digital de ensino musical.

Inspirado em plataformas como o Google Classroom, o sistema permite o gerenciamento de turmas, compartilhamento de materiais e interação entre os usuários de forma simples e organizada.

---

## 🌐 Preview do Sistema
<img width="1352" height="601" alt="image" src="https://github.com/user-attachments/assets/2fe62539-9f34-4bde-9b2b-d1d3b62b25b4" />

---

## 🚀 Funcionalidades

* **Autenticação** — Login seguro para alunos, professores e escolas
* **Gerenciamento de Turmas** — Criar, organizar e gerenciar turmas por escola
* **Vinculação de Usuários** — Alunos conectam-se a escolas e turmas; professores associados às turmas
* **Publicação de Materiais** — Professores compartilham títulos, descrições, arquivos e datas de envio
* **Download de Materiais** — Alunos visualizam e fazem download dos materiais das turmas
* **Upload de Arquivos** — Sistema completo de upload com armazenamento em pasta dedicada
* **Consulta de Pessoas** — Visualização de professores e alunos por turma
* **Geolocalização de Escolas** — Mapa interativo com localização (latitude/longitude) das instituições
* **Sistema de Testes** — Testes E2E e unitários para validação de qualidade

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python (Flask)
* **Banco de Dados:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript
* **Mapas:** Leaflet
* **Testes:** Pytest
* **Design:** Figma (UI/UX)

---

## 📂 Estrutura do Projeto

```
pi-joao-pedro/
├── app.py                 # Aplicação Flask com rotas web
├── service.py             # Lógica de negócio (orquestração)
├── model.py               # Camada de dados (queries SQLite)
├── BANCO.py               # Schema do banco de dados
├── inserts.py             # Seed com dados de população inicial
├── pytest.ini             # Configuração de testes
├── static/
│   ├── style.css          # Estilos da aplicação
│   ├── img/               # Imagens e assets
│   └── uploads/           # Arquivos enviados por professores
├── templates/             # Páginas HTML
│   ├── index.html
│   ├── login.html
│   ├── cadastrar.html
│   ├── escola.html
│   ├── conexao_escola.html
│   ├── turmas.html
│   ├── turma_pessoas.html
│   └── professor.html
├── tests/
│   └── test_service.py    # Testes unitários
├── E2E/
│   └── test_frontend.py   # Testes end-to-end
└── README.md
```

### Descrição dos Arquivos Python

| Arquivo | Responsabilidade |
|---------|------------------|
| **app.py** | Rotas Flask: autenticação, turmas, materiais, download, logout |
| **service.py** | Lógica de negócio: validações, orquestração de operações |
| **model.py** | Acesso ao banco: queries para alunos, professores, turmas, materiais |
| **BANCO.py** | Definição do schema: tabelas (Escola, Professor, Aluno, Turma, Material) |
| **inserts.py** | População inicial: 8 escolas, 3 professores, 12 turmas e 10 alunos |

---

## ▶️ Como Executar o Projeto

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Joao-dapaz/pi-joao-pedro.git
   cd pi-joao-pedro
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou: source venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install flask
   ```

4. **Inicialize o banco de dados (opcional):**
   ```bash
   python BANCO.py      # Criar tabelas
   python inserts.py    # Popular com dados de teste
   ```

5. **Execute a aplicação:**
   ```bash
   python app.py
   ```

6. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

---

## 🧪 Testando a Aplicação

### Testes Unitários
```bash
pytest tests/test_service.py
```

### Testes E2E (End-to-End)
```bash
pytest E2E/test_frontend.py
```

### Usuários de Teste
Após rodar `inserts.py`, você pode usar:
- **Aluno:** email: `aluno@email.com`
- **Professor:** email: `professor@email.com`
- **Escola:** email: `escola@email.com`

---

## 🎯 Objetivo do Projeto

O Maestro foi desenvolvido como parte do curso Técnico em Desenvolvimento de Sistemas, com foco na aplicação prática de conceitos como:

* Desenvolvimento web com Flask
* Arquitetura em camadas (MVC)
* Design de banco de dados relacional
* Experiência do usuário (UI/UX)
* Testes automatizados (unitários e E2E)

---

## 🎨 Design e Interface

O protótipo visual do sistema foi desenvolvido no Figma, com foco em uma interface intuitiva, moderna e acessível, facilitando a navegação entre alunos, professores e escolas.

---

## 👨‍💻 Autor

João Pedro  
Estudante de Desenvolvimento de Sistemas

---

## 📌 Status do Projeto

🚧 Em desenvolvimento (em constante evolução)
