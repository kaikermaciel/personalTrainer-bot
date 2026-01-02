# 🏋️‍♂️ Personal Trainer Bot com IA (GitHub Actions + Gemini)

Este projeto é uma automação em **Python** que atua como um Personal Trainer digital. Ele roda diariamente na nuvem via **GitHub Actions**, gera treinos personalizados usando a **IA** e envia os planos por e-mail para uma lista de atletas cadastrados.

Se a IA estiver indisponível, o sistema conta com um mecanismo de **Fallback (Backup)** robusto para garantir que ninguém fique sem treinar.

---

## 🚀 Funcionalidades

* **🤖 Geração com IA:** Usa o modelo `gemma-3-27b-it` para criar treinos únicos baseados no perfil de cada usuário (ex: Hipertrofia vs. Resistência). Verificar a lista de modelos disponíveis e analisar qual se alinha com seu plano.
* **👥 Multi-Usuário:** Suporta múltiplos perfis. O script itera sobre uma lista de atletas e personaliza o prompt para cada um.
* **🛡️ Sistema Fail-Safe:** Se a API do Gemini falhar, cair ou der erro de cota, o script alterna automaticamente para uma rotina fixa de backup. Fazer mudanças de acordo com o que desejas.
* **☁️ Serverless:** Roda gratuitamente no GitHub Actions com agendamento Cron (sem necessidade de servidor ligado 24/7).
* **📧 E-mails HTML:** Envio formatado com listas limpas e design responsivo simples.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Google Gemini API** (`google-generativeai`)
* **GitHub Actions** (Automação/Cron)
* **SMTP Lib** (Envio de E-mails)

---

## ⚙️ Configuração Local

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repo.git](https://github.com/seu-usuario/seu-repo.git)
    cd seu-repo
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    
    pip install -r requirements.txt
    ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz (não suba isso para o GitHub!) com o seguinte conteúdo:
    ```env
    EMAIL_USER=seu_email@gmail.com
    EMAIL_PASSWORD=sua_senha_de_app_google # verificar documentação de como gerar essa senha (não é a senha de acesso padrão)
    GEMINI_API_KEY=sua_chave_do_ai_studio
    ```

4.  **Edite os Perfis:**
    No arquivo `script.py`, edite a lista `ATLETAS` com os dados reais:
    ```python
    ATLETAS = [
        {
            "nome": "Seu Nome",
            "email": "seu@email.com",
            "perfil": "Objetivo: Hipertrofia...",
            "nivel": "Intermediário"
        },
        # Adicione outros aqui...
    ]
    ```

5.  **Teste Localmente:**
    ```bash
    python script.py
    ```

---

## ☁️ Configuração no GitHub (Deploy)

Para rodar automaticamente todo dia:

1.  Vá na aba **Settings** > **Secrets and variables** > **Actions** do seu repositório.
2.  Adicione as seguintes *Repository Secrets*:
    * `EMAIL_USER`: Seu e-mail do Gmail.
    * `EMAIL_PASSWORD`: Sua Senha de App (Gerada na conta Google, *não* é a senha de login).
    * `GEMINI_API_KEY`: Sua chave de API do Google AI Studio.
3.  O Workflow está configurado em `.github/workflows/build.yml` para rodar todos os dias às **05:30 AM (Horário de Manaus)**.

---

## 📂 Estrutura do Projeto

```text
.
├── .github/
│   └── workflows/
│       └── build.yml    # Configuração do Cron Job
├── script.py            # Lógica principal (IA + Email)
├── requirements.txt     # Dependências (google-generativeai, python-dotenv)
├── .env                 # Variáveis locais (Ignorado pelo Git)
└── README.md            # Documentação
