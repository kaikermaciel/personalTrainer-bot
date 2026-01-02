import smtplib
import ssl
import datetime
import os
import google.generativeai as genai
from email.message import EmailMessage
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

# --- CONFIGURAÇÕES ---
EMAIL_SENDER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# --- CONFIGURAÇÃO DOS ATLETAS ---
ATLETAS = [
    {
        "nome": "Kaike",
        "email": EMAIL_SENDER,
        "perfil": "Homem, 90kg, 1.71m. Objetivo: Condicionamento metabólico e queima de gordura. Calistenia.",
        "nivel": "Intermediário"
    },
    {
        "nome": "Keke",
        "email": "macielkemerson@gmail.com",
        "perfil": "Homem. Objetivo: Perda de peso e condicionamento físico.",
        "nivel": "Iniciante/Intermediário"
    }
]

# Se a IA falhar
rotina_backup = {
    0: {
        "titulo": "SEGUNDA: Força Superior + Cardio",
        "treino": "<li>Flexão de braço: 3x falha</li><li>Tríceps Banco: 3x 12</li><li>Prancha: 3x 45s</li><li>Polichinelos: 1 min</li>",
        "dieta": "Carbo médio, Proteína alta."
    },
    1: {
        "titulo": "TERÇA: Pernas",
        "treino": "<li>Agachamento Livre: 4x 15</li><li>Afundo: 3x 10 cada perna</li><li>Panturrilha: 4x 20</li><li>Wall Sit: 45s</li>",
        "dieta": "Recuperação muscular. Coma bem."
    },
    2: {
        "titulo": "QUARTA: Cardio Intenso",
        "treino": "<li>Skipping: 4x 1 min</li><li>Abdominal Remador: 3x 15</li><li>Mountain Climbers: 3x 40s</li><li>Sprawl: 3x 10</li>",
        "dieta": "Hidratação dobrada (3.5L)."
    },
    3: {
        "titulo": "QUINTA: Full Body Rápido",
        "treino": "<li>Flexão: 3x 10</li><li>Agachamento: 3x 10 rápido</li><li>Superman: 3x 15</li><li>Prancha toques: 3x 20</li>",
        "dieta": "Evite fritura."
    },
    4: {
        "titulo": "SEXTA: Desafio Resistência",
        "treino": "<li>Circuito 5x: 50 Polichinelos + 20 Agachamentos + 30s Prancha</li>",
        "dieta": "Proteína alta."
    },
    5: {
        "titulo": "SÁBADO: Esporte",
        "treino": "<li>Pratique seu esporte favorito (Futebol, Corrida, Vôlei).</li>",
        "dieta": "Livre com consciência."
    },
    6: {
        "titulo": "DOMINGO: Descanso",
        "treino": "<li>Caminhada leve ou alongamento.</li>",
        "dieta": "Prepare a semana."
    }
}

def gerar_treino_ia(atleta, dia_int):
    """Tenta gerar treino com Gemini. Retorna None se falhar."""
    if not GEMINI_KEY:
        return None

    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_str = dias_semana[dia_int]

    prompt = f"""
    Aja como um personal trainer. Crie um treino para hoje: {dia_str}.
    ALUNO: {atleta['nome']}
    PERFIL: {atleta['perfil']}
    NÍVEL: {atleta['nivel']}
    DIETA: Deficit Calórico alinhado com o nível de esforço do atleta.
    
    Regras:
    1. Apenas peso do corpo (calistenia). Considere que caso seja necessários equipamentos específicos, eles podem ser encontrados em casa.
    2. Curto e direto.
    3. Responda APENAS com tags HTML <li> para os exercícios. Nada de introdução. Se quiser configurar a estética sinta-se a vontade
    4. Ao final, coloque uma frase motivacional.
    Exemplo: <li>3x10 Flexões</li>
    
    Observação: Antes ou depois desses exercícios, teremos uma corrida/caminhada leve ou moderada de 1 hora de duração. 
    """

    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemma-3-27b-it')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro na IA para {atleta['nome']}: {e}")
        return None

def enviar_email():
    dia_int = datetime.datetime.today().weekday()
    
    # Prepara o contexto SSL
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)

            for atleta in ATLETAS:
                print(f"Processando treino de: {atleta['nome']}...")
                
                # 1. IA
                conteudo_treino = gerar_treino_ia(atleta, dia_int)
                origem_treino = "Treino Personalizado"

                # 2. Se a IA falhar (retornar None), usa o Backup
                if not conteudo_treino:
                    print(f"IA falhou ou desativada. Usando backup para {atleta['nome']}.")
                    backup = rotina_backup.get(dia_int)
                    conteudo_treino = backup['treino']
                    dica_extra = f"<p><strong>Dica de Dieta:</strong> {backup['dieta']}</p>"
                    origem_treino = f"Treino Clássico: {backup['titulo']}"
                else:
                    dica_extra = "<p><i>Mantenha a constância!</i></p>"

                # Monta HTML
                body = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #2E86C1;">Bom dia, {atleta['nome']}!</h2>
                    <p>Aqui está o seu desafio de hoje:</p>
                    
                    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0;">{origem_treino}</h3>
                        <ul>
                            {conteudo_treino}
                        </ul>
                    </div>

                    {dica_extra}
                    
                    <p style="font-size: 12px; color: #777;">Automação Python v2.0</p>
                  </body>
                </html>
                """

                msg = EmailMessage()
                msg['From'] = EMAIL_SENDER
                msg['To'] = atleta['email']
                msg['Subject'] = f"Treino de Hoje {datetime.date.today().strftime('%d/%m/%Y')}: {atleta['nome']}"
                msg.set_content(body, subtype='html')

                smtp.send_message(msg)
                print(f"E-mail enviado para {atleta['nome']}!")

    except Exception as e:
        print(f"Erro CRÍTICO no envio: {e}")

if __name__ == "__main__":
    enviar_email()