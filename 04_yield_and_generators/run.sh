#!/usr/bin/sh

TIME_CMD_FORMAT="\nTotal execution time: %e seconds"

echo "--- sync_generator.py (plain yield, lazy iteration) ---\n"
time -f "${TIME_CMD_FORMAT}" ./sync_generator.py
echo "\n--- Done ---"

echo "\n\n--- async_generator.py (async def + yield, consumed with async for) ---\n"
time -f "${TIME_CMD_FORMAT}" ./async_generator.py
echo "\n--- Done ---"

echo "\n\n--- yield_vs_await.py (side-by-side contrast) ---\n"
time -f "${TIME_CMD_FORMAT}" ./yield_vs_await.py
echo "\n--- Done ---"
