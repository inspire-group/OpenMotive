FROM armv7/armhf-ubuntu:latest
ENV INITSYSTEM on
ENV mode=""
ENV ip="0.0.0.0"
ENV perf=""
ADD run.py /
ADD Local.py /
ADD Cloud.py /
ADD Hybrid.py /
ADD test1.jpg /
ADD test2.jpg /
ADD test3.jpg /
ADD lp.xml /
ADD mode_hybrid /mode_hybrid/
ADD opencv-3.2.0 /opencv-3.2.0/
ADD opencv_contrib-3.2.0 /opencv_contrib-3.2.0/
RUN apt-get update && apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
RUN apt-get install -y python3 python3-dev python3-pip
#RUN apt-get install -y build-essential cmake pkg-config
#RUN apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng-dev
#RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#RUN apt-get install -y libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran
RUN apt-get install -y python3-numpy python3-scipy
RUN pip3 install sk-video
#WORKDIR /opencv-3.2.0
#RUN mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.2.0/modules .. && make && sudo make install && sudo ldconfig
#WORKDIR /
CMD python3 run.py $mode $ip $perf