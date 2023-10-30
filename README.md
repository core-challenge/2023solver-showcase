# 2023solver-showcase

- This repository contains all solvers submitted for [CoRe Challenge 2023](https://core-challenge.github.io/2023/).
- For detail, please see [the submission repository][https://github.com/core-challenge/2023solver-submission/tree/main]. 

## Build

- `[container/]$ docker build -f Dockerfile -t solver-name .` will build each solver docker image.

## Run  

- Using the docker image, `docker run --rm -t -v /ABSOLUTEPATH/2023solver-submission/container/test-instances:/test solver-name /test/hc-toyyes-01.col /test/hc-toyyes-01_01.dat` will print a result.
    - Note: ABSOLUTEPATH must be the absolute path where the cloned repository downloaded.
