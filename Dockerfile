FROM ubuntu:latest
LABEL authors="Lucas Fujita de Freitas"

ENTRYPOINT ["top", "-b"]