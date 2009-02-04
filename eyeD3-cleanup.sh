#!/usr/bin/env bash

# Convert tags to utf-8.
OPTS="${OPTS} --set-encoding=utf8 --force-update"

# Remove comments, lyrics and ID3v1 tags.
OPTS="${OPTS} --remove-comments --remove-lyrics"

# Remove any kind of embedded image.
for IMG_TYPE in $(eyeD3 --list-image-types | tail -n +2); do
	OPTS="${OPTS} --add-image=:${IMG_TYPE}"
done

# Convert all tags to ID3v2.4 and remove the ID3v1 tags, strip unneeded stuff
# from the tags, convert the encoding to UTF-8 and rewrite the ID3v1 tags.
eyeD3 --to-v2.4 "$@" >& /dev/null
eyeD3 --remove-v1 "$@" >& /dev/null
eyeD3 ${OPTS} "$@" >& /dev/null
eyeD3 --to-v1.1 "$@" >& /dev/null
