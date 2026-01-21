FROM golang:tip-alpine3.22 as agru
RUN apk add --no-cache git
WORKDIR /go/agru
RUN git clone https://github.com/etkecc/agru.git /go/agru
RUN go mod download
WORKDIR /go/agru/cmd/agru
RUN go build .

FROM ghcr.io/willhallonline/docker-ansible:2.17-alpine-3.22
RUN apk add --update --no-cache \
    libc6-compat \
    python3 \
    py3-pip \
    py3-regex \
    py3-yaml \
    py3-passlib \
    just \
    pre-commit \
    ansible-lint \
    pwgen \
    jq \
    nodejs npm && \
    pip3 install bwenv && \
    npm install -g @bitwarden/cli jfq
COPY --from=agru /go/agru/cmd/agru/agru /usr/bin/agru
