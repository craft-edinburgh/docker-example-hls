# Docker container for Vitis

1. To build the container:

```
make build-docker
```
This might take a while but you only need to run it once (unless you modified `Docker/Dockerfile`, e.g. adding more packages).

2. To enter the container:
```
make shell
```
The you are in the container and you can do whatever you want.

3. To test if this works, you can run a simple HLS example provided (inside the container).
```
make test-hls
```
If you see something like this in the console - it works!
```
INFO: [COSIM 212-1000] *** C/RTL co-simulation finished: PASS ***
```
