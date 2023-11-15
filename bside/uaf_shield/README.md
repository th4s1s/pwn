# UAF S.H.I.E.L.D

## Compilation

```console
docker build --target run_qemu -t uaf_shield .
```

## Usage
```console
docker run -it --publish 8080:8080 uaf_shield
nc 127.0.0.1 8080
```
