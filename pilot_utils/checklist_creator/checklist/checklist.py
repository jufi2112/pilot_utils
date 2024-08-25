from pilot_utils.checklist_creator.checklist import ChecklistSection, ChecklistConfiguration

class Checklist:
    def __init__(self,
                 aircraft_type: str = None,
                 checklist_type: str = None,
                 checklist_version: str = '1.0.0'
                 ):
        """
            A class that represents a checklist.

            Params
            ------
                aircraft_type (str):
                    Type of the aircraft. Is shown in the header
                checklist_type (str):
                    Type of the checklist. Is shown in the header
                checklist_version (str):
                    Version of the checklist. Defaults to '1.0.0'
        """
        self.aircraft_type = aircraft_type
        self.checklist_type = checklist_type
        self.checklist_version = checklist_version
        self.sections = []
        self.sections_sequence_head = 1
        self.checklist_config = ChecklistConfiguration()


    def append_section(self,
                       section: ChecklistSection
                       ):
        """
            Appends the given section to this checklist
        """
        section.number_in_sequence = self.sections_sequence_head
        self.sections_sequence_head += 1
        self.sections.append(section)
