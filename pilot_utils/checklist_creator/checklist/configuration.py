from typing import Dict, Union
from reportlab.lib.pagesizes import A5

page_sizes_dict = {'A5': A5}

class ChecklistConfiguration:
    def __init__(self):
        """
            Class that contains all configuration values
            and defaults for them.
        """
        # Border margins
        self.border_left = 80
        self.border_right = 50
        self.border_top = 80
        self.border_bottom = 80
        # Fonts and font sizes
        self.font = "Helvetica"
        self.font_bold = "Helvetica-Bold"
        self.font_size_section = 9
        self.font_size_item = 6
        # Space between different elements
        self.space_after_header = 30
        self.space_between_sections = 32
        self.space_section_to_item = 20
        self.space_between_items = 12
        self.space_for_enumerations = 10
        # Page size
        self.page_size = page_sizes_dict["A5"]


    def update_configuration(self,
                             new_config: Dict[str, Union[int, str]],
                             print_missing_elements: bool = True
                             ):
        """
            Updates the configuration with values from the provided dictionary.
            Attributes that are not present in the configuration are ignored and
            printed at the end if print_missing_elements is True.

        Params
        ------
            new_config (Dict[str, Union[int, str]]):
                Dictionary that contains the new configuration values
            print_missing_elements (bool):
                Whether configuration elements from new-config that were ignored
                should be printed at the end. Defaults to True
        """
        missing_elements = []
        for key, value in new_config.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                missing_elements.append(key)
        if print_missing_elements and len(missing_elements) > 0:
            print(f"The following configuration elements were ignored: {missing_elements}")
