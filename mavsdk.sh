##-------- Install MavSDK server for TX2 OR RASPI -------##
##-------- Author: Tong He -------##
##-------- Date: 10/01/2021 -------##

mv GCS.py /home/$USER/
sudo apt update
sudo apt upgrade
sudo apt-get update -y
sudo apt-get install cmake build-essential colordiff git doxygen -y
git clone https://github.com/HETONGAPP/MAVSDK.git
cd /$(pwd)/MAVSDK/
source mavsdk_server.sh
pip3 install mavsdk

