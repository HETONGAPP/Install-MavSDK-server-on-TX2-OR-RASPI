# Install-MavSDK-server-on-TX2-OR-RASPI

# Install MavSDK in Component computer (TX2 OR RASPI)
  source ./mavsdk.sh
# Install API on Master computer
  pip install Paramiko
  or pip3 install Paramiko
# Run the server on (TX2 OR RASPI)
  cd ~/MAVSDK/build/default/src/backend/src
  ./mavsdk_server -p 50051 serial:///dev/ttyTHS2:921600
# Run the USER.py on MASTRER server 
  python USER.py
  or python3 USER.py
