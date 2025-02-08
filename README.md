# Evangelio del Día - Bot de WhatsApp

Este proyecto es un bot automatizado que obtiene el evangelio del día de un canal de YouTube específico, genera un resumen utilizando la API de Gemini, convierte el texto a audio y lo envía a través de WhatsApp.

## 🚀 Características

- Obtiene automáticamente el evangelio del día desde YouTube
- Genera resúmenes inteligentes usando Gemini AI
- Convierte el texto a audio usando gTTS
- Envía mensajes y archivos de audio por WhatsApp
- Manejo de errores robusto y logging detallado
- Autenticación OAuth2 para YouTube API

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google Cloud Platform con YouTube Data API v3 habilitada
- Credenciales de API de Gemini
- Cuenta de WhatsApp Business API

### Obtención de Credenciales

1. **Gemini API Key**:
   - Ve a https://makersuite.google.com/app/apikey
   - Crea una cuenta si no la tienes
   - Genera una nueva API key

2. **YouTube API y client-secret.json**:
   - Ve a https://console.cloud.google.com/
   - Crea un nuevo proyecto
   - Habilita la YouTube Data API v3
   - Ve a "Credenciales"
   - Crea credenciales -> ID de cliente de OAuth
   - Selecciona "Aplicación de escritorio"
   - Descarga el archivo JSON y renómbralo a `client-secret.json`

3. **WhatsApp Business API (Green API)**:
   - Ve a https://green-api.com/
   - Regístrate para obtener una cuenta
   - Crea una nueva instancia
   - Obtendrás:
     - `WHATSAPP_ID_INSTANCE`
     - `WHATSAPP_API_TOKEN`

## 🔧 Configuración

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/evangelio-bot.git
cd evangelio-bot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno en un archivo `.env`:
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# WhatsApp Configuration
WHATSAPP_ID_INSTANCE=your_whatsapp_instance_id
WHATSAPP_API_TOKEN=your_whatsapp_api_token
# Número de WhatsApp en formato: país+número@c.us
WHATSAPP_RECIPIENT=34612345678@c.us

# YouTube Channel Configuration
CHANNEL_ID=your_youtube_channel_id
```

4. Coloca tu archivo `client-secret.json` de Google OAuth2 en el directorio raíz

## 🎯 Uso

Para ejecutar el bot:

```bash
python main.py
```

La primera vez que ejecutes el programa, se abrirá una ventana del navegador solicitando autorización para acceder a YouTube. Las credenciales se guardarán en `token.pickle` para futuros usos.

## 📁 Estructura del Proyecto

```
Proyecto_Evangelio/
├── .env                    # Variables de entorno
├── .gitignore             # Archivos ignorados por git
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
├── client-secret.json     # Credenciales de OAuth2 de Google
├── config.py             # Configuración y carga de variables de entorno
├── youtube_fetcher.py    # Cliente de YouTube API
├── gemini_api.py         # Cliente de Gemini AI
├── tts_converter.py      # Conversor de texto a voz
├── whatsapp_sender.py    # Cliente de WhatsApp
└── main.py              # Punto de entrada principal
```

## 🔒 Seguridad

- Nunca subas tu archivo `.env` o `client-secret.json` al repositorio
- Mantén tus tokens y claves API seguros
- Usa siempre variables de entorno para las credenciales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📝 Notas

- El bot está configurado para buscar videos con el título "Evangelio del día" y la fecha actual
- Los archivos de audio se almacenan temporalmente en la carpeta `audio_files/`
- Se implementa un sistema de caché para las credenciales de YouTube

## ⚠️ Manejo de Errores

El proyecto incluye manejo de errores robusto para:
- Fallos en la conexión API
- Videos no encontrados
- Errores de conversión de audio
- Fallos en el envío de mensajes

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 