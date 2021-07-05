# notificador

# Dependencias

- Windows
- Python 3.7+
- [Git](https://git-scm.com/downloads)
- [Chia Plot Status](https://github.com/grayfallstown/Chia-Plot-Status)
- Log de Chia o su fork debe estar a nivel `INFO`
- Crear un bot en Telegram
- Programador de Tareas de Windows


# 1. Instalación vía Powershell


1. Abre Powershell

Clona el repositorio en alguna ubicación de tu pc (ejemplo. C:\Users\[YOUR-USER]\)

    cd C:\Users\[YOUR-USER]\
    git clone https://github.com/Hatt3rPi/notificador.git
    cd notificador

2. Crea un ambiente virtual para que corra el notificador llamado 'venv'

     `python.exe -m venv venv `

3. Activa el ambiente virtual recién creado

     `. .\venv\Scripts\activate `

Nota: si te arroja un error diciendo 'The term 'python.exe' is not recognized' or 'Python was not found', cambiar python.exe en la última línea por py.exe o python3.exe. Si no funciona, se debe a que no tiene python instalado en tu sistema.


4. Actualiza pip3 a la última versión

     `python.exe -m pip install --upgrade pip `

5. Instala requisitos

     `pip3 install -r requirements.txt `

6. Desactiva el ambiente virtual

     `deactivate `
     
# 2. Dejar log a nivel `INFO`

1. Abre el siguiente archivo con tu editor de texto favorito
    ```
    C:\Users\[YOUR-USER]\.chia\mainnet\config\config.yaml
    ```
    
3. Encuentra la línea 
    ```
    log_level: DEBUG
    ```
    y déjala en nivel `INFO` 
    ```
    log_level: INFO
    ```
4. Cierra la GUI de Chia o tu fork, y vuelve a iniciarla.

# Crear un bot en Telegram
1. En Telegram ingresa @Botfather en la pestaña de búsqueda y elige este bot.
    ![image](https://user-images.githubusercontent.com/11076084/124400069-d7c05c80-dced-11eb-97e9-8ce1afbc60b3.png)
    Ten en cuenta que los bots oficiales de Telegram tienen una marca de verificación azul junto a su nombre

2. Haz clic en "Inicio" para activar el bot BotFather.
    ![image](https://user-images.githubusercontent.com/11076084/124400089-f888b200-dced-11eb-824b-71233aacbd70.png)
    En respuesta, recibirás una lista de comandos para administrar bots.
3. Elige o escribe el comando / newbot y envíalo.
    ![image](https://user-images.githubusercontent.com/11076084/124400097-0807fb00-dcee-11eb-80be-79ab60df8067.png)
4. Elige un nombre para tu bot: tus suscriptores lo verán en la conversación. Y elige un nombre de usuario para tu bot: el bot se puede encontrar por tu nombre de usuario en las búsquedas. El nombre de usuario debe ser único y terminar con la palabra "bot".
    ![image](https://user-images.githubusercontent.com/11076084/124400108-16561700-dcee-11eb-97c7-d05b31cc84ba.png)
    
    Después de elegir un nombre adecuado para tu bot, se crea el bot. Recibirás un mensaje con un enlace a tu bot t.me/ <nombre de usuario del bot>, recomendaciones para configurar una imagen de perfil, descripción y una lista de comandos para administrar tu nuevo bot.
    Para conectar un bot al notificador necesitas un token. 
    ![image](https://user-images.githubusercontent.com/11076084/124400122-469db580-dcee-11eb-9bfe-e61937bdfb2b.png)
    
5. Copia el ID del BOT en el campo `token_bot` del archivo `parametros.py`
    ![image](https://user-images.githubusercontent.com/11076084/124400179-a1371180-dcee-11eb-9c5c-550dec41980b.png)

6. En Telegram ingresa @userinfobot en la pestaña de búsqueda y elige este bot.
    ![image](https://user-images.githubusercontent.com/11076084/124400281-3df9af00-dcef-11eb-8976-1fb5e024149e.png)
7. Activa el bot con el botón anterior o con el comando `/start`
    ![image](https://user-images.githubusercontent.com/11076084/124400297-59fd5080-dcef-11eb-8f53-f3e576bfaaae.png)
8. Copia el ID en el campo `chat_id` del archivo `parametros.py`
    ![image](https://user-images.githubusercontent.com/11076084/124400341-a6489080-dcef-11eb-88ca-4359c40ec39a.png)

    
