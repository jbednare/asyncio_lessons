#!/usr/bin/env python3

import asyncio
import time
import sys


async def double_print_with_sleep(text_to_print) -> None:
    print(f"Starting print for: {text_to_print}")
    await asyncio.sleep(1)
    print(f"Printing text: {text_to_print}")


async def main():
    await asyncio.gather(
        double_print_with_sleep("Text 1"),
        double_print_with_sleep("Text 2"),
        double_print_with_sleep("Text 3"),
    )


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
