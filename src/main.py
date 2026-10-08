#!/usr/bin/env python3
import os
import sys
import json
import argparse
from src.engine import ProjectAnalyzer, render_ui, asdict

def main():
    parser = argparse.ArgumentParser(
        description="CODEWEAVER Alpha.1: Deterministic, read-only project understanding framework."
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Target folder path to analyze"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output results strictly as raw JSON data for other AI agents"
    )
    args = parser.parse_args()

    # Automatically drop down to clean data mode if being used as a pipeline pipeline/plugin
    is_piped = not sys.stdout.isatty()

    # Guard rail against invalid target environments
    if not os.path.isdir(args.path):
        err_payload = {"status": "error", "message": f"Path '{args.path}' does not exist or is inaccessible."}
        if args.json or is_piped:
            print(json.dumps(err_payload))
        else:
            print(f"\033[31mError: {err_payload['message']}\033[0m", file=sys.stderr)
        sys.exit(1)

    try:
        # Instantiate your core deterministic analytics pipeline
        analyzer = ProjectAnalyzer(args.path)
        context = analyzer.analyze()

        if args.json or is_piped:
            # Emit clean structured JSON payload for external AIs to ingest
            print(json.dumps(asdict(context), indent=2))
        else:
            # Present the beautiful terminal experience for human developers
            render_ui(context)
            
    except Exception as e:
        err_payload = {"status": "error", "message": f"Execution halted: {str(e)}"}
        if args.json or is_piped:
            print(json.dumps(err_payload))
        else:
            print(f"\033[31mSystem Failure: {str(e)}\033[0m", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
