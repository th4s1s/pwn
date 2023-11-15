FROM ubuntu:22.04

MAINTAINER anonymous
RUN apt-get update
RUN apt-get install xinetd systemctl -y

RUN useradd -m authservice
RUN useradd -m babyservice

RUN mkdir -p /tmp/session/
RUN mkdir -p /tmp/users/

COPY ./challenge/authservice /home/authservice/authservice
COPY ./challenge/babyservice /home/babyservice/babyservice
COPY ./challenge/flag /home/authservice/flag
COPY ./challenge/authservice.xinetd /etc/xinetd.d/authservice
COPY ./challenge/babyservice.xinetd /etc/xinetd.d/babyservice
COPY ./challenge/init.sh /init.sh

RUN chown -R root:authservice /home/authservice/
RUN chown -R root:babyservice /home/babyservice/
RUN chmod -R 750 /home/authservice/
RUN chmod -R 750 /home/babyservice/

RUN chown -R root:authservice /tmp/users/
RUN chown -R root:authservice /tmp/session/
RUN chmod -R 775 /tmp/users/
RUN chmod -R 775 /tmp/session/
RUN systemctl daemon-reload
RUN chmod +x /init.sh

WORKDIR /

CMD ["/init.sh"]

EXPOSE 1337