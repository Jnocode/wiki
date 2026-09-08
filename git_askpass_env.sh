#!/bin/sh
# Git asks this process for username/password; the token is supplied only by
# OpenClaw's runtime environment and is never stored in this repository.
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *)
    [ -n "${GITHUB_TOKEN:-}" ] || exit 1
    printf '%s\n' "$GITHUB_TOKEN"
    ;;
esac
