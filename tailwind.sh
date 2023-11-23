#!/usr/bin/env bash
cd /workspace/folding && curl -fsSL https://bun.sh/install | bash && source /home/gitpod/.bashrc && bun install && bun run tailwind