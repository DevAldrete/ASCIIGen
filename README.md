# ASCII Generator

A simple ASCII Generator for images and text. Built with the purpose of being used as CLI.

You can download and use this project in this way:

1. Clone the repository:

```
git clone git@github.com:DevAldrete/ASCIIGen.git
```

2. Download dependencies:

- Using UV (Recommended):

```
uv sync
```

- Using pip:

```
pip install -r requirements.txt
```

3. Run the program:

- Using UV:

```
uv pip install -e .
```

- Using pip:

```
pip install -e .
```

That's it! You can now use the ASCII Generator from your command line.

Example usage:

- Images:

```
asciigen image "path_to_image.jpg" --width 100
```

- Texts:

```
asciigen text "Hello, World!" --font standard
```
