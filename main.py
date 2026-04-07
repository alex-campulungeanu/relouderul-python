#!/usr/bin/env python3

import argparse
import json
import logging
import os
import subprocess
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from watchfiles import watch

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)

logger = logging.getLogger("RELOADER")


class ServiceInfo(BaseModel):
    name: str
    command: list[str]
    watch_path: str


def get_project_path() -> Path:
    path_str = os.getenv("DIAGNOSTIC_PATH")
    if path_str is None:
        raise SystemError("DIAGNOSTIC_PATH is not set")
    return Path(path_str)


def load_services() -> dict[str, ServiceInfo]:
    config_path = Path("services.json")
    if not config_path.exists():
        raise FileNotFoundError("File services.json not found")

    with open(config_path, "r") as f:
        data = json.load(f)

    services = {}
    for key, value in data.items():
        services[key] = ServiceInfo(
            name=value["name"],
            command=value["command"],
            watch_path=str(get_project_path() / value["watch_path"]),
        )
    return services


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--service", required=True, help="Give the the microservice to start"
    )
    args = parser.parse_args()
    return args


def run(args):
    process = None
    services = load_services()

    if args.service not in services:
        logger.error(f"Service {args.service} not found in configuration")
        available = ", ".join(services.keys())
        logger.info(f"Available services: {available}")
        return
    srv = services[args.service]

    try:
        while True:
            # Start the process
            logger.info(f"▶ Starting server {srv.name}...")
            process = subprocess.Popen(srv.command, cwd=get_project_path())

            # Wait for changes
            logger.info(f"👀 Watching for changes for {srv.name}...")
            for changes in watch(srv.watch_path, f"{get_project_path()}/libs"):
                logger.info("🔁 Change detected! Restarting server...")
                for _, path in changes:
                    if not path.endswith(".py"):
                        continue

                # Kill old process safely
                process.terminate()

                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    logger.info("⚠ Process did not exit, killing...")
                    process.kill()

                break  # Break watch loop → restart process
    except KeyboardInterrupt:
        logger.info("✋ Exiting...")
    finally:
        if process and process.poll() is None:
            process.kill()


if __name__ == "__main__":
    args = get_args()
    run(args)
