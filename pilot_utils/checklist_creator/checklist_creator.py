import os
import argparse

from os import path as osp
from typing import Dict, Tuple
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5

from pilot_utils.checklist_creator import ChecklistParser


class PDFChecklistCreator:
    def __init__(self,
                 aircraft_type: str,
                 checklist_type: str,
                 border_left: int = 80,
                 border_right: int = 50,
                 border_height: int = 80,
                 font: str = "Helvetica",
                 font_bold: str = 'Helvetica-Bold',
                 font_size_item: int = 6,
                 font_size_section: int = 9,
                 line_spacing_item: int = 12,
                 page_size: str = 'A5',
                 space_between_sections: int = 32,
                 space_after_header: int = 30,
                 space_section_item: int = 20
                 ):
        self.border_left = border_left
        self.border_right = border_right
        self.border_height = border_height
        self.font = font
        self.font_bold = font_bold
        self.font_size_item = font_size_item
        self.font_size_section = font_size_section
        self.line_spacing_item = line_spacing_item
        self.page_size = page_size
        self.aircraft_type = aircraft_type
        self.checklist_type = checklist_type
        self.space_between_sections = space_between_sections
        self.space_after_header = space_after_header
        self.space_section_item = space_section_item


    def create_checklist(self,
                         cl: Dict,
                         output_dir: str,
                         output_name: str
                         ):
        if not osp.isdir(output_dir):
            os.makedirs(output_dir)
        if osp.splitext(output_name)[1] != '.pdf':
            output_name = output_name + ".pdf"
        c = canvas.Canvas(osp.join(output_dir, output_name),
                          pagesize=A5)
        width, height = A5
        left_border = self.border_left
        right_border = width - self.border_right
        top_border = height - self.border_height
        bottom_border = self.border_height
        current_page = 0

        c = self._write_header_footer(c, current_page+1,
                                      left_border, right_border,
                                      top_border, bottom_border)
        current_y_position = top_border - self.space_after_header



        for section_idx in cl.keys():
            # Check if section longer than space on page
            if not self._section_fits_onto_current_page(current_y_position, cl[section_idx]):
                current_page += 1
                c.showPage()
                c = self._write_header_footer(c, current_page+1,
                                              left_border, right_border,
                                              top_border, bottom_border)
                current_y_position = top_border - self.space_after_header
            c, current_y_position = self._print_section(cl[section_idx],
                                                        c,
                                                        right_border,
                                                        left_border,
                                                        current_y_position)
        c.setFont(self.font_bold, self.font_size_item)
        c.drawRightString(right_border, bottom_border, f"Page {current_page+1}")
        c.save()


    def _print_section(self,
                       section: Dict,
                       canvas: canvas.Canvas,
                       right_border: int,
                       left_border: int,
                       current_y_position
                       ) -> Tuple[canvas.Canvas, int]:
        canvas.setFont(self.font_bold, self.font_size_section)
        canvas.drawString(left_border, current_y_position, section['name'])
        current_y_position -= self.space_section_item
        index_offset = 0
        for item_idx, item_content in section['content'].items():
            subitems = item_content['content']
            left = item_content['left']
            right = item_content['right']
            number = item_idx + 1 + index_offset
            if number < 10:
                spaces = "     "
            elif number < 100:
                spaces = "   "
            else:
                spaces = " "

            if right is None:
                # Print left in bold and without numbering
                index_offset -= 1
                text_offset = canvas.stringWidth(f"{number}.{spaces}", self.font, self.font_size_item)
                text_left = f"{left}"
                canvas.setFont(self.font_bold, self.font_size_item)
                canvas.drawString(left_border + text_offset, current_y_position, text_left)
                current_y_position -= self.line_spacing_item
            else:
                text_left = f"{number}.{spaces}{left} "
                text_right = f" {right}"
                text_right_width = canvas.stringWidth(text_left, self.font, self.font_size_item)
                text_left_width = canvas.stringWidth(text_right, self.font_bold, self.font_size_item)
                # How much width do we have remaining for the dots?
                text_dots_width = right_border - left_border - text_right_width - text_left_width
                text_dots = '.' * int(text_dots_width / canvas.stringWidth('.', self.font, self.font_size_item))

                canvas.setFont(self.font, self.font_size_item)
                canvas.drawString(left_border, current_y_position, text_left)
                canvas.setFont(self.font_bold, self.font_size_item)
                canvas.drawRightString(right_border, current_y_position, text_right)
                canvas.setFont(self.font, self.font_size_item)
                canvas.drawString(left_border + text_right_width, current_y_position, text_dots)
                current_y_position -= self.line_spacing_item
            # Draw possible subitems
            canvas, current_y_position = self._print_subitems(subitems,
                                                            canvas,
                                                            right_border,
                                                            left_border,
                                                            current_y_position,
                                                            "        ")
        current_y_position -= self.space_between_sections
        current_y_position += self.line_spacing_item
        return canvas, current_y_position


    def _section_fits_onto_current_page(self,
                                        current_y_position: int,
                                        section: Dict
                                        ) -> bool:
        """
            Returns True if the given section still fits onto the page, otherwise False

        Params
        ------
            current_y_position (int):
                Current y position
            section_content (Dict):
                Section that should be checked

        Returns
        -------
            bool:
                Whether the given section fits onto the remaining page
        """
        # Section name
        new_y_position = current_y_position - self.space_section_item
        # Spacing due to items
        for _, item_content in section['content'].items():
            new_y_position -= self.line_spacing_item
            # Spacing due to subitems
            for _, _ in item_content['content'].items():
                new_y_position -= self.line_spacing_item
        new_y_position -= self.line_spacing_item
        if new_y_position < self.border_height:
            return False
        return True


    def _print_subitems(self,
                        item_content: Dict,
                        canvas: canvas.Canvas,
                        right_border: int,
                        left_border: int,
                        current_y_position: int,
                        leading_spaces: str
                        ) -> Tuple[canvas.Canvas, int]:
        index_offset = 0
        for idx, content in item_content.items():
            number = idx + 1 + index_offset
            left = content['left']
            right = content['right']
            if right is None:
                # Print left in bold and without numbering 
                index_offset -= 1
                text_offset = canvas.stringWidth(f"{leading_spaces}{chr(ord('`')+number)}.   ", self.font, self.font_size_item)
                text_left = f"{left}"
                canvas.setFont(self.font_bold, self.font_size_item)
                canvas.drawString(left_border + text_offset, current_y_position, text_left)
            else:
                symbol = chr(ord('`') + number)
                text_left = f"{leading_spaces}{symbol}.   {left} "
                text_right = f" {right}"
                text_left_width = canvas.stringWidth(text_left, self.font, self.font_size_item)
                text_right_width = canvas.stringWidth(text_right, self.font_bold, self.font_size_item)
                text_dots_width = right_border - left_border - text_left_width - text_right_width
                text_dots = '.' * int(text_dots_width / canvas.stringWidth('.', self.font, self.font_size_item))
                canvas.setFont(self.font, self.font_size_item)
                canvas.drawString(left_border, current_y_position, text_left)
                canvas.setFont(self.font_bold, self.font_size_item)
                canvas.drawRightString(right_border, current_y_position, text_right)
                canvas.setFont(self.font, self.font_size_item)
                canvas.drawString(left_border + text_left_width, current_y_position, text_dots)
            current_y_position -= self.line_spacing_item
        return canvas, current_y_position


    def _write_header_footer(self,
                             canvas: canvas.Canvas,
                             page_number: int,
                             left_border: int,
                             right_border: int,
                             top_border: int,
                             bottom_border: int
                             ) -> canvas.Canvas:
        canvas.setFont(self.font_bold, self.font_size_item)
        canvas.drawString(left_border, top_border, self.aircraft_type)
        canvas.drawRightString(right_border, top_border, self.checklist_type)
        canvas.drawRightString(right_border, bottom_border, f"Page {page_number}")
        return canvas


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a PDF checklist from a .txt file")
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the input txt file that should be converted to a pdf checklist")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output path. If no filename is provided, uses the same filename as the input file.")
    parser.add_argument('--aircraft-type', type=str, default="", help="Aircraft type that should be stated in the upper left corner of each page")
    parser.add_argument('--checklist-type', type=str, default="", help="Type of the checklist, is specified in the upper right of each page")
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

    checklist_creator = PDFChecklistCreator(args.aircraft_type, args.checklist_type)
    checklist_creator.create_checklist(cl, output_path, output_file)
