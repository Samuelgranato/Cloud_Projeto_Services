sudo rm /boot/grub/menu.lst
sudo apt update --assume-yes && sudo apt upgrade --assume-yes -y
sudo apt install --assume-yes python3-pip 
yes | pip3 install flask
yes | pip3 install pymongo

