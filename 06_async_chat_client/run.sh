#!/usr/bin/sh

# This demo needs interactive input from at least two terminals, so the
# script just starts the server in the background and prints what to do
# next. Run `./chat_client.py` in two or more separate terminals to chat.

SERVER_PID=""
cleanup() {
    if [ -n "${SERVER_PID}" ] && kill -0 "${SERVER_PID}" 2>/dev/null; then
        echo "\n--- stopping server (pid=${SERVER_PID}) ---"
        kill "${SERVER_PID}" 2>/dev/null
        wait "${SERVER_PID}" 2>/dev/null
    fi
}
trap cleanup EXIT INT TERM

echo "--- starting chat server in background ---"
./chat_server.py &
SERVER_PID=$!
sleep 0.5

cat <<'EOF'

Server is running. To try the chat:

  1. Open two (or more) extra terminals in this directory.
  2. In each, run:    ./chat_client.py
  3. Type a message in any client and press Enter -- every connected
     client will see it.
  4. Ctrl-C this terminal to stop the server when you are done.

Press Ctrl-C here to shut down.
EOF

wait "${SERVER_PID}"
