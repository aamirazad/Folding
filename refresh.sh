#!/usr/bin/env bash

cd /workspace/folding && python3 -m venv .venv && . .venv/bin/activate && flask run --debug