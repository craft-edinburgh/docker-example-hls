vhls=/home/tools/Xilinx/2025.1/2025.1

# Build Docker container
build-docker: 
	@docker build \
        --build-arg HLS_PATH=$(vhls) \
        -f Docker/Dockerfile \
        --tag hls-vm Docker

shell: 
	@touch ${HOME}/.gitconfig
	@docker run \
        -it --shm-size 256m \
        --hostname hls-vm \
        -w /workspace \
        -v $(vhls):$(vhls):ro \
        -v /home/$(shell whoami)/.gitconfig:/root/.gitconfig:z \
        -v /home/$(shell whoami)/.ssh:/root/.ssh:z \
        -v $(shell pwd):/workspace:z \
        hls-vm:latest /bin/bash

test-hls:
	@(cd example; bash run.sh)
