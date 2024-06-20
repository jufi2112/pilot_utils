import os

from typing import Dict
from os import path as osp

class ChecklistParser:
    def __init__(self, fpath: str):
        """
            Parses the given checklist to a dictionary that can be used
            further down the pipeline

        Params
        ------
            fpath (str):
                Path to the checklist that should be parsed
        """
        if not osp.isfile(fpath):
            raise ValueError(f"The provided path is not a valid file: {fpath}")
        self.fpath = fpath


    def parse(self) -> Dict:
        """
            Parses the checklist file
        """
        with open(self.fpath, 'r') as file:
            content = file.readlines()
        cl = {}
        current_section_idx = -1
        current_item_idx = -1
        current_subitem_idx = -1
        for ln, line in enumerate(content):
            line = self._sanitize(line)
            if line.startswith('#'):
                # New section
                current_section_idx += 1
                current_item_idx = -1
                section_name = line[1:].strip()
                cl[current_section_idx] = {
                    'name': section_name,
                    'content': {}
                }
            elif line.startswith('-'):
                # New item in the current section
                current_item_idx += 1
                current_subitem_idx = -1
                if '..' not in line[1:]:
                    item = self._sanitize(line[1:])
                    value = None
                else:
                    item, value = line[1:].split("..", 1)
                    item = self._sanitize(item)
                    value = self._sanitize(value)
                cl[current_section_idx]['content'][current_item_idx] = {
                    'left': item,
                    'right': value,
                    'content': {}
                }
            elif line.startswith('+'):
                # New subitem of the current item in the current section
                current_subitem_idx += 1
                if current_item_idx == -1:
                    raise ValueError(f"Line {ln+1}: Encountered a new subitem definition (+) before the first item of section {cl[current_section_idx]['name']} was defined!")
                if '..' not in line[1:]:
                    item = self._sanitize(line[1:])
                    value = None
                else:
                    item, value = line[1:].split("..", 1)
                    item = self._sanitize(item)
                    value = self._sanitize(value)
                cl[current_section_idx]['content'][current_item_idx]['content'][current_subitem_idx] = {
                    'left': item,
                    'right': value,
                    'content': {}
                }
        return cl


    def _sanitize(self, s: str) -> str:
        """
            Removes leading and trailing whitespaces from the given string

        Params
        ------
            s (str):
                String which should be sanitized
        """
        return s.strip()
