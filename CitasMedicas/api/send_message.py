from twilio.rest import Client

def send(phone_number, message="Hi from Django App"):
    # Las credenciales de Twilio (asegúrate de usar las tuyas propias)
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    from_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'  # El número que compraste en Twilio

    # Crear una instancia del cliente de Twilio
    client = Client(account_sid, auth_token)

    try:
        # Enviar el mensaje SMS
        message = client.messages.create(
            body=message,
            from_=from_phone_number,
            to=phone_number
        )

        # Verificar si el mensaje fue enviado correctamente
        if message.sid:
            return "Message sent successfully"
        else:
            return "Failed to send message"
    except Exception as e:
        return f"Error: {str(e)}"
