#!/bin/bash

# remove se tiver instalado pelo snap
sudo snap remove firefox

# Caminho do arquivo a ser criado
FILE="/etc/apt/preferences.d/mozilla-firefox"

# Conteúdo a ser adicionado ao arquivo
CONTENT="Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001"

# Verifica se o arquivo já existe
if [ -f "$FILE" ]; then
    echo "O arquivo $FILE já existe. Adicionando o conteúdo..."
else
    echo "Criando o arquivo $FILE e adicionando o conteúdo..."
    sudo touch "$FILE"
fi

# Adiciona o conteúdo ao arquivo
echo -e "$CONTENT" | sudo tee "$FILE"

echo "Operação concluída."

# adiciona a versão mais recente
echo "Baixando versão mais recente do Firefox..."
sudo add-apt-repository ppa:mozillateam/ppa
sudo apt update

# instala o firefox
echo "Instalando o Firefox..."
sudo apt update && sudo apt install firefox
echo "Firefox instalado com sucesso!"