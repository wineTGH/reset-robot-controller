#! /bin/bash

rsync --filter=':- .gitignore' -azP . kvant@kvant.local:~/robot
ssh kvant@kvant.local 'cd ~/robot && ~/.local/bin/uv sync --no-dev'
