import os
import argparse

from os import path as osp
from reportlab.pdfgen import canvas
from typing import Dict, Tuple, Union
from reportlab.lib.pagesizes import A5

from pilot_utils.checklist_creator import ChecklistParser
from pilot_utils.checklist_creator.checklist import Checklist, ChecklistSection, SectionItem, CenteredText, ChecklistConfiguration


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
        if not osp.isdir(output_dir):
            os.makedirs(output_dir)
        if osp.splitext(output_name)[1] != '.pdf':
            output_name = output_name + ".pdf"

        config = checklist.checklist_config

        c = canvas.Canvas(osp.join(output_dir, output_name),
                          pagesize=config.page_size)

        page_width, page_height = config.page_size
        page_number = 1

        self._apply_header_and_footer_to_page(c, config, checklist.aircraft_type,
                                              checklist.checklist_type, checklist.checklist_version,
                                              page_number)
        current_y_position = page_height - config.border_top - config.space_after_header

        section_id: int = 0
        while (section_id < len(checklist.sections)):
        #for section in checklist.sections:
            section: ChecklistSection = checklist.sections[section_id]
            # Check whether section fits onto current page
            if not self._does_section_fit_onto_page(section, config, current_y_position):
                # Create new page
                c.showPage()
                page_number += 1
                self._apply_header_and_footer_to_page(c, config, checklist.aircraft_type,
                                                      checklist.checklist_type, checklist.checklist_version,
                                                      page_number)
                current_y_position = page_height - config.border_top - config.space_after_header
            if not self._does_section_fit_onto_page(section, config, current_y_position):
                # Splits current section and returns it, puts new section into checklist after current section
                section = self._split_section_to_fit_on_page(checklist,
                                                             section_id,
                                                             current_y_position)
            # Write section onto page starting at current_y_position
            current_y_position = self._print_section_to_canvas(c,
                                                               section,
                                                               config,
                                                               current_y_position)
            # After last element of header, current_y_position is at position for next item,
            # but we want it to be at position for next section
            current_y_position += config.space_between_items
            current_y_position -= config.space_between_sections
            section_id += 1
        # Save PDF
        c.save()


    def _print_section_to_canvas(self,
                                 canvas: canvas.Canvas,
                                 section: ChecklistSection,
                                 config: ChecklistConfiguration,
                                 current_y_position: int,
                                 ) -> int:
        """
            Prints the given section to the canvas using the provided
            configuration and starting at the provided y position.

        Returns
        -------
            int:
                The next y position after the section at which text can be drawn
        """
        # Draw section name
        canvas.setFont(config.font_name_section_name, config.font_size_section_name)
        canvas.drawString(config.border_left, current_y_position, section.name)
        current_y_position -= config.space_section_to_item
        # Draw items
        for item in section.items:
            current_y_position = self._print_item_to_canvas(canvas,
                                                            item,
                                                            config,
                                                            current_y_position,
                                                            0)
        return current_y_position


    def _print_item_to_canvas(self,
                              canvas: canvas.Canvas,
                              item: Union[SectionItem, CenteredText],
                              config: ChecklistConfiguration,
                              current_y_position: int,
                              x_offset_left_border: int,
                              ) -> int:
        """
            Prints the given item onto the canvas starting at the
            given y position, respecting the provided x offset, and
            using the provided configuration.

            Params
            ------
                canvas (canvas.Canvas):
                    The canvas onto which the item should be printed
                item (SectionItem or CenteredText):
                    The item that should be printed
                config (ChecklistConfiguration):
                    The configuration
                current_y_position (int):
                    Y position onto which the item should be written
                x_offset_left_border (int):
                    Horizontal offset from the left border which should
                    be kept clear. Can be used for indentations.

        Returns
        -------
            int:
                The next y position onto which can be written
        """
        page_width, page_height = config.page_size
        # Handle case of CenteredText
        if isinstance(item, CenteredText):
            text_width = canvas.stringWidth(item.text,
                                            config.font_name_bold_item if item.is_bold else config.font_name_item,
                                            config.font_size_item)
            x_middle = (page_width - config.border_right - config.border_left) // 2 + config.border_left
            canvas.setFont(config.font_name_bold_item if item.is_bold else config.font_name_item,
                           config.font_size_item)
            canvas.drawString(x_middle - (text_width // 2), current_y_position, item.text)
            return current_y_position - config.space_between_items
        # We have a SectionItem
        current_x_position = config.border_left + x_offset_left_border
        if item.ignore_in_sequence or item.number_in_sequence is None:
            enum = ""
        else:
            # First-level item, numerical enumeration
            if x_offset_left_border == 0:
                enum = f"{item.number_in_sequence}."
            # Second-level item, alphabetical enumeration
            else:
                enum = f"{chr(ord('`') + item.number_in_sequence)}."
        canvas.setFont(config.font_name_item, config.font_size_item)
        canvas.drawString(current_x_position, current_y_position, enum)
        current_x_position += config.space_for_enumerations
        # Calculate sizes of text
        text_left_width = canvas.stringWidth(item.text_left,
                                             config.font_name_bold_item if item.is_left_bold else config.font_name_item,
                                             config.font_size_item) if item.text_left is not None else 0
        text_right_width = canvas.stringWidth(item.text_right,
                                              config.font_name_bold_item if item.is_right_bold else config.font_name_item,
                                              config.font_size_item) if item.text_right is not None else 0
        # Draw left text
        if item.text_left is not None:
            canvas.setFont(config.font_name_bold_item if item.is_left_bold else config.font_name_item,
                           config.font_size_item)
            canvas.drawString(current_x_position, current_y_position, item.text_left)
            current_x_position += text_left_width
        # Draw right text
        if item.text_right is not None:
            canvas.setFont(config.font_name_bold_item if item.is_right_bold else config.font_name_item,
                           config.font_size_item)
            canvas.drawRightString(page_width - config.border_right, current_y_position, item.text_right)
        # Draw connecting dots
        if item.text_left is not None and item.text_right is not None:
            text_dots_width = page_width - config.border_right - text_right_width - current_x_position
            text_dots = '.' * int(text_dots_width / canvas.stringWidth('.', config.font_name_item, config.font_size_item))
            # Replace first and last dot with space if we have non-empty text so that we have a small separation
            if item.text_left != "":
                text_dots = " " + text_dots[1:]
            if item.text_right != "":
                text_dots = text_dots[:-1] + " "
            canvas.setFont(config.font_name_item, config.font_size_item)
            canvas.drawString(current_x_position, current_y_position, text_dots)
        current_y_position -= config.space_between_items
        # Draw subitems
        for subitem in item.subitems:
            current_y_position = self._print_item_to_canvas(canvas,
                                                            subitem,
                                                            config,
                                                            current_y_position,
                                                            x_offset_left_border + config.space_for_enumerations)
        return current_y_position


    def _apply_header_and_footer_to_page(self,
                                         canvas: canvas.Canvas,
                                         config: ChecklistConfiguration,
                                         aircraft_type: str,
                                         checklist_type: str,
                                         checklist_version: str,
                                         page_number: int,
                                         ):
        """
            Applies header and footer to the current page of the PDF.
        """
        page_width, page_height = config.page_size
        canvas.setFont(config.font_name_header_footer, config.font_size_header_footer)
        canvas.drawString(config.border_left, page_height - config.border_top, aircraft_type)
        canvas.drawRightString(page_width - config.border_right, page_height - config.border_top, checklist_type)
        canvas.drawRightString(page_width - config.border_right, config.border_bottom, f"Page {page_number}")
        canvas.drawString(config.border_left, config.border_bottom, f"Version {checklist_version}")
        if not config.real_world_clearance:
            text = "----- For Simulator Use Only -----"
            text_width = canvas.stringWidth(text, config.font_name_header_footer, config.font_size_header_footer)
            x_middle = (page_width - config.border_right - config.border_left) // 2 + config.border_left
            canvas.drawString(x_middle - (text_width // 2), config.border_bottom, text)


    def _does_section_fit_onto_page(self,
                                    section: ChecklistSection,
                                    config: ChecklistConfiguration,
                                    current_y_position: int
                                    ) -> bool:
        """
            Determines whether the given section fits onto a page starting
            at a given y position with the given configuration
        """
        # Space between section name and first item
        final_y_position = current_y_position - config.space_section_to_item
        if section.description is not None:
            raise NotImplementedError("Section descriptions are currently not supported!")
        for item in section.items:
            final_y_position -= config.space_between_items
            if isinstance(item, SectionItem):
                final_y_position -= (len(item.subitems) * config.space_between_items)
        # The last element does not need spacing between items, so remove it
        final_y_position += config.space_between_items
        return final_y_position > (config.border_bottom + config.font_size_header_footer + config.space_before_footer)


    def _split_section_to_fit_on_page(self,
                                      checklist: Checklist,
                                      section_id: int,
                                      current_y_position: int
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
                current_y_position (int):
                    Current y position on the page

            Returns
            -------
                ChecklistSection:
                    The current section split such that it fits onto the page
        """
        current_section: ChecklistSection = checklist.sections[section_id]
        section_name: str = current_section.name
        config = checklist.checklist_config
        split_y_position = current_y_position
        y_end: int = config.border_bottom + config.font_size_header_footer + config.space_before_footer

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
