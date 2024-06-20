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
        current_section_name = None
        current_item_name = None
        for ln, line in enumerate(content):
            line = self._sanitize(line)
            if line.startswith('#'):
                # New section
                section_name = line[1:].strip()
                if section_name in cl.keys():
                    raise ValueError(f"Line {ln+1}: The section name {section_name} already appears in the checklist")
                cl[section_name] = {}
                current_section_name = section_name
                current_item_name = None
            elif line.startswith('-'):
                # New item in the current section
                item, value = line[1:].split("..", 1)
                item = self._sanitize(item)
                value = self._sanitize(value)
                if item in cl[current_section_name].keys():
                    raise ValueError(f"Line {ln+1}: Item {item} is already present in section {current_section_name}")
                cl[current_section_name][item] = (value, {})
                current_item_name = item
            elif line.startswith('+'):
                # New subitem of the current item in the current section
                if current_item_name is None:
                    raise ValueError(f"Line {ln+1}: Encountered a new subitem definition (+) before the first item of section {current_section_name} was defined!")
                item, value = line[1:].split("..", 1)
                item = self._sanitize(item)
                value = self._sanitize(value)
                cl[current_section_name][current_item_name][1][item] = (value, {})
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
