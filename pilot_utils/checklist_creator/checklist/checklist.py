from pilot_utils.checklist_creator.checklist import ChecklistSection, ChecklistConfiguration

class Checklist:
    def __init__(self,
                 aircraft_type: str = None,
                 checklist_type: str = None,
                 checklist_version: str = '1.0.0',
                 real_world_clearance: bool = False,
                 background_coloring: bool = False
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
                real_world_clearance (bool):
                    Whether the checklist should be used in the real-world.
                    Defaults to False
                background_coloring (bool):
                    Whether the checklist's background should colored
                    alternatingly. Defaults to False
        """
        self.aircraft_type = aircraft_type
        self.checklist_type = checklist_type
        self.checklist_version = checklist_version
        self.real_world_clearance = real_world_clearance
        self.background_coloring = background_coloring
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


    def add_section_at_index(self,
                             index: int,
                             section: ChecklistSection
                             ):
        """
            Adds the given section at the provided index and recalculates
            the indices for all following sections
        """
        section.number_in_sequence = index + 1
        self.sections.insert(index, section)
        for idx in range(index + 1, len(self.sections)):
            self.sections[idx].number_in_sequence = idx + 1
        self.sections_sequence_head = len(self.sections)
