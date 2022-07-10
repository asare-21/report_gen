from pydoc import doc
from docx2pdf import convert
import os
import pathlib
import asyncio


async def docxToPdf(file_id):
    try:
        if os.getcwd().endswith("files"):
            file_list = os.listdir()
            index = file_list.index(f"{file_id}.docx")
            # convert docx to pdf
            convert(input_path=file_list[index],
                    output_path=f"{file_id}.pdf")
            print("done")
        else:
            os.chdir("ease")
            os.chdir("static")
            os.chdir("files")  # in the files directory
            file_list = os.listdir()
            index = file_list.index(f"{file_id}.docx")
            convert(input_path=file_list[index],
                    output_path=f"{file_id}.pdf", keep_active=True)
    except Exception as e:
        print(e)
