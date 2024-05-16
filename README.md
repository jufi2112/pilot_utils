# PDF Merger
Merging and Arranging of PDFs.

Merges all PDFs in a specified directory and aranges them such that two original pages will be on a new landscape-oriented page. If there is an uneven number of pages, ignores the last page.

## Use Case
Arrange downloaded pages from the German [AIP](https://aip.dfs.de/BasicVFR) to a format that better suits a kneeboard. We support both landscape and portrait oriented PDFs.

## Requirements
A somewhat recent version of Python3 and PyPDF. We tested with Python 3.7.9 and PyPDF 4.2.0

You can install the newest PyPDF version using `pip install pypdf` in the shell that you also use to run python scripts.

To install all requirements into the currently active Python, you can run `pip install -r requirements.txt` from this directory.

## Usage
1. Download your required PDFs (e.g. from the German AIP website) to a common directory.
2. Open your favorite shell that can run Python and navigate to the directory in which `pdf_merger.py` is located
3. Run `python pdf_merger.py` with the following options:

| Option | Argument | Description |
| ------ | -------- | ----------- |
| -i / --input-dir | string | The path to the directory in which the pdf files are located that you want to merge and arrange |
| -o / --output-dir | string | The path to the directory where the output should be saved to. If not provided, uses the same directory as --input-dir |
| --merged-name | string | The name that should be given to the merged pdf file. If not provided, uses 'merged.pdf' |
| --arranged-name | string | The name that should be given to the arranged pdf file. If not provided, uses 'arranged.pdf' |
| --allow-overwriting | - | If provided, allows the program to overwriting existing files in the output directory that have the same name as --merged-name and --arranged-name |
| --remove-temp-files | - | If provided, removes the merged file after the program has finished. |
| --no-arrange | - | If provided, the program will just merge the PDFs without arranging them |

For example
```bash
python pdf_merger.py -i /path/to/aip/EDAU
```
which will merge all PDFs in `/path/to/aip/EDAU` to a file `/path/to/aip/EDAU/merged.pdf` and arranges them for kneeboard use in a file `/path/to/aip/EDAU/arranged.pdf` that you can then print.
