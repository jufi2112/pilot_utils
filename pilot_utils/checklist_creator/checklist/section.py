from typing import Union
from pilot_utils.checklist_creator.checklist import CenteredText, SectionItem

class ChecklistSection:
    def __init__(self,
                 section_name: str,
                 section_description: str
                 ):
        """
            Class that represents a section of a checklist
        """
        self.name = section_name
        self.description = section_description
        self.items = []
        self.items_sequence_head = 1
        self.number_in_sequence = None


    def append_item(self,
                    item: Union[CenteredText, SectionItem]
                    ):
        """
            Appends the given element to this section's list of items.

        Params
        ------
            item (SectionItem or CenteredText):
                The element that should be appended to this section
        """
        if isinstance(item, CenteredText):
            self.items.append(item)
            return
        if not item.ignore_in_sequence:
            item.number_in_sequence = self.items_sequence_head
            self.items_sequence_head += 1
        self.items.append(item)
