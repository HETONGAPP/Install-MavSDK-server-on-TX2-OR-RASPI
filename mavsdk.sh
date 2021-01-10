##-------- Install MavSDK server for TX2 OR RASPI -------##
##-------- Author: Tong He -------##
##-------- Date: 10/01/2021 -------##

mv GCS.py /home/$USER/
sudo apt-get update -y
sudo apt-get install cmake build-essential colordiff git doxygen -y
git clone https://github.com/mavlink/MAVSDK.git
cd MAVSDK
git checkout master
git submodule update --init --recursive
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_BACKEND=ON -Bbuild/default -H.
cmake --build build/default
pip3 install mavsdk

