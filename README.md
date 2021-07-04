# notificador


# 1. Instalación vía Powershell


    Abre Powershell

    Clona el repositorio en alguna ubicación de tu pc (ejemplo. C:\Users\[YOUR-USER]\)

    cd C:\Users\[YOUR-USER]\
    git clone https://github.com/Hatt3rPi/notificador.git
    cd notificador

# 1.1 Crea un ambiente virtual para que corra el notificador llamado 'venv'

    python.exe -m venv venv

# 1.2. Activa el ambiente virtual recién creado

    . .\venv\Scripts\activate

    Nota: si te arroja un error diciendo 'The term 'python.exe' is not recognized' or 'Python was not found', cambiar python.exe en la última línea por py.exe o python3.exe. Si no funciona, se debe a que no tiene python instalado en tu sistema.

    Actualiza pip e instala los requisitos del notificador

# 1.3. Actualiza pip3 a la última versión

    python.exe -m pip install --upgrade pip

# 1.4. Instala requisitos

    pip3 install -r requirements.txt

# 1.5. Desactiva el ambiente virtual

    deactivate
