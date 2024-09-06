# linphone_with_python

# Emergency Calling Booth - Linphone / Linphonec with Python with RPI with GUI

Multipowr_Plug_and_Play_Utility Tool {PPU TOOL} is a User Interaction Software written with python 3.11.x and 
many supporing libraries and development Tools.


********************************************

Communication Protocols Used by TOOL:
----------------
1. Ethernet 
2. Wifi
3. GUI - Tkinter Python



********************************************


Required Softwares are (For developement)
-----------------
1. Python 3.11.x (minimum) - with any text editor
2. VSCodes (prefered editor)
3. 



********************************************

TEST SERVER / APP / TOOLs used
-----------
Test Server APP/TOOLS
1. Linphone-5.2.6-win64.exe
Link : https://new.linphone.org/technical-corner/linphone?qt-technical_corner=2#qt-technical_corner
OR 
2. Linphone (Mobile-App) <- In your phone
Link : Google Play Store
or
3. msp_v9_setup.exe     <- Mini sip phone   (On Desktop)

4. mss_v50_u5.exe       <- Mini sip server  (On Desktop)
// For Windows Laptop
Link1 : https://www.myvoipapp.com/
Link2 : https://www.myvoipapp.com/download/index.html




********************************************
INSTALLATION GUIDE 
-----------
"readme instructions Linux.txt"

1. sudo apt update 

2. sudo apt install cmake automake autoconf libtool intltool yasm libasound2-dev libpulse-dev libv4l-dev nasm git libglew-dev doxygen 

3. sudo pip install pystache && sudo pip install wheel

4. git clone --branch release/5.2 https://gitlab.linphone.org/BC/public/linphone-sdk.git --recursive

5. cd linphone-sdk && mkdir build-raspberry && cd build-raspberry

6. cmake .. -DLINPHONESDK_PLATFORM=Desktop -DENABLE_OPENH264=ON  -DENABLE_LIME_X3DH=OFF -DENABLE_ADVANCED_IM=OFF -DENABLE_WEBRTC_AEC=OFF -DENABLE_UNIT_TESTS=OFF -DENABLE_MKV=OFF -DENABLE_FFMPEG=OFF -DENABLE_CXX_WRAPPER=OFF -DENABLE_NON_FREE_CODECS=ON -DENABLE_VCARD=OFF -DENABLE_BV16=OFF -DENABLE_V4L=ON -DENABLE_CONSOLE_UI=ON -DENABLE_DAEMON=ON -DENABLE_FLEXIAPI=OFF -DENABLE_QRCODE=OFF -DENABLE_PYTHON_WRAPPER=ON -DENABLE_DOC=ON

7. make -j2

8. mkdir -p ~/.local/share/linphone

9. sudo nano ~/.bashrc
// add these below 2 commands here
export PATH=/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin:$PATH
export PATH=$PATH:/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin/  # (optional)

10. cd linphone-sdk/desktop/bin

11. ./linphonec
