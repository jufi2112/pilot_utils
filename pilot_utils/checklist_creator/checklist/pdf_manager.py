from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from pilot_utils.checklist_creator.checklist import ChecklistSection, ChecklistConfiguration, SectionItem, CenteredText
import os
from os import path as osp
from typing import Union

class PDFManager:
    def __init__(self,
                 config: ChecklistConfiguration,
                 output_dir: str,
                 output_name: str,
                 aircraft_type: str,
                 checklist_type: str,
                 checklist_version: str,
                 real_world_clearance: bool,
                 show_page_numbers: bool = True
                 ):
        """
            Class that manages the pdf document.

            Params
            ------
                config (ChecklistConfiguration):
                    Configuration file for the checklist
                output_dir (str):
                    Output directory
                output_name (str):
                    Output file name
                aircraft_type (str):
                    Type of aircraft
                checklist_type (str):
                    Type of checklist
                checklist_version (str):
                    Version of the checklist
                real_world_clearance (bool):
                    Whether the checklist is meant for real-world usage
                show_page_numbers (bool):
                    Whether page numbering should be shown. Defaults to True.
        """
        self.page_width, self.page_height = config.page_size
        self.current_page = 0
        self.y_header = self.page_height - config.border_top
        self.y_footer = config.border_bottom
        self.y_limit_bottom = config.border_bottom + config.font_size_header_footer + config.space_before_footer
        self.y_limit_top = self.page_height - config.border_top - config.space_after_header
        self.x_limit_left = config.border_left
        self.x_limit_right = self.page_width - config.border_right
        self.current_y_position = self.y_limit_top
        self.aircraft_type = aircraft_type
        self.checklist_type = checklist_type
        self.checklist_version = checklist_version
        self.real_world_clearance = real_world_clearance
        self.show_page_numbers = show_page_numbers
        self.config = config

        if not osp.isdir(output_dir):
            os.makedirs(output_dir)
        if osp.splitext(output_name)[1] != '.pdf':
            output_name += '.pdf'

        self.canvas = canvas.Canvas(osp.join(output_dir, output_name),
                                    pagesize=config.page_size)
        self.add_page()


    def finish_section(self):
        """
            Performs clean up after a section has been finished.
            After last element of section, current_y_position is at position for next item,
            but we want it to be at position for next section
        """
        self.current_y_position += self.config.space_between_items
        self.current_y_position -= self.config.space_between_sections


    def save_pdf(self):
        """Saves the PDF."""
        self.canvas.save()


    def print_section_to_current_page(self,
                                      section: ChecklistSection
                                      ) -> bool:
        """
            Prints the given section onto the current page.

            Params
            ------
                section (ChecklistSection):
                    The section that should be printed onto the page

            Returns
            -------
                bool:
                    Whether operation was successful. If False,
                    consider adding a new page and trying again.
        """
        if not self.section_fits_page(section):
            return False
        # Draw section name
        self.canvas.setFont(self.config.font_name_section_name, self.config.font_size_section_name)
        self.canvas.drawString(self.x_limit_left, self.current_y_position, section.name)
        self.current_y_position -= self.config.space_section_to_item
        # Draw items
        for item in section.items:
            self._print_item_to_page(item, 0)


    def _print_item_to_page(self,
                            item: Union[SectionItem, CenteredText],
                            x_offset_left_border: int
                            ):
        """
            Prints the given item (and potential subitems) to the current page.
            No check as to whether the item will fit onto the page is performed.

            Params
            ------
                item (SectionItem or CenteredText):
                    Item that should be printed to the current page
                x_offset_left_border (int):
                    Offset to the left border at which printing should take place.
        """
        # Handle case of CenteredText
        if isinstance(item, CenteredText):
            self.canvas.setFont(self.config.font_name_bold_item if item.is_bold else self.config.font_name_item,
                                self.config.font_size_item)
            text_width = self.canvas.stringWidth(item.text,
                                                 self.config.font_name_bold_item if item.is_bold else self.config.font_name_item,
                                                 self.config.font_size_item)
            self.canvas.drawString(self._get_centered_text_x(text_width), self.current_y_position, item.text)
            self.current_y_position -= self.config.space_between_items
            return
        # We have a section item
        current_x_position = self.x_limit_left + x_offset_left_border
        if item.ignore_in_sequence or item.number_in_sequence is None:
            enum = ""
        else:
            # First-level item, numberical enumeration
            if x_offset_left_border == 0:
                enum = f"{item.number_in_sequence}."
            # Second-level item, alphabetical enumeration
            else:
                enum = f"{chr(ord('`') + item.number_in_sequence)}."
        self.canvas.setFont(self.config.font_name_item, self.config.font_size_item)
        self.canvas.drawString(current_x_position, self.current_y_position, enum)
        current_x_position += self.config.space_for_enumerations
        # Calculate sizes of text
        text_left_width = self.canvas.stringWidth(item.text_left,
                                                  self.config.font_name_bold_item if item.is_left_bold else self.config.font_name_item,
                                                  self.config.font_size_item) if item.text_left is not None else 0
        text_right_width = self.canvas.stringWidth(item.text_right,
                                                   self.config.font_name_bold_item if item.is_right_bold else self.config.font_name_item,
                                                   self.config.font_size_item) if item.text_right is not None else 0
        # Draw left text
        if item.text_left is not None:
            self.canvas.setFont(self.config.font_name_bold_item if item.is_left_bold else self.config.font_name_item,
                                self.config.font_size_item)
            self.canvas.drawString(current_x_position, self.current_y_position, item.text_left)
            current_x_position += text_left_width
        # Draw right text
        if item.text_right is not None:
            self.canvas.setFont(self.config.font_name_bold_item if item.is_right_bold else self.config.font_name_item,
                                self.config.font_size_item)
            self.canvas.drawRightString(self.x_limit_right, self.current_y_position, item.text_right)
        # Draw connecting dots
        if item.text_left is not None and item.text_right is not None:
            text_dots_width = self.x_limit_right - text_right_width - current_x_position
            text_dots = '.' * int(text_dots_width / self.canvas.stringWidth('.', self.config.font_name_item, self.config.font_size_item))
            # Replace first and last dot with space if we have non-empty text so that we have a small separation
            if item.text_left != "":
                text_dots = " " + text_dots[1:]
            if item.text_right != "":
                text_dots = text_dots[:-1] + " "
            self.canvas.setFont(self.config.font_name_item, self.config.font_size_item)
            self.canvas.drawString(current_x_position, self.current_y_position, text_dots)
        self.current_y_position -= self.config.space_between_items
        # Draw subitems
        for subitem in item.subitems:
            self._print_item_to_page(subitem,
                                     x_offset_left_border + self.config.space_for_enumerations)


    def add_page(self,
                 draw_header: bool = True,
                 draw_footer: bool = True
                 ):
        """
            Adds a new page to the pdf

            Params
            ------
                draw_header (bool):
                    Whether a header should be drawn onto the page. Defaults to True
                draw_footer (bool):
                    Whether a footer should be drawn onto the page. Defaults to True
        """
        if self.current_page != 0:
            self.canvas.showPage()
        self.current_page += 1
        if draw_header:
            self._draw_header(self.aircraft_type,
                              self.checklist_type)
        if draw_footer:
            self._draw_footer(self.checklist_version,
                              self.real_world_clearance,
                              self.show_page_numbers)
        self.current_y_position = self.y_limit_top


    def _draw_header(self,
                     aircraft_type: str,
                     checklist_type: str
                     ):
        """
            Draws a header onto the current page

            Params
            ------
                aircraft_type (str):
                    Type of the aircraft the checklist is for
                checklist_type (str):
                    Type of the checklist
        """
        self.canvas.setFont(self.config.font_name_header_footer, self.config.font_size_header_footer)
        self.canvas.drawString(self.x_limit_left, self.y_header, aircraft_type)
        self.canvas.drawRightString(self.x_limit_right, self.y_header, checklist_type)


    def _draw_footer(self,
                     version: str,
                     real_world_clearance: bool,
                     show_page_number: bool = True
                     ):
        """
            Draws a footer onto the current page

            Params
            ------
                version (str):
                    Version of the Checklist
                real_world_clearance (bool):
                    Whether the checklist is meant for real-world usage
                show_page_number (bool):
                    Whether the page number should be shown in the bottom right corner.
                    Defaults to True.
        """
        self.canvas.setFont(self.config.font_name_header_footer, self.config.font_size_header_footer)
        self.canvas.drawString(self.x_limit_left, self.y_footer, f"Version {version}")
        if show_page_number:
            self.canvas.drawRightString(self.x_limit_right, self.y_footer, f"Page {self.current_page}")
        if not real_world_clearance:
            text = "----- For Simulator Use Only -----"
            text_width = self.canvas.stringWidth(text, self.config.font_name_header_footer, self.config.font_size_header_footer)
            self.canvas.drawString(self._get_centered_text_x(text_width), self.y_footer, text)


    def _get_centered_text_x(self,
                             text_width: int
                             ) -> int:
        """
            Returns the x coordinate to which the text
            can be written such that it appears centered

            Params
            ------
                text_width (int):
                    Width of the text

            Returns
            -------
                int:
                    X coordinate at which the text should start in order
                    to appear centered
        """
        x_middle = (self.page_width - self.config.border_right - self.config.border_left) // 2 + self.config.border_left
        x_start = x_middle - (text_width // 2)
        return x_start


    def section_fits_page(self,
                          section: ChecklistSection
                          ) -> bool:
        """
            Determines whether the given section fits onto the current page

            Params
            ------
                section (ChecklistSection):
                    The section which should be tested

            Returns
            -------
                bool:
                    Whether the section fits onto the current page or not
        """
        # Space between section name and first item
        final_y_position = self.current_y_position - self.config.space_section_to_item
        if section.description is not None:
            raise NotImplementedError("Section descriptions are currently not supported!")
        for item in section.items:
            final_y_position -= self.config.space_between_items
            if isinstance(item, SectionItem):
                final_y_position -= (len(item.subitems) * self.config.space_between_items)
        # The last element does not need spacing between items, so remove it
        final_y_position += self.config.space_between_items
        return final_y_position > self.y_limit_bottom
