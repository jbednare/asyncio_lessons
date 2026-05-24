#!/usr/bin/sh

TIME_CMD_FORMAT="\nTotal execution time: %e seconds"

echo "--- Running non-async example ---\n"
time -f "${TIME_CMD_FORMAT}" ./non_async_sleep_print.py
echo "\n--- Done ---"

echo "\n\n--- Running async example ---\n"
time -f "${TIME_CMD_FORMAT}" ./async_sleep_print.py
echo "\n--- Done ---"

echo "\n\n--- Running async gather example ---\n"
time -f "${TIME_CMD_FORMAT}" ./async_gather_sleep_print.py
echo "\n--- Done ---"
