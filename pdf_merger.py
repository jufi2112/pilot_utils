import os
import argparse

from os import path as osp
try:
    from pypdf import PdfWriter, PdfReader, Transformation
    from pypdf.generic import RectangleObject
except ImportError:
    raise ImportError("Could not import pypdf, please install it using the command 'pip install pypdf', then run the script again")

try:
    from tqdm import tqdm
    tqdm_imported = True
except ImportError:
    tqdm_imported = False


def merge(input_dir: str,
          output_dir: str,
          output_name: str,
          arranged_output_name: str,
          overwrite_existing_pdf: bool = False):
    if not osp.isdir(input_dir):
        raise ValueError(f"Not a valid directory: {input_dir}")
    if osp.isfile(osp.join(output_dir, output_name)) and not overwrite_existing_pdf:
        raise ValueError(f"File {output_name} already exists at {output_dir}. "
                         "Provide --allow-overwriting to allow overwriting of "
                         "existing merged files.")
    os.makedirs(output_dir, exist_ok=True)
    pdfs = sorted(
        [
            file for file in os.listdir(input_dir) \
                if osp.splitext(file)[1] == '.pdf' and file != output_name and file != arranged_output_name
        ],
        key=lambda v: v.upper()
        )
    n_pdfs = len(pdfs)
    if n_pdfs == 0:
        return False
    merger = PdfWriter()
    for pdf in pdfs:
        merger.append(osp.join(input_dir, pdf))
    merger.write(osp.join(output_dir, output_name))
    merger.close()
    print(f"Done merging {n_pdfs} pdf files: {pdfs}")
    print(f"Merged pdf location: {osp.join(output_dir, output_name)}")
    return True


def arrange(input_file: str,
            output_dir: str,
            output_name: str,
            overwrite_existing_pdf: bool = False):
    a4_width = 595
    a4_height = 842
    if not osp.isfile(input_file):
        raise ValueError(f"The provided input file is not valid: {input_file}")
    if osp.isfile(osp.join(output_dir, output_name)) and not overwrite_existing_pdf:
        raise ValueError(f"File {output_name} already exists at {output_dir}. "
                         "Provide --allow-overwriting to allow overwriting of "
                         "existing arranged files.")
    os.makedirs(output_dir, exist_ok=True)
    writer = PdfWriter()
    reader = PdfReader(input_file)
    num_pages = len(reader.pages)
    i = 0
    while i < num_pages:
        if i+1 < num_pages:
            first_page = reader.pages[i]
            second_page = reader.pages[i+1]
            # Create blanked A4 page
            new_page = writer.add_blank_page(width=a4_height, height=a4_width)

            for n, page in enumerate([first_page, second_page]):
                transformation = Transformation()
                mediabox = page.mediabox
                # check if the provided page is in landscape format.
                is_landscape = mediabox.width > mediabox.height

                # if landscape, we also have to rotate during merging
                if is_landscape:
                    transformation = transformation.rotate(90)
                    # determine scaling necessary to print original in portrait
                    # orientation to new page in landscape orientation
                    scale = a4_width / mediabox.width
                else:
                    # determine scaling necessary to print original in portrait
                    # orientation to new page in landscape orientation
                    scale = a4_width / mediabox.height
                transformation = transformation.scale(sx=scale, sy=scale)

                # Second page needs to be moved to 2nd halve of the landscape-oriented A4 page
                if n == 1:
                    transformation = transformation.translate(tx=a4_height/2,
                                                              ty=0)
                if is_landscape:
                    transformation = transformation.translate(tx=mediabox.height*scale,
                                                              ty=0)
                new_page.merge_transformed_page(page, transformation)

            i += 2
        else:
            print("One extra page (due to uneven number of pages) ignored in "
                  "arranged pdf (this is the last page in the merged pdf)!")
            i += 1
    writer.write(osp.join(output_dir, output_name))
    print(f"Finished arranging pdf. Saved to {osp.join(output_dir, output_name)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merges all pdf files in the "
                                     "provided directory (order according to "
                                     "name) and arranges them for dual-side use"
                                     " (e.g. for a kneeboard). The provided "
                                     "pdfs have to be in portrait format.")
    parser.add_argument('-i', '--input-dir', type=str, required=True,
                        help="Directory in which the to-be-merged pdf files "
                        "are located.")
    parser.add_argument('-o', '--output-dir', type=str, default=None,
                        help="Output path. Defaults to same directory as "
                        "the input directory.")
    parser.add_argument('--merged-name', type=str, default=None,
                        help="Name of the merged pdf. Defaults to 'merged'")
    parser.add_argument('--arranged-name', type=str, default=None,
                        help="Name of the arranged pdf. Defaults to 'arranged'")
    parser.add_argument('--allow-overwriting', action='store_true',
                        help="Allows overwriting of existing merged pdfs.")
    parser.add_argument('--no-arrange', action='store_true',
                        help="Do not arrange the merged pdfs")
    parser.add_argument('--remove-temp-files', action='store_true',
                        help="Remove temporary files (i.e. the merged file)")
    parser.add_argument('-r', '--recursive', action='store_true',
                        help="If specified, interprets the given input-dir as "
                        "parent directory where the merging and arranging "
                        "operations should be applied to each sub-directory. "
                        "In this case, ignores output-dir and outputs all "
                        "results to the respective sub-directories. "
                        "Naming will also be inferred from the sub-directory"
                        " name.")
    args = parser.parse_args()
    dirs_to_process = []
    if not args.recursive:
        dirs_to_process = [args.input_dir]
        if args.merged_name is None:
            args.merged_name = 'merged'
        if args.arranged_name is None:
            args.arranged_name = 'arranged'
    else:
        dirs_to_process = [osp.join(args.input_dir, element) for element in os.listdir(args.input_dir) if osp.isdir(osp.join(args.input_dir, element))]
        args.output_dir = None
        args.merged_name = None
        args.arranged_name = None

    for directory in tqdm(dirs_to_process) if tqdm_imported else dirs_to_process:
        output_dir = args.output_dir
        merged_name = args.merged_name
        arranged_name = args.arranged_name
        if output_dir is None:
            output_dir = directory
        if merged_name is None:
            merged_name = osp.basename(osp.normpath(directory)) + '_merged'
        if osp.splitext(merged_name)[1] != '.pdf':
            merged_name += '.pdf'
        if arranged_name is None:
            arranged_name = osp.basename(osp.normpath(directory)) + '_arranged'
        if osp.splitext(arranged_name)[1] != '.pdf':
            arranged_name += '.pdf'
        success = merge(directory, output_dir, merged_name, arranged_name, args.allow_overwriting)
        if not success:
            print(f"No PDFs found in directory {directory}, skipping...")
            continue
        if not args.no_arrange:
            arrange(osp.join(output_dir, merged_name), output_dir,
                    arranged_name, args.allow_overwriting)
        if args.remove_temp_files:
            merged_file = osp.join(output_dir, merged_name)
            if osp.isfile(merged_file):
                os.remove(merged_file)
                print(f"Removed merged file at {merged_file}")
