FROM ubuntu:20.04

# Install dependencies
# RUN apt-get update && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git curl ca-certificates default-jre


RUN apt-get update && apt-get install -y --no-install-recommends wget build-essential libreadline-dev \ 
libncursesw5-dev libssl-dev libsqlite3-dev libgdbm-dev libbz2-dev liblzma-dev zlib1g-dev uuid-dev libffi-dev libdb-dev

#任意バージョンのpython install
RUN wget --no-check-certificate https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz \
&& tar -xf Python-3.11.2.tgz \
&& cd Python-3.11.2 \
&& ./configure --enable-optimizations\
&& make \
&& make install

RUN apt-get autoremove -y

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir colorlog networkx

RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1

COPY src /solver-dir
WORKDIR /solver-dir

# Set up your solver
# RUN git clone --depth 1 https://github.com/core-challenge/util-example-solver.git /util-example-solver

RUN cd /solver-dir/ddreconf && make

# Set environment variables if needed
# ENV PATH $PATH:/root/.local/share/coursier/bin

# specify the solver command
ENTRYPOINT ["bash", "/solver-dir/run.sh"]
