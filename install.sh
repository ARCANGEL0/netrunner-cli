#!/bin/bash
echo "// INSTALLATION_SEQUENCE . . . . . . . . . . . " | pv -qL 45
echo ""
clear
sudo apt update -qq > /dev/null 2>&1
echo ">>>> FETCHING NECESSARY MODULES. . . . . . . . " | pv -qL 45
sudo apt-get install gnome-terminal ffmpeg curl wget zip htop  -y curl > /dev/null 2>&1
echo "NET::TECH INTERFACE INSTALLATION. . . . . . . . " | pv -qL 45
sudo apt-get install git nmtui nmap figlet micro toilet tor python pip3 ffmpeg pv -y curl > /dev/null 2>&1
pip3 install wifi --break-system-packages
[ ! -d "$HOME/.boot" ] && mkdir -p "$HOME/.boot"

for item in *; do
  [ -d "$item" ] && cp -r "$item" "$HOME/.boot/" || cp "$item" "$HOME/.boot/"
done

if [[ "$SHELL" == *"zsh"* ]]; then
  RC_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
  RC_FILE="$HOME/.bashrc"
else
  exit 1
fi

mkdir -p ~/.local/share/fonts
[ ! -f ~/.local/share/fonts/starwars.flf ] && curl -o ~/.local/share/fonts/starwars.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/starwars.flf
[ ! -f ~/.local/share/fonts/Doom.flf ] && curl -o ~/.local/share/fonts/Doom.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/Doom.flf



echo "///// SETTING PATH " | pv -qL 30
echo ""
echo ""
grep -q "python $HOME/.boot/init.py" "$RC_FILE" || echo "python $HOME/.boot/init.py" >> "$RC_FILE"
echo ""


cd $HOME
echo "[::]> INSTALLING DEPENDENCIES AND TOOLS. . . . . . . .   " | pv -qL 60
echo ""
echo ""

wget https://github.com/JohnMcLaren/torctl-bridged/releases/download/torctl-bridged/torctl-bridged_0.5.7-1_amd64.deb
sudo apt install $HOME/torctl-bridged_0.5.7-1_amd64.deb

git clone https://github.com/ARCANGEL0/EzyMap.git $HOME/.local/EzyMap
cd $HOME/.local/EzyMap 
echo "Installing..."
echo "Updating package lists..."
sudo apt-get update -qq > /dev/null 2>&1

echo "Installing curl..."
sudo apt-get install -y curl > /dev/null 2>&1

echo "Installing nmap..."
sudo apt-get install -y nmap > /dev/null 2>&1

mkdir -p ~/.local/share/fonts
[ ! -f ~/.local/share/fonts/starwars.flf ] && curl -o ~/.local/share/fonts/starwars.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/starwars.flf
[ ! -f ~/.local/share/fonts/Doom.flf ] && curl -o ~/.local/share/fonts/Doom.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/Doom.flf
sudo systemctl stop tor
for i in {1..5}; do
  echo -n "Loading"
  for j in {1..3}; do
    echo -n "."
    sleep 0.5
  done
  echo ""
done

echo ""

figlet -f ~/.local/share/fonts/starwars.flf "EzyMap"

sudo cp ezymap ~/.local/bin/

SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" == "bash" ]; then
  echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
elif [ "$SHELL_NAME" == "zsh" ]; then
  echo "export PATH=\$PATH:$(pwd)" >> ~/.zshrc
else
  sudo cp ezymap /usr/bin/
fi


cd $HOME;
clear    
sleep 5 
echo " "
echo " "
echo " "
figlet -f ~/.local/share/fonts/starwars.flf "NET::TECH"
echo "NET::TECH UI BOOT SCRIPT INSTALLED SUCCESSFULLY ✔" | pv -qL 45
echo " "
echo " "
cd $HOME
read -n 1 -s -r -p "Press any key to restart your shell..."
clear 
cd $HOME;
