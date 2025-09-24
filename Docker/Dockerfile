# This Dockerfile configures a Docker environment that 
# contains all the required packages for the tool
FROM ubuntu:22.04

USER root
RUN apt-get update -y && apt-get install apt-utils -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

# Install basic packages 
RUN apt-get upgrade -y 
RUN apt-get update -y \
    && apt-get install -y gcc-riscv64-unknown-elf \
                          libgmp-dev python3 python3-pip g++\
                          clang llvm lld clang-tidy clang-format \
                          gcc-multilib gcc cmake sudo wget vim \
                          curl tmux git bc locales libncurses5 \
                          help2man

# Install tools from source 
# RUN mkdir -p /srcPkgs \
#     && cd /srcPkgs \
#     && git clone https://github.com/B-Lang-org/bsc.git \
#     && cd bsc \
#     && git checkout 65e3a87a17f6b9cf38cbb7b6ad7a4473f025c098 \
#     && git submodule update --init --recursive \
#     && make install-src

# Install board mapping dependencies 
# RUN apt-get install -y openocd

# Append any packages you need here
# RUN apt install -y gcc-11-riscv64-linux-gnu

RUN locale-gen en_US.UTF-8

CMD ["bash"]

# Install Python packages 
ENV PATH="${PATH}:/root/.local/bin"
RUN pip3 install --user --upgrade pip \
    && pip3 install black colorlog toml tabulate pyserial

# Define external paths used by the container 
ARG HLS_PATH

# Add environment variables
RUN printf "\
\nexport LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:\$LIBRARY_PATH \
\n# Basic PATH setup \
\nexport PATH=/root/.local/bin:\$PATH \
\n# Vitis setup \
\nexport VHLS=${HLS_PATH} \
\n# Thread setup \
\nexport nproc=\$(grep -c ^processor /proc/cpuinfo) \
\n# Terminal color... \
\nexport PS1=\"[\\\\\\[\$(tput setaf 3)\\\\\\]\\\t\\\\\\[\$(tput setaf 2)\\\\\\] \\\u\\\\\\[\$(tput sgr0)\\\\\\]@\\\\\\[\$(tput setaf 2)\\\\\\]\\\h \\\\\\[\$(tput setaf 7)\\\\\\]\\\w \\\\\\[\$(tput sgr0)\\\\\\]] \\\\\\[\$(tput setaf 6)\\\\\\]$ \\\\\\[\$(tput sgr0)\\\\\\]\" \
\nexport LS_COLORS='rs=0:di=01;96:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01' \
\nalias ls='ls --color' \
\nalias grep='grep --color'\n" >> /root/.bashrc

#Add vim environment
RUN printf "\
\nset autoread \
\nset hlsearch \
\nautocmd BufWritePost *.cpp silent! !clang-format -i <afile> \
\nautocmd BufWritePost *.c   silent! !clang-format -i <afile> \
\nautocmd BufWritePost *.h   silent! !clang-format -i <afile> \
\nautocmd BufWritePost *.hpp silent! !clang-format -i <afile> \
\nautocmd BufWritePost *.cc  silent! !clang-format -i <afile> \
\nautocmd BufWritePost *.py  silent! set tabstop=4 shiftwidth=4 expandtab \
\nautocmd BufWritePost *.py  silent! !python3 -m black <afile> \
\nautocmd BufWritePost * redraw! \
\n" >> /root/.vimrc

CMD ["bash"]

# Entrypoint set up
WORKDIR workspace
