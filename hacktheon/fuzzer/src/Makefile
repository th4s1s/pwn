all:
	g++ ./main.cc -o main ./instrument.cc fork_server.cc -lpthread -fno-stack-protector -mpreferred-stack-boundary=12
	gcc -shared -o child_hook.so -fPIC child_hook.c -ldl -fno-stack-protector
	gcc -shared -o main_hook.so -fPIC main_hook.c -ldl -fno-stack-protector
