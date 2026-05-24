#!/usr/bin/sh

TIME_CMD_FORMAT="\nTotal execution time: %e seconds"

echo "--- blocking_in_async.py (event loop frozen, expect ~3s) ---\n"
time -f "${TIME_CMD_FORMAT}" ./blocking_in_async.py
echo "\n--- Done ---"

echo "\n\n--- create_task_vs_await.py ---\n"
time -f "${TIME_CMD_FORMAT}" ./create_task_vs_await.py
echo "\n--- Done ---"

echo "\n\n--- interleaving.py ---\n"
time -f "${TIME_CMD_FORMAT}" ./interleaving.py
echo "\n--- Done ---"

echo "\n\n--- cancellation_and_timeout.py ---\n"
time -f "${TIME_CMD_FORMAT}" ./cancellation_and_timeout.py
echo "\n--- Done ---"
