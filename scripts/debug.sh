ssh kvant@kvanr.local "echo 'cd ~/robot && ./.venv/bin/python -m debugpy --listen kvant.local:5678 --wait-for-client ./main.py' | at now"
sleep 3
echo ==========
echo Task done!