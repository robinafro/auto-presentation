from ai import fill_sysprompt
from images import parse_img_tags
from sources import parse_source_tags
from marp import marp_convert
from settings import MD_STORE_DIR, PPTX_STORE_DIR
import argparse
import os, sys


def get_prompt(**kwargs):
    """Get the prompt and output it to the user"""
    sysprompt = fill_sysprompt(**kwargs)
    print(sysprompt)


def convert_to_presentation(input_markdown, output_path, format="pptx"):
    response_with_images = parse_img_tags(input_markdown)
    response_with_sources = parse_source_tags(response_with_images)

    # Save the response to a markdown file
    path = os.path.join(MD_STORE_DIR, "response.md")

    if not os.path.exists(MD_STORE_DIR):
        os.makedirs(MD_STORE_DIR)

    with open(path, "w") as f:
        f.write(response_with_sources)

    # Convert to Presentation
    marp_convert(path, output_path, f"--{format}")

    print(f"Presentation generated at {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a presentation from a given prompt"
    )
    subparsers = parser.add_subparsers(dest="command")

    prompt_parser = subparsers.add_parser("prompt", help="Get the prompt")
    prompt_parser.add_argument(
        "--subject", type=str, help="The subject of the presentation", required=True
    )
    prompt_parser.add_argument(
        "--num-slides",
        type=int,
        help="The number of slides in the presentation",
        required=False,
        default=10,
    )
    prompt_parser.add_argument(
        "--country",
        type=str,
        help="The country of the presentation",
        required=False,
        default="the Czech Republic",
    )
    prompt_parser.add_argument(
        "--language",
        type=str,
        help="The language of the presentation",
        required=False,
        default="czech",
    )

    generate_parser = subparsers.add_parser(
        "generate", help="Generate the presentation"
    )
    generate_parser.add_argument(
        "--output", type=str, help="The output path of the presentation", required=True
    )

    args = parser.parse_args()
    if args.command == "prompt":
        get_prompt(
            subject=args.subject,
            num_slides=args.num_slides,
            country=args.country,
            language=args.language,
        )
    elif args.command == "generate":
        format = args.output.split(".")[-1]

        assert format in ["pptx", "pdf", "html"], "Invalid format"

        stdin = sys.stdin.read()
        convert_to_presentation(stdin, args.output, format=format)
    else:
        raise ValueError("Invalid command")
