FROM amd64/ubuntu:hirsute

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  gdb \
  git \
  && rm -rf /var/lib/apt/lists/*

RUN echo "set disable-randomization off" >> ~/.gdbinit

RUN bash -c "$(curl -fsSL http://gef.blah.cat/sh)"

COPY reverse /tmp/reverse

EXPOSE 2888

CMD gdb -q /tmp/reverse
