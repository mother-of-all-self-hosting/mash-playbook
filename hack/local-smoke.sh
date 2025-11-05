#!/usr/bin/env bash
set -euo pipefail

TAG="mash-nextcloud:32.0.1-smoke-$(date +%s)"
TMPDIR="$(mktemp -d)"
cleanup() {
  docker rmi -f "$TAG" >/dev/null 2>&1 || true
  rm -rf "$TMPDIR"
  docker container prune -f --filter "until=24h" >/dev/null 2>&1 || true
  docker image prune -f --filter "until=24h" >/dev/null 2>&1 || true
  docker builder prune -f --filter "until=24h" >/dev/null 2>&1 || true
}
trap cleanup EXIT

cat >"$TMPDIR/Dockerfile" <<'EOF_DOCKERFILE'
# syntax=docker/dockerfile:1.6
ARG NC_IMAGE=nextcloud:32.0.1-apache
FROM ${NC_IMAGE}

ARG APT_PROXY=
ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash","-o","pipefail","-c"]
ENV PHP_MEMORY_LIMIT=1024M \
    PHP_UPLOAD_LIMIT=2048M \
    PHP_MAX_EXECUTION_TIME=3600

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates curl \
      imagemagick libmagickcore-7.q16-10-extra \
      ghostscript poppler-utils \
      ffmpeg ffmpegthumbnailer \
      libheif1 librsvg2-bin \
      tesseract-ocr tesseract-ocr-eng tesseract-ocr-dan \
      libreoffice \
      fonts-dejavu fonts-liberation fonts-noto-color-emoji \
      fontconfig gsfonts hunspell-da \
      ocrmypdf \
      libimage-exiftool-perl; \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    for P in /etc/ImageMagick-6/policy.xml /etc/ImageMagick/policy.xml; do \
      [ -f "$P" ] || continue; \
      sed -ri 's/(pattern="PDF"[^>]*rights=)"none"/\1"read"/' "$P" || true; \
      sed -ri 's/(pattern="PS"[^>]*rights=)"none"/\1"read"/'  "$P" || true; \
      sed -ri 's/(pattern="EPS"[^>]*rights=)"none"/\1"read"/' "$P" || true; \
      sed -ri 's/(pattern="XPS"[^>]*rights=)"none"/\1"read"/' "$P" || true; \
    done

RUN set -eux; \
    if php -r 'exit(extension_loaded("imagick")?0:1);'; then \
      docker-php-ext-enable imagick || true; \
    else \
      apt-get update; \
      apt-get install -y --no-install-recommends autoconf build-essential libmagickwand-dev pkg-config; \
      pecl channel-update pecl.php.net; \
      printf '\n' | pecl install -f imagick; \
      docker-php-ext-enable imagick; \
      apt-get purge -y --auto-remove autoconf build-essential libmagickwand-dev pkg-config; \
      rm -rf /var/lib/apt/lists/* /tmp/pear ~/.pearrc; \
    fi

RUN set -eux; \
    install -d -o www-data -g www-data /var/www/html/data/tmp; \
    cat <<'EOF_PHP' >/usr/local/etc/php/conf.d/zzz-mash-overrides.ini
memory_limit=${PHP_MEMORY_LIMIT:-1024M}
upload_max_filesize=${PHP_UPLOAD_LIMIT:-2048M}
post_max_size=${PHP_UPLOAD_LIMIT:-2048M}
max_execution_time=${PHP_MAX_EXECUTION_TIME:-3600}
EOF_PHP

RUN cat <<'EOF_ENTRY' >/usr/local/bin/mash-entrypoint.sh
#!/bin/bash
set -euo pipefail
upload="${PHP_UPLOAD_LIMIT:-2048M}"
memory="${PHP_MEMORY_LIMIT:-1024M}"
maxexec="${PHP_MAX_EXECUTION_TIME:-3600}"
cat <<EOPHP >/usr/local/etc/php/conf.d/zzz-mash-overrides.ini
memory_limit=${memory}
upload_max_filesize=${upload}
post_max_size=${upload}
max_execution_time=${maxexec}
EOPHP
install -d -o www-data -g www-data /var/www/html/data/tmp
exec /entrypoint.sh "$@"
EOF_ENTRY
RUN chmod +x /usr/local/bin/mash-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/mash-entrypoint.sh"]
CMD ["apache2-foreground"]
EOF_DOCKERFILE

pushd "$TMPDIR" >/dev/null

docker buildx build --pull --progress=plain --load -t "$TAG" .

docker run --rm "$TAG" php -m | grep -iq imagick
docker run --rm "$TAG" bash -lc 'convert -list format | egrep "^(PDF|PS|EPS|XPS|HEIC|WEBP) "'
docker run --rm "$TAG" tesseract --list-langs | egrep -q '(^| )(eng|dan)( |$)'
docker run --rm "$TAG" ocrmypdf --version >/dev/null
docker run --rm "$TAG" ffmpeg -v error -hide_banner -filters >/dev/null

echo "Local smoke OK: $TAG"

popd >/dev/null
