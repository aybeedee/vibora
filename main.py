# if you are on windows, download Poppler and add it to PATH
# go to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version
import time, os, sys, argparse, logging

from vibora.pdf2png import pdf_to_png
from vibora.pdf2txt import pdf_to_text
from vibora.txt2pdf import txt_to_pdf
from vibora.extract_img_from_pdf import extract_img_from_pdf
from vibora.compress import compress_pdf  
from vibora.merge import merge_pdf, merge_pdf_directory
from vibora.rename import rename_file
from vibora.rotate import rotate_pdf
from vibora.img2pdf import image_to_pdf
from vibora.split import split_pdf
from vibora.watermark import watermark_pdf
from vibora.encrypt import encrypt_pdf
from vibora.decrypt import decrypt_pdf
from vibora.pdf2audio import audio
from vibora.redact import Redactor
from vibora.compare import compare_file
from vibora.extra_compression.rwcompression import rwcomp
from vibora.extra_compression.fitzcompression import fitzcomp

if __name__ == '__main__':
  # case we type only vibora
  if len(sys.argv) == 1:
    print("Missign arguments, see 'help' for reference on how to use it!")
  # case we type vibora help
  elif sys.argv[1].lower() == 'help':
    print('\nWelcome to vibora :) A PDF tool that lets you convert a PDF to PNG, PDF to text, plus some more awesome things. See below!')
    print("\nPDF TO PNG:\n   To convert a .PDF to .PNG, use: 'pdf2png [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nPDF TO TEXT:\n   To convert a .PDF to .TXT, use: 'pdf2text [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nEXTRACT IMAGES FROM PDF:\n   To extract images from a .PDF file, use: 'extractimg [file].pdf'")
    print('   You will be prompted with the amount of images found, and if you want to proceed or not.')
    print("\nCOMPRESS PDF:\n   To compress a .PDF file, use: 'compress [file].pdf'")
    print('   It will try to compress your file without losing quality or removing content.')
    print("\nTXT TO PDF:\n   To convert a .TXT file to .PDF, use: 'txt2pdf [file].txt'")
    print('   It will convert a .txt file into .pdf.')
    print("\nMERGE PDFs:\n   To merge .PDF files into one .PDF, use: 'merge [file1].pdf [file2].pdf [file3].pdf'")
    print('   It will merge the files provided, without losing quality or cutting content. It can take as many files as you want.')
    print("\nMERGE ALL PDF FILES INSIDE DIRECTORY:\n   To merge all .PDF files inside a directory, use: 'mergeall [directory]'")
    print('   It will ignore non .PDF files and merge all .PDF files inside that folder. Files are merged by alphabetical order.')
    print("\nRENAME FILES:\n   To rename files using vibora, you can use: 'rename [file].pdf [newname].pdf'")
    print('   It will change the name of the file you provided, with the name you typed after it, without affecting th file.')
    print("\nROTATE PDF:\n   To rotate a .PDF file, you can you can use: 'rotate [file].pdf'")
    print('   It will rotate you file by 90º. Depending on your file, you may want to rotate it multiple times.')
    print("\nIMAGE TO PDF:\n   To convert an image to a .PDF file, you can you can use: 'img2pdf [file].[extension]'")
    print('   It can convert multiple image formats into a .PDF file.')
    print("\nSPLIT PDF:\n   To split a .PDF file into separated pages, you can you can use: 'split [file].pdf'")
    print('   It will split the .PDF file into separated pages. Each page from the .PDF will be a single .PDF file.')
    print("\nWATERMARK PDF:\n   To add watermark to a a .PDF file, you can you can use: 'watermark [file].pdf [watermarkfile].pdf'")
    print('   It will add a watermark to the bottom left of the .PDF file. Remember that the watermark must also be a .PDF file.')
    print("\nENCRYPT PDF:\n   To encrypt a .PDF file, you can you can use: 'encrypt [file].pdf [password]'")
    print('   It will encrypt a .pdf file by adding a password to be able to read its content.')
    print("\nDECRYPT PDF:\n   To decrypt a .PDF file, you can you can use: 'decrypt [file].pdf [password]'")
    print("   It will remove the password of a pdf file. Note that it doesn't crack the .pdf file, it works only if you have the password.")
    print("\nREAD PDF FOR ME:\n   To make vibora read (yes, audio related) a .PDF file, you can use: 'speak [file].pdf'")
    print("   It will start reading the text of a pdf file for you. You can stop it by pressing CTRL + C.")
    print("\nREDACT SENSITIVE INFORMATION:\n   To redact sensitive information in a .PDF file, you can use: 'redact [file].pdf'")
    print("   It will hide sensitive information behind a black rectangle.")
    print("\nCOMPARE FILES:\n   To compare files at a low level, you can use: 'compare [file1.pdf] [file2.pdf]'")
    print("   It will compare these files at a low level (length, metadata, etc) to see if they match.")
    
  # case we actually pass a valid argument
  else:

    # error msg
    def custom_error(msg):
      print("Command not recognized. Use 'help' to see the available commands.")
      exit()

    parser = argparse.ArgumentParser(description="vibora")
    parser.error = custom_error
    subparser = parser.add_subparsers(title='subparser', dest='subcommand')

    # pdf to png subparser
    pdf2png_parser = subparser.add_parser('pdf2png', description='Convert a .PDF file into a .PNG file.')
    pdf2png_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the PDF file to convert.')
    pdf2png_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode ')

    # pdf to text subparser
    pdf2txt_parser = subparser.add_parser('pdf2txt', description='Convert a .PDF file into a .TXT file.')
    pdf2txt_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the PDF file.')
    pdf2txt_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # extract img from pdf subparser
    extractimg_parser = subparser.add_parser('extractimg', help='help message', description='It will extract all images from a .PDF file.')
    extractimg_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    extractimg_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    
    # compress subparser
    compress_parser = subparser.add_parser('compress', help='help message', description='It will compress your file without losing quality or removing content.')
    compress_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the PDF file to compress.')
    compress_parser.add_argument('output', type=str, metavar='output', nargs='?', help='Name of the output file.')
    compress_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # text to pdf subparser
    txt2pdf_parser = subparser.add_parser('txt2pdf', help='help message', description='It will convert a .TXT file into a .PDF file.')
    txt2pdf_parser.add_argument('txt_path', type=str, metavar='txt_path', help='Path to the .TXT file.')
    txt2pdf_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # merge pdf subparser
    merge_parser = subparser.add_parser('merge', help='help message', description='It will merge .PDF files into a single one.')
    merge_parser.add_argument('pdf_files', type=str, metavar='pdf_files', nargs='+', help='Path to .PDF files.')
    merge_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # merge all pdf inside dir subparser
    mergeall_parser = subparser.add_parser('mergeall', help='help message', description='It will merge all .PDF files inside a directory.')
    mergeall_parser.add_argument('dir_path', type=str, metavar='dir_path', help='Path to directory.')
    mergeall_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # rename file subparser
    rename_parser = subparser.add_parser('rename', help='help message', description='It will rename a file.')
    rename_parser.add_argument('file_path', type=str, metavar='file_path', help='Path to the file to rename.')
    rename_parser.add_argument('new_name', type=str, metavar='new_name', help='New file name')
    rename_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # rotate pdf subparser
    rotate_parser = subparser.add_parser('rotate', help='help message', description='It will rotate a .PDF file by 90 degrees.')
    rotate_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    rotate_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # image to pdf subparser
    img2pdf_parser = subparser.add_parser('img2pdf', help='help message', description='It will convert an image into a .PDF file.')
    img2pdf_parser.add_argument('img_path', type=str, metavar='img_path', help='Path to the image file.')
    img2pdf_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # split pdf subparser
    split_parser = subparser.add_parser('split', help='help message', description='It will split a .PDF file into separated files, each page will be a .PDF file.')
    split_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    split_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # watermark pdf subparser
    watermark_parser = subparser.add_parser('watermark', help='help message', description='It will add a watermark to a .PDF file.')
    watermark_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    watermark_parser.add_argument('watermark_path', type=str, metavar='watermark_file', help='Path to the watermark file.')
    watermark_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # encrypt pdf subparser
    encrypt_parser = subparser.add_parser('encrypt', help='help message', description='It will encrypt a .PDF file.')
    encrypt_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    encrypt_parser.add_argument('password', type=str, metavar='password', help='Password to encrypt the file with.')
    encrypt_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # decrypt pdf subparser
    decrypt_parser = subparser.add_parser('decrypt', help='help message', description='It will decrypt a .PDF file.')
    decrypt_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    decrypt_parser.add_argument('password', type=str, metavar='password', help='Password to decrypt the file.')
    decrypt_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # pdf to audio subparser
    pdf2audio_parser = subparser.add_parser('pdf2audio', help='help message', description='It will read a .PDF file for you.')
    pdf2audio_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    pdf2audio_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # redact information from pdf subparser
    redact_parser = subparser.add_parser('redact', help='help message', description='It will redact sensitive information from a .PDF file.')
    redact_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')
    redact_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # compare files subparser
    compare_parser = subparser.add_parser('compare', help='help message', description='It will compare files at a low level.')
    compare_parser.add_argument('file1', type=str, metavar='file1', help='Path to file one.')
    compare_parser.add_argument('file2', type=str, metavar='file2', help='Path to file two.')
    compare_parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')

    # rwcompression subparser
    rwcompression_parser = subparser.add_parser('rwcompress', help='help message', description='Compress files using pdfrw compressions algorithm')
    rwcompression_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')

    # fitzcompression subparser
    fitzcompression_parser = subparser.add_parser('fitzcompress', help='help message', description='Compress files using pymupdf.')
    fitzcompression_parser.add_argument('pdf_path', type=str, metavar='pdf_path', help='Path to the .PDF file.')

    args = parser.parse_args()  

    match args.subcommand:

      case 'pdf2png':
        pdf_path = args.pdf_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Converting file: {args.pdf_path}\n. . .\nFile converted!")
        pdf_to_png(pdf_path)
      
      case 'pdf2txt':
        pdf_path = args.pdf_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Converting file: {args.pdf_path}\n. . .\nFile converted!")
        pdf_to_text(pdf_path)

      case 'extractimg':
        pdf_path = args.pdf_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Extracting images from file: {args.pdf_path}\n. . .\nImages extracted!")
        extract_img_from_pdf(pdf_path)

      case 'compress':
        pdf_path = args.pdf_path
        output = args.output
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            # logging.basicConfig(level=logging.INFO)
            print(f"Compressing file: {args.pdf_path}\n. . .\nFile compressed!")
        compress_pdf(pdf_path, output)
      
      case 'txt2pdf':
        txt_path = args.txt_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Converting file {txt_path}\n. . .\nFile converted!")
        txt_to_pdf(txt_path)

      case 'merge':
        pdf_files = args.pdf_files
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Merging files: {pdf_files}\n. . .\nFiles merged!")
        merge_pdf(*pdf_files)

      case 'mergeall':
        dir_path = args.dir_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Merging files in directory: {dir_path}\n. . .\n Files merged!")
        merge_pdf_directory(dir_path)
    
      case 'rename':
        file_path = args.file_path
        new_name = args.new_name
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Renaming file {file_path} to {new_name}")
        rename_file(file_path, new_name)

      case 'rotate':
        pdf_path = args.pdf_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Rotating file: {pdf_path}\n. . .\nFile rotated!")
        rotate_pdf(pdf_path)

      case 'img2pdf':
        img_path = args.img_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Converting file: {args.img_path}\n. . .\nFile converted!")
        image_to_pdf(img_path)
      
      case 'split':
        pdf_path = args.pdf_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Splitting file: {pdf_path}\n. . .\nFile split!")
        split_pdf(pdf_path)

      case 'watermark':
        pdf_path = args.pdf_path
        watermark_path = args.watermark_path
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Adding watermark to file: {pdf_path}\n. . .\nWatermark added!")
        watermark_pdf(pdf_path, watermark_path)

      case 'encrypt':
        pdf_path = args.pdf_path
        password = args.password
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Encrypting file: {args.pdf_path}\n. . .\nFile encrypted!")
        encrypt_pdf(pdf_path, password)

      case 'decrypt':
        pdf_path = args.pdf_path
        password = args.password
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG) 
          case False:
            print(f"Decrypting file: {args.pdf_path}\n. . .\nFile decrypted!")
        decrypt_pdf(pdf_path, password)

      case 'pdf2audio':
        pdf_path = args.pdf_path
        audio(pdf_path)

      case 'redact':
        pdf_path = args.pdf_path
        redactor = Redactor(pdf_path)
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            print(f"Redacting file: {pdf_path}")
        redactor.redaction()
      
      case 'compare':
        file1 = args.file1
        file2 = args.file2
        match args.debug:
          case True:
            logging.basicConfig(level=logging.DEBUG)
          case False:
            # logging.basicConfig(level=logging.DEBUG)
            print(f"Comparing files {file1} and {file2}\n. . .")
        compare_file(file1, file2)

      case 'rwcompress':
        pdf_path = args.pdf_path
        rwcomp(pdf_path)

      case 'fitzcompress':
        pdf_path = args.pdf_path
        fitzcomp(pdf_path)

