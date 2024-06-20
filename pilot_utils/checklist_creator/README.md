# Checklist Creator
Create a printable checklist from a simple text document.

## Use Case
Ever wanted to create a checklist without having to do all the formatting by yourself?

## Usage
Create a new text document (`.txt` file) and use the following formatting:
1. To indicate a new section, prefix the section name with a `#`, e.g. `# Cockpit Inspection`
2. To create items and their associated action, start the line with a minus `-` and use two dots `..` to separate them, e.g. `- LANDING GEAR Handle .. DOWN`
    - The items will be automatically numbered
3. If you want to add subitems, start the line with a plus `+` and proceed as above
    - The subitems will automatically be itemized using letters a-z
4. If you don't want to provide an action but just print an item (e.g. an `---OR---` separator) in bold, leave out the `..`

You can also check out the example.txt and example.pdf checklists.