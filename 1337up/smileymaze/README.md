# Instructions
run `./build.sh`

If you get an error, you will need to add xauth cookie. On your host VM, run `xauth list`

Then go to the docker container and run `xauth add :0 . COOKIE`