import smtplib
import ssl
import datetime
from email.message import EmailMessage
import os
from dotenv import load_dotenv 

load_dotenv()

EMAIL_SENDER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

if not EMAIL_SENDER or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_USER e EMAIL_PASSWORD são obrigatórios.")

env_list = os.environ.get('EMAIL_LIST')
if env_list:
    LISTA_DESTINATARIOS = [email.strip() for email in env_list.split(',')]
else:
    # Fallback se esquecer de configurar a Secret
    LISTA_DESTINATARIOS = [os.environ.get('EMAIL_USER')]
    LISTA_DESTINATARIOS = [EMAIL_SENDER]

print(f"DEBUG: EMAIL_USER está carregado? {'SIM' if EMAIL_SENDER else 'NÃO'}")
print(f"DEBUG: Tamanho da senha: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0}")


rotina = {
    0: {
        "titulo": "SEGUNDA: Força Superior + Cardio",
        "treino": """
        <ul>
            <li>Flexão de braço: 3x falha</li>
            <li>Tríceps Banco: 3x 10-15</li>
            <li>Prancha: 3x 45s</li>
            <li>Polichinelos: 1 min</li>
            <li>Sombra de Boxe: 2 min</li>
        </ul>
        """,
        "dieta": "Foco: Carboidrato médio no almoço, Proteína alta no jantar."
    },
    1: {
        "titulo": "TERÇA: Pernas (Cuidado com o joelho)",
        "treino": """
        <ul>
            <li>Agachamento Livre: 4x 15</li>
            <li>Afundo: 3x 10 cada perna</li>
            <li>Panturrilha: 4x 20</li>
            <li>Wall Sit: 45s isometria</li>
        </ul>
        """,
        "dieta": "Foco: Recuperação muscular. Coma bem no pós-treino."
    },
    2: {
        "titulo": "QUARTA: Cardio Intenso + Core",
        "treino": """
        <ul>
            <li>Skipping (Corrida parada): 4x 1 min</li>
            <li>Abdominal Remador: 3x 15</li>
            <li>Mountain Climbers: 3x 40s</li>
            <li>Sprawl (Meio Burpee): 3x 10</li>
        </ul>
        """,
        "dieta": "Hidratação dobrada hoje. Tente 3.5L de água."
    },
    3: {
        "titulo": "QUINTA: Full Body Rápido",
        "treino": """
        <ul>
            <li>Flexão: 3x 10</li>
            <li>Agachamento: 3x 10 (rápido)</li>
            <li>Superman (Dorsal): 3x 15</li>
            <li>Prancha toques no ombro: 3x 20</li>
        </ul>
        """,
        "dieta": "Padrão. Evite fritura no almoço."
    },
    4: {
        "titulo": "SEXTA: Desafio de Resistência",
        "treino": """
        <ul>
            <li>Corrida/Caminhada Rápida: 40 min</li>
            <li>OU Circuito: 5 rounds de (50 Polichinelos + 20 Agachamentos + 30s Prancha)</li>
        </ul>
        """,
        "dieta": "Sexta pode, mas com moderação. Tente manter a proteína alta."
    },
    5: {
        "titulo": "SÁBADO: Esporte + Culto",
        "treino": "Pratique seu esporte (Futebol/Vôlei/Corrida). Divirta-se.",
        "dieta": "Livre (com consciência)."
    },
    6: {
        "titulo": "DOMINGO: Recuperação Ativa",
        "treino": "Caminhada leve de 1h ou Alongamento completo. Descanso para o SNC.",
        "dieta": "Prepare as marmitas da semana!"
    }
}

def enviar_email():
    # Pega o dia da semana atual (0-6)
    dia_hoje = datetime.datetime.today().weekday()
    dados_hoje = rotina.get(dia_hoje)

    if not dados_hoje:
        print("Erro ao carregar rotina.")
        return

    subject = f"💪 Treino do Dia: {dados_hoje['titulo']}"
    
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2E86C1;">Bom dia! Bora treinar?</h2>
        <p>Aqui está o seu plano para hoje:</p>
        
        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0;">🔥 O Treino</h3>
            {dados_hoje['treino']}
        </div>

        <div style="background-color: #e8f8f5; padding: 15px; border-radius: 5px; margin-top: 10px;">
            <h3 style="margin-top: 0;">🍎 A Dieta</h3>
            <p>{dados_hoje['dieta']}</p>
        </div>

        <p style="font-size: 12px; color: #777;">Enviado automaticamente pelo seu script Python.</p>
      </body>
    </html>
    """

    context = ssl.create_default_context()

    try:
        # Abre a conexão UMA VEZ
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            # Loop para enviar para cada pessoa da lista
            for destinatario in LISTA_DESTINATARIOS:
                msg = EmailMessage()
                msg['From'] = EMAIL_SENDER
                msg['To'] = destinatario
                msg['Subject'] = subject
                msg.set_content(body, subtype='html')
                print(f"DEBUG: enviado para: {(destinatario)}")
                

                # Envia
                smtp.send_message(msg)
                print(f"E-mail enviado para: {destinatario}")
                
    except Exception as e:
        print(f"Erro no envio: {type(e).__name__} - {e}")

if __name__ == "__main__":
    enviar_email()