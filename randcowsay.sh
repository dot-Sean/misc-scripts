#!/bin/sh
#
# Copyright (c) 2007-2008 Sebastian Noack
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

FORTUNE="/usr/bin/fortune"
COWSAY="/usr/bin/cowsay"
COWFILE_DIR="/usr/share/cowsay-3.03/cows"
COWSAY_FLAGS="-b -d -g -p -s -t -w -y"

# Get random cowfile.
COWFILES_NUM=$(find ${COWFILE_DIR} -name "*.cow" | wc -l)
COWFILE=$(find ${COWFILE_DIR} -name "*.cow" | \
	head -n $(((RANDOM%COWFILES_NUM)+1)) | tail -n 1)

# Get a random flag.
COWSAY_FLAGS_NUM=$(echo ${COWSAY_FLAGS} | wc -w)
COWSAY_FLAG=""
for flag in ${COWSAY_FLAGS}; do
	[ $((RANDOM%COWSAY_FLAGS_NUM)) -eq 0 ] && break
	COWSAY_FLAG=${flag}
done

# Invoke fortune and cowsay.
${FORTUNE} | ${COWSAY} -f ${COWFILE} -n ${COWSAY_FLAG}
