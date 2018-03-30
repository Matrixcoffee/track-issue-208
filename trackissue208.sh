#!/bin/sh

NEWWD="${0%/*.sh}"
[ "$0" != "$NEWWD" ] && cd "$NEWWD"

python3 TrackIssue208.py "$@"
