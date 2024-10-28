import os
import argparse

from os import path as osp
from reportlab.pdfgen import canvas
from typing import Dict, Tuple, Union
from reportlab.lib.pagesizes import A5

from pilot_utils.checklist_creator import ChecklistParser
from pilot_utils.checklist_creator.checklist import Checklist, ChecklistSection, SectionItem, CenteredText, ChecklistConfiguration, PDFManager


class PDFChecklistCreator:
    """
        Class that creates a formatted PDF checklist from a text file.
    """
    def format_checklist(self,
                         checklist: Checklist,
                         output_dir: str,
                         output_name: str
                         ):
        """
            Formats the given checklist into a PDF at the desired location.

        Params
        ------
            checklist (Checklist):
                The checklist object as created by the CheckListParser class
            output_dir (str):
                Desired output directory
            output_name (str):
                Desired output filename
        """
        config = checklist.checklist_config

        pdf = PDFManager(config,
                         output_dir,
                         output_name,
                         checklist.aircraft_type,
                         checklist.checklist_type,
                         checklist.checklist_version,
                         checklist.real_world_clearance)

        section_id: int = 0
        while (section_id < len(checklist.sections)):
            section: ChecklistSection = checklist.sections[section_id]
            # Check whether section fits onto current page
            if not pdf.section_fits_page(section):
                # Create new page
                pdf.add_page()
            if not pdf.section_fits_page(section):
                # Splits current section and returns it, puts new section into checklist after current section
                section = self._split_section_to_fit_on_page(checklist,
                                                             section_id,
                                                             pdf)
            # Write section onto page starting at current_y_position
            pdf.print_section_to_current_page(section)
            # After last element of section, current_y_position is at position for next item,
            # but we want it to be at position for next section
            pdf.finish_section()
            section_id += 1
        # Save PDF
        pdf.save_pdf()


    def _split_section_to_fit_on_page(self,
                                      checklist: Checklist,
                                      section_id: int,
                                      pdf: PDFManager
                                      ) -> ChecklistSection:
        """
            Splits the section with the given ID such that it fits onto a page.
            Potentially split sections are added to the checklist directly after the
            split section

            Params
            ------
                checklist (Checklist):
                    The overall checklist where newly split sections are to be added
                section_id (int):
                    ID of the section to potentially split
                pdf (PDFManager):
                    The PDF manager instance

            Returns
            -------
                ChecklistSection:
                    The current section split such that it fits onto the page
        """
        current_section: ChecklistSection = checklist.sections[section_id]
        section_name: str = current_section.name
        config = checklist.checklist_config
        split_y_position = pdf.current_y_position
        y_end: int = pdf.y_limit_bottom

        # 1. Find out the index on which the section has to be split in order to still fit onto the page
        split_index = self._get_section_splitting_point(current_section, config, split_y_position, y_end)

        # 2. Split items and put remainder in new section
        items_new_section = current_section.items[split_index:]
        if len(items_new_section) > 0:
            current_section.items = current_section.items[:split_index]
            current_section.items_sequence_head = len(current_section.items) + 1
            if section_name[-12:] == ' - CONTINUED':
                new_name = section_name
            else:
                new_name = section_name + " - CONTINUED"
            new_section = ChecklistSection(new_name, None, len(current_section.items) + current_section.item_numbering_offset)
            for item in items_new_section:
                new_section.append_item(item)

            # 3. Add new section to checklist
            checklist.add_section_at_index(current_section.number_in_sequence, new_section)
        return current_section


    def _get_section_splitting_point(self,
                                     section: ChecklistSection,
                                     config: ChecklistConfiguration,
                                     y_start: int,
                                     y_end: int
                                     ) -> int:
        """
            Returns the index at which the provided section has be to split
            in order for it to fit onto the page determined by y_start and y_end.
            If all items fit on page, the length of the item list is returned.

            Params
            ------
                section (ChecklistSection):
                    Section from which the items should be taken
                config (ChecklistConfiguration):
                    Checklist configuration
                y_start (int):
                    Height at which first item should start
                y_end (int):
                    Height which should not be overflown by items

            Returns
            -------
                int: Index of the last item that fits onto the page
        """
        current_y = y_start
        for item_idx in range(len(section.items)):
            if item_idx == 0:
                current_y -= config.space_section_to_item
            else:
                current_y -= config.space_between_items
            if isinstance(section.items[item_idx], SectionItem):
                current_y -= (len(section.items[item_idx].subitems) * config.space_between_items)
            if current_y < y_end:
                return item_idx
        return len(section.items)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a PDF checklist from a .txt file")
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the input txt file that should be converted to a pdf checklist")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output path. If no filename is provided, uses the same filename as the input file.")
    args = parser.parse_args()
    if not osp.isfile(args.input):
        raise ValueError(f"-i/--input option is not a valid file!")
    input_fname = osp.splitext(osp.basename(args.input))[0]
    output_path, output_file = osp.split(args.output)
    if output_file == "":
        output_file = input_fname + ".pdf"
    elif osp.splitext(output_file)[1] != '.pdf':
        output_file = output_file + '.pdf'
    p = ChecklistParser(args.input)
    cl = p.parse()

    checklist_creator = PDFChecklistCreator()
    checklist_creator.format_checklist(cl, output_path, output_file)
