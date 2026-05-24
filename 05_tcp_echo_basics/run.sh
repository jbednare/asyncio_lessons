#!/usr/bin/sh

# Start the echo server in the background, give it a moment to bind,
# run the client once, then tear the server down. `trap` makes sure the
# server is killed even if the client fails or the script is interrupted.

SERVER_PID=""
cleanup() {
    if [ -n "${SERVER_PID}" ] && kill -0 "${SERVER_PID}" 2>/dev/null; then
        echo "\n--- stopping server (pid=${SERVER_PID}) ---"
        kill "${SERVER_PID}" 2>/dev/null
        wait "${SERVER_PID}" 2>/dev/null
    fi
}
trap cleanup EXIT INT TERM

echo "--- starting server in background ---"
./echo_server.py &
SERVER_PID=$!
sleep 0.5

echo "\n--- running client ---\n"
./echo_client.py
echo "\n--- client done ---"
