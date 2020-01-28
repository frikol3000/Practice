import win32print
import win32ui
from PIL import Image, ImageWin
from os import remove

def printImage(file_name):
  PHYSICALWIDTH = 110
  PHYSICALHEIGHT = 111

  try:
    printer_name = win32print.GetDefaultPrinter()
  except:
    print("No printer found")

  hDC = win32ui.CreateDC ()
  hDC.CreatePrinterDC (printer_name)
  printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)

  bmp = Image.open (file_name)
  if bmp.size[0] < bmp.size[1]:
    bmp = bmp.rotate (90)

  hDC.StartDoc (file_name)
  hDC.StartPage ()

  dib = ImageWin.Dib (bmp)
  dib.draw (hDC.GetHandleOutput (), (0,0,printer_size[0],printer_size[1]))

  hDC.EndPage ()
  hDC.EndDoc ()
  hDC.DeleteDC ()

  remove("temp.png")