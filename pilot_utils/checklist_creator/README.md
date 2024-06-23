# Checklist Creator
Create a printable checklist from a simple text document.

## Use Case
Ever wanted to create a checklist without having to do all the formatting by yourself?

## Checklist Text File Syntax
Create a new text document (`.txt` file) and use the following formatting:
| Command            | Meaning                                                                                                                                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       # Name       | Create a new section with name "Name"                                                                                                                                                                          |
| - Left .. Right    | Create a new item with text "Left" and "Right" on left and right side, respectively. The item is enumerated using numbers starting from 1, both text sides are connected via dots and "Right" is printed bold. |
| - Left             | Create a new item with text "Left" on the left side and without any right text or dots.                                                                                                                        |
| + Left .. Right    | Create a new subitem. Same as - command, but indented by one level and enumerated using lowercase alphabet a-z                                                                                                 |
| + Left             | Same as - option but with properties of the + command above                                                                                                                                                    |
| * Left             | Create a new subitem with "Left" on the left side in bold, without any right side, and enumerated a-z                                                                                                          |
| ** Left            | Same as * option above, but without enumeration                                                                                                                                                                |
| = Text             | Create a centered text in bold, no enumeration                                                                                                                                                                 |
| // Setting = Value | Overwrittes the default value of property "Setting" with the provided Value. Everything is case sensitive. Possible properties can be found in `checklist/configuration.py`                                    |

You can also check out the example C700.txt and corresponding C700.pdf files.

## Usage
```shell
python checklist_creator.py --input .\example.txt --output .\example.pdf
```
