from PyPDF2 import PdfFileReader, PdfFileWriter
import subprocess
import pyAesCrypt
import re

print("""
░▒█▀▀▀░█▀▀▄░█▀▄░█▀▀▄░█░░█░▄▀▀▄░▀█▀░░▀░░█▀▀▄░█▀▀▀░░░░░░░░░
░▒█▀▀▀░█░▒█░█░░░█▄▄▀░█▄▄█░█▄▄█░░█░░░█▀░█░▒█░█░▀▄░▄▄░▄▄░▄▄
░▒█▄▄▄░▀░░▀░▀▀▀░▀░▀▀░▄▄▄▀░█░░░░░▀░░▀▀▀░▀░░▀░▀▀▀▀░▀▀░▀▀░▀▀

""")
input_file = "sample.pdf"
with open(input_file, "rb") as pdf_file:
    reader = PdfFileReader(input_file, strict=False)

writer = PdfFileWriter()
writer.appendPagesFromReader(reader)
writer.encrypt("0000")
encrypted_file_name = "{}_encrypted.pdf".format(re.split("[.]", input_file)[0])
with open(encrypted_file_name, 'wb') as f:
    writer.write(f)

print("""
░░░░░░   ░░░░░░  ░░░    ░░ ░░░░░░░ ░░ 
▒▒   ▒▒ ▒▒    ▒▒ ▒▒▒▒   ▒▒ ▒▒      ▒▒ 
▒▒   ▒▒ ▒▒    ▒▒ ▒▒ ▒▒  ▒▒ ▒▒▒▒▒   ▒▒ 
▓▓   ▓▓ ▓▓    ▓▓ ▓▓  ▓▓ ▓▓ ▓▓         
██████   ██████  ██   ████ ███████ ██ 

""")

