FROM armv7/armhf-ubuntu:latest
ENV INITSYSTEM on
ENV mode=""
ENV ip=""
ENV perf=""
ADD run.py /
ADD Local.py /
ADD Cloud.py /
ADD Hybrid.py /
ADD lp.xml /
ADD mode_hybrid /mode_hybrid/
ADD Footage /Footage/
RUN apt-get update && apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
RUN apt-get install -y python3 python3-dev python3-pip python3-numpy python3-scipy
RUN pip3 install sk-video
CMD python3 run.py $mode $ip $perf