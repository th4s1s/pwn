FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

COPY flag.txt /home/user/
COPY chall /home/user/
COPY setup.sh /home/user/

WORKDIR /home/user/

CMD ["./setup.sh"]