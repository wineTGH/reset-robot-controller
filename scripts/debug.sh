ssh kvant@kvant.local "echo 'cd ~/robot && ./.venv/bin/python -m debugpy --listen kvant.local:5678 --wait-for-client ./main.py' | at now"
sleep 5
echo ==========
echo Task done!