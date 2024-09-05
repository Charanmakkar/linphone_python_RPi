


sudo apt install cmake automake autoconf libtool intltool yasm libasound2-dev libpulse-dev libv4l-dev nasm git libglew-dev doxygen 

sudo pip install pystache && sudo pip install wheel


git clone --branch release/5.2 https://gitlab.linphone.org/BC/public/linphone-sdk.git --recursive



cd linphone-sdk && mkdir build-raspberry && cd build-raspberry



cmake .. -DLINPHONESDK_PLATFORM=Desktop -DENABLE_OPENH264=ON  -DENABLE_LIME_X3DH=OFF -DENABLE_ADVANCED_IM=OFF -DENABLE_WEBRTC_AEC=OFF -DENABLE_UNIT_TESTS=OFF -DENABLE_MKV=OFF -DENABLE_FFMPEG=OFF -DENABLE_CXX_WRAPPER=OFF -DENABLE_NON_FREE_CODECS=ON -DENABLE_VCARD=OFF -DENABLE_BV16=OFF -DENABLE_V4L=ON -DENABLE_CONSOLE_UI=ON -DENABLE_DAEMON=ON -DENABLE_FLEXIAPI=OFF -DENABLE_QRCODE=OFF -DENABLE_PYTHON_WRAPPER=ON -DENABLE_DOC=ON



make -j2



mkdir -p ~/.local/share/linphone


nano ~/.bashrc

PATH=/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin:$PATH
export PATH=$PATH:/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin/





cd linphone-sdk/desktop/bin





////////////**************************///////////////////////
person Account information
alternate_email SIP address: sip:charanmakkar@sip.linphone.org

person Username: charanmakkar

dns Domain: sip.linphone.org

lan Proxy/registrar address: sip:sip.linphone.org

settings_ethernet Transport: TLS (recommended), TCP or UDP




////////////**************************///////////////////////
sip:192.168.1.4:5060












