#!/usr/bin/env bash

cd .git/hooks

HOOK_DIR=../../githooks
for hook in $(ls $HOOK_DIR); do
    if [ ! -f "./$hook" ]; then
        echo "Adding $hook"
        ln -s "$SOURCE/$hook" ./
    fi
done
