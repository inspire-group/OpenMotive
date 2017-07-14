FROM resin/armv7hf-debian
ENTRYPOINT []
ENV mode=""
ADD run.py /
ADD __pycache__ /
ADD Server /
ADD obd.pem /
ADD ModeStandard.py /
ADD ModeSecure.py /
ADD README.md /
RUN apt-get update && apt-get -y install python3 python3-pip python3-dev python3-pip
RUN pip3 install requests python-can
RUN sudo echo "dtparam=spi=on" >> /boot/config.txt
RUN sudo echo "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25" >> /boot/config.txt
RUN sudo echo "dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=24" >> /boot/config.txt
RUN sudo echo "dtoverlay=spi-bcm2835-overlay" >> /boot/config.txt
RUN apt-get update && apt-get -y install iproute2
CMD python3 ./run.py $mode