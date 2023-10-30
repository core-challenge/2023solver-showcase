FROM ubuntu:20.04

#------------------------------------------------
# (1) install fundamental commands
#------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive
RUN \
    apt update && \
    apt -y upgrade && \
    apt install -y curl git man unzip sudo openjdk-16-jre
    # if you need any
ENV TZ=Asia/Tokyo

#   Hint: you may want to additionally install the followings. 
# 
#   apt install -y build-essential
#   apt install -y software-properties-common

#------------------------------------------------
# (2) install your solver
#------------------------------------------------
COPY ISR_Solver /ISR_Solver
WORKDIR /ISR_Solver

## .. write your solver install commands ..

# or if you can put all files into a PUBLIC repository
# just clone it and compile it
#
# git clone your-solver-repository
# ... write your solver install commands ...

#------------------------------------------------
# (3) write your solver execution command as ENTRYPOINT
# this command should accept 2 arguments *.col and *.dat
#------------------------------------------------

ENTRYPOINT ["java", "-cp", "bin"]
