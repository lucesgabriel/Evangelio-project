# 🙏 Evangelio del Día - Bot Automatizado

Este proyecto es un bot automatizado que obtiene el evangelio del día de un canal de YouTube específico, genera un resumen utilizando la API de Gemini, convierte el texto a audio y lo envía a través de WhatsApp.

## 🌟 Características Principales

- 📺 Obtención automática del evangelio del día desde YouTube
- 🤖 Generación de resúmenes inteligentes usando Gemini AI
- 🎧 Conversión de texto a audio usando OpenAI TTS (con fallback a gTTS)
- 📱 Envío automático de mensajes y archivos de audio por WhatsApp
- 📝 Transcripción automática de audio usando Whisper
- 💾 Sistema de caché para optimizar las consultas
- 🔄 Manejo robusto de errores y logging detallado

## 🏗️ Estructura del Proyecto

```
Evangelio-project/
├── src/
│   ├── services/
│   │   ├── youtube_service.py    # Gestión de YouTube API
│   │   ├── gemini_service.py     # Integración con Gemini AI
│   │   └── whatsapp_service.py   # Envío de mensajes WhatsApp
│   ├── audio/
│   │   ├── transcription_manager.py  # Transcripción de audio
│   │   └── tts_converter.py      # Conversión texto a voz
│   └── data/
│       └── data_manager.py       # Gestión de caché y datos
├── config/
│   ├── __init__.py
│   └── config.py                 # Configuración centralizada
├── data/
│   ├── cache/                    # Caché de videos y transcripciones
│   └── credentials/              # Credenciales de APIs
├── audio_files/                  # Archivos de audio temporales
├── logs/                         # Registros del sistema
├── .env                         # Variables de entorno
├── main.py                      # Punto de entrada
└── requirements.txt             # Dependencias
```

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google Cloud Platform con YouTube Data API v3
- API Key de Gemini AI
- API Key de OpenAI (para TTS y Whisper)
- Cuenta de WhatsApp Business API (Green API)

## 🔑 Configuración de APIs

### 1. Gemini API
- Obtén tu API key en [Google AI Studio](https://makersuite.google.com/app/apikey)

### 2. YouTube API
- Configura un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
- Habilita YouTube Data API v3
- Crea credenciales OAuth2 y descarga `client-secret.json`

### 3. OpenAI API
- Regístrate en [OpenAI Platform](https://platform.openai.com/)
- Genera tu API key en la sección de configuración

### 4. WhatsApp Business API
- Regístrate en [Green API](https://green-api.com/)
- Crea una nueva instancia y obtén tus credenciales

## ⚙️ Configuración del Proyecto

1. Clona el repositorio:
```bash
git clone https://github.com/lucesgabriel/Evangelio-project.git
cd Evangelio-project
```

2. Crea y activa un entorno virtual:
```bash
python -m venv evangelio-project_env
source evangelio-project_env/bin/activate  # Linux/Mac
.\evangelio-project_env\Scripts\activate   # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno en `.env`:
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key

# WhatsApp Configuration
WHATSAPP_ID_INSTANCE=your_whatsapp_instance_id
WHATSAPP_API_TOKEN=your_whatsapp_api_token
WHATSAPP_RECIPIENT=country_code+number@c.us

# YouTube Channel Configuration
CHANNEL_ID=your_youtube_channel_id
```

5. Coloca el archivo `client-secret.json` en `data/credentials/`

## 🚀 Uso

Para ejecutar el bot:

```bash
python main.py
```

## 🔄 Flujo de Trabajo

1. **Obtención del Video**
   - Busca el video del evangelio del día en el canal configurado
   - Almacena la información en caché para optimizar futuras búsquedas

2. **Procesamiento del Contenido**
   - Obtiene la transcripción del video (YouTube o Whisper)
   - Genera un resumen usando Gemini AI
   - Convierte el texto a audio usando OpenAI TTS

3. **Distribución**
   - Envía el mensaje de texto por WhatsApp
   - Envía el archivo de audio por WhatsApp

## 🛠️ Mantenimiento

- Los archivos de audio se limpian automáticamente después de su uso
- El sistema de caché optimiza las consultas repetidas
- Los logs detallados facilitan el debugging

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles. 