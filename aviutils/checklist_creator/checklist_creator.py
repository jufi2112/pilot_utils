from typing import Dict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from os import path as osp
import os
import sys
sys.path.append('..')
from aviutils.checklist_creator import ChecklistParser


class PDFChecklistCreator:
    def __init__(self,
                 border_width: int = 10,
                 border_height: int = 100,
                 font: str = "Helvetica",
                 font_bold: str = 'Helvetica-Bold',
                 font_size: int = 12,
                 line_space: int = 20,
                 page_size: str = 'A5'):
        self.border_width = border_width
        self.border_height = border_height
        self.font = font
        self.font_bold = font_bold
        self.font_size = font_size
        self.line_space = line_space
        self.page_size = page_size


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
        left_border = self.border_width
        right_border = width - self.border_width
        top_border = height - self.border_height
        bottom_border = self.border_height

        current_y_position = top_border
        for section_name in cl.keys():
            for item, value in cl[section_name].items():
                value = value[0]
                text_item = f"{item} "
                text_value = f" {value}"
                text_width_item = c.stringWidth(f"{item} ", self.font_bold, self.font_size)
                text_width_value = c.stringWidth(f" {value}", self.font_bold, self.font_size)
                # How much width do we have remaining for the dots?
                text_dots_width = right_border - left_border - text_width_item - text_width_value
                text_dots = '.' * int(text_dots_width / c.stringWidth('.', self.font, self.font_size))

                c.setFont(self.font_bold, self.font_size)
                c.drawString(left_border, current_y_position, text_item)
                c.drawRightString(right_border, current_y_position, text_value)
                c.setFont(self.font, self.font_size)
                c.drawString(left_border + text_width_item, current_y_position, text_dots)
                current_y_position -= self.line_space
        c.save()

if __name__ == '__main__':
    parser = ChecklistParser(r"C:\Users\Julien\git\aviation_utils\aviutils\checklist_creator\test.txt")
    cl = parser.parse()

    checklist_creator = PDFChecklistCreator()
    checklist_creator.create_checklist(cl, r"C:\Users\Julien\git\aviation_utils\aviutils\checklist_creator", 'test.pdf')
