# Install-MavSDK-server-on-TX2-OR-RASPI

# 1.Install MavSDK in Component computer (TX2 OR RASPI)
  source ./mavsdk.sh
# 2.Install API on Master computer
  pip install Paramiko
  or pip3 install Paramiko
# 3.Run the server on (TX2 OR RASPI)
  cd ~/MAVSDK/build/default/src/backend/src
  ./mavsdk_server -p 50051 serial:///dev/ttyTHS2:921600
# 4.Run the USER.py on MASTRER server 
  python USER.py
  or python3 USER.py
