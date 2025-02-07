from typing import Union
from pilot_utils.checklist_creator.checklist import CenteredText

class SectionItem:
    def __init__(self,
                 text_left: str = None,
                 text_right: str = None,
                 left_bold: bool = False,
                 right_bold: bool = True,
                 ignore_in_sequence: bool = False
                 ):
        """
            Class that represents one item in a section of a
            checklist.

            Params
            ------
                text_left (str):
                    Text on the left side of the checklist
                text_right (str):
                    Text on the right side of the checklist
                left_bold (bool):
                    Whether the text on the left side should be
                    printed bold
                right_bold (bool):
                    Whether the text on the right side should be
                    printed bold
                ignore_in_sequence (bool):
                    Whether this item should be ignored when enumerating
                    items
        """
        self.text_left = text_left
        self.is_left_bold = left_bold
        self.text_right = text_right
        self.is_right_bold = right_bold
        self.number_in_sequence = None
        self.ignore_in_sequence = ignore_in_sequence
        self.subitems = []
        self.subitems_sequence_head = 1


    def append_subitem(self,
                       subitem: Union['SectionItem', CenteredText]
                       ) -> None:
        """
            Appends the given item to the list of subitems of this item.

        Params
        ------
            subitem (SectionItem or CenteredText):
                The subitem that should be appended to this item
        """
        if isinstance(subitem, CenteredText):
            self.subitems.append(subitem)
            return
        if not subitem.ignore_in_sequence:
            subitem.number_in_sequence = self.subitems_sequence_head
            self.subitems_sequence_head += 1
        self.subitems.append(subitem)
