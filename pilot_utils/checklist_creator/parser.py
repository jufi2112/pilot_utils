import os

from typing import Dict
from os import path as osp

from pilot_utils.checklist_creator.checklist import Checklist, ChecklistSection, SectionItem, CenteredText

class ChecklistParser:
    def __init__(self, fpath: str):
        """
            Parses the given checklist to a Checklist object

        Params
        ------
            fpath (str):
                Path to the checklist that should be parsed
        """
        if not osp.isfile(fpath):
            raise ValueError(f"The provided path is not a valid file: {fpath}")
        self.fpath = fpath
        self.checklist = None


    def parse(self) -> Checklist:
        """
            Parses the checklist file

        Returns
        -------
            Checklist:
                The parsed checklist object.
        """
        with open(self.fpath, 'r') as file:
            content = file.readlines()

        self.checklist = Checklist()
        checklist_config = {}

        current_section = None
        current_item = None
        current_subitem = None

        for line_nbr, line in enumerate(content):
            # Check for checklist configuration item
            if line.startswith("//"):
                line = line[2:].strip()
                try:
                    config_key, config_value = line.split('=', 1)
                except ValueError:
                    print(f"Encountered an invalid checklist configuration instruction in line {line_nbr+1}, ignoring it")
                    continue
                config_key = config_key.strip()
                config_value = config_value.strip()
                checklist_config[config_key] = config_value

            # Check for new section
            elif line.startswith("#"):
                line = line[1:].strip()
                # Check whether we have to "close" a previous subitem
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Check whether we have to "close" a previous item
                if current_item is not None:
                    current_section.append_item(current_item)
                # Check whether we have to "close" a previous section
                if current_section is not None:
                    self.checklist.append_section(current_section)
                # Create new section
                sectrion_description = None # we do not support section descriptions at the moment
                current_section = ChecklistSection(line, sectrion_description)
                current_item = None
                current_subitem = None

            # Check for new item
            elif line.startswith("-"):
                line = line[1:].strip()

                if current_section is None:
                    raise ValueError(f"Line {line_nbr+1}: Found item definition before section definition!")

                # Check whether we have to "close" a previous subitem
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Check whether we have to "close" a previous item
                if current_item is not None:
                    current_section.append_item(current_item)
                # Parse the item
                if '..' not in line:
                    text_left = line
                    text_right = None
                else:
                    text_left, text_right = line.split('..', 1)
                    text_left = text_left.strip()
                    text_right = text_right.strip()
                # Create new item with parsed information
                current_item = SectionItem(text_left, text_right, False, True, False)
                current_subitem = None

            # Check for new sub-item
            elif line.startswith('+'):
                line = line[1:].strip()

                if current_item is None:
                    raise ValueError(f"Line {line_nbr+1}: Found sub-item definition before item definition!")

                # Check whether we have to "close" a previous sub-item
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Parse the subitem
                if '..' not in line:
                    text_left = line
                    text_right = None
                else:
                    text_left, text_right = line.split('..', 1)
                    text_left = text_left.strip()
                    text_right = text_right.strip()
                # Create new subitem with parsed information
                current_subitem = SectionItem(text_left, text_right, False, True, False)

            # Check for new sub-item with left only in bold, not enumerated
            elif line.startswith('**'):
                line = line[2:].strip()

                if current_item is None:
                    raise ValueError(f"Line {line_nbr+1}: Found sub-item definition before item definition!")

                # Check whether we have to "close" a previous sub-item
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Create new subitem
                current_subitem = SectionItem(line, None, True, False, True)

            # Check for new sub-item with left only in bold, enumerated
            elif line.startswith('*'):
                line = line[1:].strip()

                if current_item is None:
                    raise ValueError(f"Line {line_nbr+1}: Found sub-item definition before item definition!")

                # Check whether we have to "close" a previous sub-item
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Create new subitem
                current_subitem = SectionItem(line, None, True, False, False)

            # Check for centered line
            elif line.startswith('='):
                line = line[1:].strip()

                # Check whether we have to "close" a previous sub-item
                if current_subitem is not None:
                    current_item.append_subitem(current_subitem)
                # Create new centered text and treat it as subitem
                current_subitem = CenteredText(line, True)

        # We've iterated all lines, "close" all remaining elements
        if current_subitem is not None:
            current_item.append_subitem(current_subitem)
            current_subitem = None
        if current_item is not None:
            current_section.append_item(current_item)
            current_item = None
        if current_section is not None:
            self.checklist.append_section(current_section)
            current_section = None

        # Read out aircraft and checklist type from config
        if "Aircraft Type" in checklist_config.keys():
            self.checklist.aircraft_type = checklist_config["Aircraft Type"]
            del checklist_config["Aircraft Type"]
        if "Checklist Type" in checklist_config.keys():
            self.checklist.checklist_type = checklist_config["Checklist Type"]
            del checklist_config["Checklist Type"]
        if "Checklist Version" in checklist_config.keys():
            self.checklist.checklist_version = checklist_config["Checklist Version"]
            del checklist_config["Checklist Version"]
        if "Real World Clearance" in checklist_config.keys():
            self.checklist.real_world_clearance = True if checklist_config["Real World Clearance"].lower() == "True" else False
            del checklist_config["Real World Clearance"]
        # Update checklist configuration with remaining settings
        self.checklist.checklist_config.update_configuration(checklist_config, True)
        return self.checklist
