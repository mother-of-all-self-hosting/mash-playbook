FROM alpine:3.22.0

ENV ANSIBLE_LOG_PATH=" "
WORKDIR /playbook
ENTRYPOINT ["/bin/sh"]

RUN apk add --no-cache ansible ansible-core py3-passlib git openssh-client just

COPY . /playbook

RUN git rev-parse HEAD > /playbook/source-commit && \
	rm -rf /playbook/.git && \
	just roles
