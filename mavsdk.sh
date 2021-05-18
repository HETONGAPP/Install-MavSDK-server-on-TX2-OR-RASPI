##-------- Install MavSDK server for TX2 OR RASPI -------##
##-------- Author: Tong He -------##
##-------- Date: 10/01/2021 -------##

mv GCS.py /home/$USER/
git clone https://github.com/HETONGAPP/MAVSDK.git
cd /$(pwd)/MAVSDK/
source mavsdk_server.sh
sudo apt install python3-pip
pip3 install mavsdk

