# Jampyyp Bot

Bot de Discord multifuncional desarrollado en Python con discord.py. Incluye reproducción de música con cola, comandos de moderación, sistema de advertencias persistente y comandos de entretenimiento.

## Características

- **Música** — Reproducción desde YouTube por URL o búsqueda, cola de canciones, controles con botones de Discord
- **Moderación** — Kick, ban, mute (timeout), purge y sistema de advertencias con historial
- **Entretenimiento** — Piedra papel o tijeras, dado, avatar, TTS
- **Configuración** — Prefijo personalizable, canal de bienvenida configurable por servidor
- **Persistencia** — Configuración y advertencias almacenadas en SQLite por servidor

## Requisitos

- Python 3.11+
- ffmpeg instalado en el sistema

## Instalación

**1. Clona el repositorio**
```bash
git clone https://github.com/JeanBiza/discordbot.git
cd discordbot
```

**2. Crea un entorno virtual e instala dependencias**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "discord.py[voice]"
```

**3. Instala ffmpeg**
```bash
# Arch / EndeavourOS
sudo pacman -S ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
Descarga ffmpeg desde https://ffmpeg.org/download.html
Extrae el zip y agrega la carpeta bin/ al PATH del sistema
```

**4. Configura las variables de entorno**
```bash
cp .env.example .env
```
Edita `.env` y agrega tu token de Discord:
```
DISCORD_TOKEN="tu_token_aqui"
```

**5. Ejecuta el bot**
```bash
python main.py
```

## Comandos

| Categoría | Comando | Descripción |
|-----------|---------|-------------|
| **Música** | `$play <url/búsqueda>` | Reproduce una canción desde YouTube |
| | `$pause` | Pausa la canción actual |
| | `$resume` | Reanuda la canción actual |
| | `$skip` | Salta a la siguiente canción |
| | `$stop` | Detiene la música y limpia la cola |
| | `$queue` | Muestra la cola de canciones |
| | `$join` / `$leave` | Conecta / desconecta del canal de voz |
| | `$tts <texto>` | Envía un mensaje de voz en el canal |
| **Moderación** | `$kick @usuario [razón]` | Expulsa a un usuario |
| | `$ban @usuario [razón]` | Banea a un usuario |
| | `$unban <id>` | Desbanea a un usuario por ID |
| | `$banlist` | Muestra la lista de usuarios baneados |
| | `$mute @usuario [minutos]` | Silencia a un usuario (timeout) |
| | `$unmute @usuario` | Quita el silencio a un usuario |
| | `$purge <n>` | Elimina los últimos n mensajes del canal |
| | `$warn @usuario [razón]` | Registra una advertencia |
| | `$warnings @usuario` | Muestra el historial de advertencias |
| | `$clearwarns @usuario` | Elimina todas las advertencias de un usuario |
| **Entretenimiento** | `$rps <piedra/papel/tijeras>` | Piedra, papel o tijeras |
| | `$dice` | Tira un dado de 6 caras |
| | `$avatar [@usuario]` | Muestra el avatar de un usuario |
| | `$hi [@usuario]` | Saluda a un usuario |
| **Configuración** | `$prefix <símbolo>` | Cambia el prefijo del bot |
| | `$setwelcome #canal` | Configura el canal de bienvenida |
| | `$help` | Muestra todos los comandos |

## Estructura del proyecto

```
discordbot/
├── main.py              # Entrada principal, carga de cogs y manejo de errores
├── database.py          # Capa de acceso a SQLite (configuración y advertencias)
├── webserver.py         # Servidor Flask para keep-alive
├── requirements.txt
├── .env.example
└── cogs/
    ├── config.py        # Comandos de configuración y bienvenida
    ├── fun.py           # Comandos de entretenimiento
    ├── moderation.py    # Comandos de moderación
    ├── music.py         # Comandos de música y cola
    └── ui.py            # Botones de control de música
```

## Stack

- [discord.py](https://discordpy.readthedocs.io/) 2.7
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) para extracción de audio de YouTube
- [gTTS](https://pypi.org/project/gTTS/) para text-to-speech
- SQLite para persistencia de datos
- Flask para keep-alive