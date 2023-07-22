#!/usr/bin/env python3
import sys
import asyncio
import aiohttp
import argparse
import os

# Import other necessary modules and packages as needed

# Define your custom wordlist directory
CUSTOM_WORDLIST_DIR = "wordlists"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enhanced Web Path Discovery Scanner")
    parser.add_argument("target", help="Target URL to scan")
    parser.add_argument("-w", "--wordlist", help="Path to the custom wordlist")
    parser.add_argument("-m", "--method", choices=["GET", "POST", "PUT", "DELETE"], default="GET", help="HTTP method to use")
    parser.add_argument("--proxy", help="Proxy server to use for requests")
    # Add more arguments as needed

    return parser.parse_args()

def load_wordlist(file_path):
    with open(file_path, "r") as file:
        wordlist = [line.strip() for line in file]

    return wordlist

async def scan_path(session, target, path, method):
    url = target + "/" + path
    async with session.request(method, url) as response:
        # Handle response here (e.g., check for interesting status codes, keywords, etc.)
        print(f"{url} - Status Code: {response.status}")

async def main():
    args = parse_arguments()

    if args.wordlist:
        wordlist_path = args.wordlist
    else:
        # Use a default wordlist if not provided
        wordlist_path = os.path.join(CUSTOM_WORDLIST_DIR, "default.txt")

    if not os.path.isfile(wordlist_path):
        print(f"Wordlist not found: {wordlist_path}")
        sys.exit(1)

    target = args.target
    method = args.method.upper()

    paths = load_wordlist(wordlist_path)

    async with aiohttp.ClientSession() as session:
        tasks = [scan_path(session, target, path, method) for path in paths]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    if sys.version_info < (3, 7):
        sys.stdout.write("Sorry, this scanner requires Python 3.7 or higher\n")
        sys.exit(1)

    asyncio.run(main())
