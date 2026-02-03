# static-site-generator
A static site generator written in Python. This project is designed to generate static websites from Markdown files. This personal project allowed me to learn more about Object Oriented programming within Python and also allowed me to learn more about Python's built-in libraries for file I/O and how to use them to create a useful tool.

## Setup
The site generator pulls markdown content from the `content` directory. To set up the site generator, you need to create a `content` directory and add your markdown files to it in the desired stucture. Any static files such as images or CSS files should be placed in the `static` directory. The directory structure will be copied from both `content` and `static` directories.

## Running
To run the static site generator, you need to have Python installed on your system. Once you have Python installed, you can run the generator with the following command:

```
./main.sh
```
script will launch http server on port 8000

## Testing

Unit tests can be run withthe following command:

```
./test.sh
```
