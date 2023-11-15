from ubuntu:18.04

run apt-get -qq update && apt-get install -qq --no-install-recommends xinetd socat gcc python
run apt-get install -qq -y libc6-dev

run useradd -mU coverage

copy ./src/child_hook.so /child_hook.so
copy ./src/main_hook.so /main_hook.so
copy ./src/main /main
copy ./src/get_patchpoints.py /get_patchpoints.py
copy ./src/fetch.h /fetch.h
copy ./src/fetch.c /fetch.c
copy ./server /server
copy ./service.conf /service.conf
copy ./flag /flag

run chmod +x /server
run chmod +x /main
run chmod 440 /flag

run chown root:coverage /flag

expose 5000
cmd ["/usr/sbin/xinetd", "-syslog", "local0", "-dontfork", "-f", "/service.conf"]
#cmd ["/server"]
