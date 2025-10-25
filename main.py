#!/usr/bin/env python3

"""
ASCII Art Generator
A command-line tool to generate ASCII art from images or text.

Dependencies:
    pip install pillow pyfiglet typer

Usage:
    # From an image
    python ascii_generator.py image path/to/your/image.jpg --width 120

    # From text
    python ascii_generator.py text "Hello World" --font "slant"
"""

import typer
from PIL import Image
import pyfiglet
import sys
from typing_extensions import Annotated

# Using a complex ramp provides more detail and shades.
ASCII_RAMP = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5YxjSQPObkWMgXqdD$#@"


def generate_image_art(image_path: str, new_width: int = 100) -> str:
    """
    Converts an image file into ASCII art.

    Args:
        image_path: The file path to the input image.
        new_width: The desired width of the ASCII art in characters.
                   Height is calculated based on aspect ratio.

    Returns:
        A string containing the ASCII art.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        raise typer.BadParameter(
            f"Unable to open image file '{image_path}'. Error: {e}"
        )

    image = image.convert("L")

    aspect_ratio = image.height / image.width
    new_height = int(new_width * aspect_ratio * 0.55)
    resized_image = image.resize((new_width, new_height))

    pixels = list(resized_image.getdata())

    ascii_art = ""
    ramp_length = len(ASCII_RAMP) - 1

    for i in range(0, len(pixels), new_width):
        row = pixels[i : i + new_width]

        for pixel_brightness in row:
            ramp_index = int((pixel_brightness / 255) * ramp_length)
            ascii_art += ASCII_RAMP[ramp_index]

        ascii_art += "\n"

    return ascii_art


def generate_text_art(text: str, font: str = "standard") -> str:
    """
    Converts a text string into a large "banner" style ASCII art.

    Args:
        text: The input text string.
        font: The name of the pyfiglet font to use.

    Returns:
        A string containing the figlet text.
    """
    try:
        return pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        return (
            f"Error: Font '{font}' not found. Using 'standard' instead.\n"
            + pyfiglet.figlet_format(text, font="standard")
        )
    except Exception as e:
        return f"Error generating text art: {e}"


# --- CLI ---

app = typer.Typer(
    help="A command-line tool to generate ASCII art from images or text.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    rich_markup_mode="markdown",
)


@app.command(
    name="image",
    help="Generate ASCII art from an **image** file.",
    epilog="Example: `python ascii_generator.py image my_photo.png --width 150`",
)
def image_cli(
    image_path: Annotated[
        typer.FileText,
        typer.Argument(
            help="Path to the input image file.",
            exists=True,
            readable=True,
            show_default=False,
            metavar="IMAGE_PATH",
        ),
    ],
    width: Annotated[
        int,
        typer.Option(
            "--width",
            "-w",
            help="Width of the generated ASCII art in characters.",
            min=10,
            show_default=True,
        ),
    ] = 100,
):
    """
    CLI command to generate ASCII art from an image.
    """
    try:
        ascii_art = generate_image_art(image_path.name, width)
        print(ascii_art)
    except Exception as e:
        typer.secho(
            f"Error processing image: {e}", fg=typer.colors.RED, file=sys.stderr
        )
        raise typer.Exit(code=1)


@app.command(
    name="text",
    help="Generate ASCII art from a **text** string.",
    epilog='Example: `python ascii_generator.py text "Hello World" --font big`',
)
def text_cli(
    text: Annotated[
        str,
        typer.Argument(
            help="Text string to convert into banner art.",
            show_default=False,
            metavar="TEXT",
        ),
    ],
    font: Annotated[
        str,
        typer.Option(
            "--font",
            "-f",
            help="Font to use for text art (e.g., 'slant', 'big', 'standard').",
        ),
    ] = "standard",
):
    """
    CLI command to generate ASCII art from text.
    """
    if not text.strip():
        typer.secho(
            "Error: Text string cannot be empty.", fg=typer.colors.RED, file=sys.stderr
        )
        raise typer.Exit(code=1)

    ascii_art = generate_text_art(text, font)

    if ascii_art.startswith("Error:"):
        typer.secho(ascii_art, fg=typer.colors.YELLOW, file=sys.stderr)
        raise typer.Exit(code=1)
    else:
        print(ascii_art)


if __name__ == "__main__":
    app()
