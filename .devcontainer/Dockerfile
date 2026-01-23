FROM golang:tip-alpine3.22 as agru
RUN apk add --no-cache git
WORKDIR /go/agru
RUN git clone https://github.com/etkecc/agru.git /go/agru
RUN go mod download
WORKDIR /go/agru/cmd/agru
RUN go build .

FROM alpine:3.22
RUN apk add --update --no-cache \
    ansible \
    ansible-core \
    ansible-lint \
    git \
    grep \
    jq \
    just \
    libc6-compat \
    nodejs \
    npm \
    openssh-client \
    pre-commit \
    pwgen \
    py3-passlib \
    py3-regex \
    py3-yaml \
    python3
RUN npm install -g @bitwarden/cli jfq
COPY --from=agru /go/agru/cmd/agru/agru /usr/bin/agru
