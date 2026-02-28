#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai",
# ]
# ///

import base64
import json
import os
import sys

import openai

KNOWN_PARAMETERS = {"prompt", "size", "quality", "output_format"}
ALLOWED_SIZES = {"1024x1024", "1536x1024", "1024x1536"}
ALLOWED_QUALITIES = {"low", "medium", "high"}
ALLOWED_OUTPUT_FORMATS = {"png", "jpeg", "webp"}


def load_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path) as config_file:
        return json.load(config_file)


def validate_parameters(parameters: dict) -> None:
    unknown = set(parameters.keys()) - KNOWN_PARAMETERS
    if unknown:
        raise ValueError(f"Unknown parameters: {', '.join(sorted(unknown))}")

    if "prompt" not in parameters:
        raise ValueError("Missing required parameter: prompt")

    if not isinstance(parameters["prompt"], str) or not parameters["prompt"].strip():
        raise ValueError("Parameter 'prompt' must be a non-empty string")

    if "size" in parameters:
        if not isinstance(parameters["size"], str):
            raise ValueError("Parameter 'size' must be a string")
        if parameters["size"] not in ALLOWED_SIZES:
            raise ValueError(
                f"Invalid size '{parameters['size']}'. Must be one of: {', '.join(sorted(ALLOWED_SIZES))}"
            )

    if "quality" in parameters:
        if not isinstance(parameters["quality"], str):
            raise ValueError("Parameter 'quality' must be a string")
        if parameters["quality"] not in ALLOWED_QUALITIES:
            raise ValueError(
                f"Invalid quality '{parameters['quality']}'. Must be one of: {', '.join(sorted(ALLOWED_QUALITIES))}"
            )

    if "output_format" in parameters:
        if not isinstance(parameters["output_format"], str):
            raise ValueError("Parameter 'output_format' must be a string")
        if parameters["output_format"] not in ALLOWED_OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid output_format '{parameters['output_format']}'. Must be one of: {', '.join(sorted(ALLOWED_OUTPUT_FORMATS))}"
            )


def generate_image(parameters: dict, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)

    prompt: str = parameters["prompt"]
    size: str = parameters.get("size", "1024x1024")
    quality: str = parameters.get("quality", "medium")
    output_format: str = parameters.get("output_format", "png")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        quality=quality,
        output_format=output_format,
    )

    image_data = base64.b64decode(response.data[0].b64_json)

    output_directory = "/tmp/gpt-image"
    os.makedirs(output_directory, exist_ok=True)

    output_filename = f"output.{output_format}"
    output_path = os.path.join(output_directory, output_filename)

    with open(output_path, "wb") as output_file:
        output_file.write(image_data)

    return output_filename


def main() -> None:
    config = load_config()
    api_key: str = config["api_key"]

    parameters: dict = json.load(sys.stdin)

    validate_parameters(parameters)

    try:
        output_filename = generate_image(parameters, api_key)
    except openai.OpenAIError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    json.dump({"file": output_filename}, sys.stdout)


main()
