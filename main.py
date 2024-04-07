from pdfquery import PDFQuery
import qrcode
from pypdf import PdfReader
from decimal import Decimal
from brcode import BRCode
import fitz
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

CNPJ = os.getenv('CNPJ')
DESCRIPTION = os.getenv('DESCRIPTION')



from flask import *
app = Flask(__name__) 

@app.route('/') 
def main(): 
	return render_template("index.html") 

@app.route('/success', methods = ['POST']) 
def success():
	if request.method == 'POST': 
		f = request.files['file'] 
		f.save(f.filename)
		doc = fitz.Document(f.filename)
		page_qrcode = doc.load_page(0)
		def pic_getinfo(doc,page_qrcode, item):
			xref, _, width, height, _, _, _, name , _ = item

			rect = page_qrcode.get_image_bbox(name)
			img = Image.open(io.BytesIO(doc.extract_image(xref)['image']))
			return {"height":height,"width":width,"xref":xref, "name":name, "rect":rect,"img":img }
		

		ImageList = page_qrcode.get_images()
		#ImageList

		pic3 = pic_getinfo(doc,page_qrcode, ImageList[3])
		pdf = PDFQuery(f.filename)
		pdf.load()
		text_elements = pdf.pq('LTTextLineHorizontal')
		text = [t.text for t in text_elements]
		
		reader = PdfReader(f.filename)
		number_of_pages = len(reader.pages)
		page = reader.pages[0]
		text2 = page.extract_text()
		lang_split = text2.split('\n')
		valor = lang_split[9].split('(-)')[0]
		if valor == '(x) Valor Espécie (=) Valor do Documento':
			valor = lang_split[10].split('(-)')[0]
        
		try:
			nome = lang_split[31].split('Pagador')[1]
		except IndexError:
			nome = lang_split[32].split('Pagador')[1]

		try:
			numero = lang_split[38].split(':  ')[1]
		except IndexError:
			numero = lang_split[37].split(':  ')[1]
		valor = valor.replace(".", "").replace(",", ".")
		nome = nome.replace(r'/',' ')
		nome = nome.replace(r'-',' ')
		nome = nome.replace(r'0',' ')
		nome = nome.replace(r'1',' ')
		nome = nome.replace(r'2',' ')
		nome = nome.replace(r'3',' ')
		nome = nome.replace(r'4',' ')
		nome = nome.replace(r'5',' ')
		nome = nome.replace(r'6',' ')
		nome = nome.replace(r'7',' ')
		nome = nome.replace(r'8',' ')
		nome = nome.replace(r'9',' ')
		nome = nome.replace(r'.',' ')
		brcode = BRCode(
            name=nome.replace(" ", ""),
            key=CNPJ,
            city="SAO PAULO",
            amount=Decimal(valor),                 # optional
            description=DESCRIPTION,   # optional
            transaction_id=numero.replace(" ", ""),                     # optional
        )
		#gera qrcode 500x500
		img = qrcode.make(str(brcode))
		img.save(f.filename + "_brcode" + ".png")
		#transforma qrcode em 302x302
		img = Image.open(f.filename + "_brcode" + ".png") # image extension *.png,*.jpg
		new_width  = 302
		new_height = 302
		img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
		img.save('output.png') # format may what you want *.png, *jpg, *.gif
		page_qrcode.insert_image(pic3['rect'], filename="output.png")
		doc.save(f.filename, incremental=True, encryption=0)
		
	return render_template("Acknowledgement.html", name = (str(brcode)))
if __name__ == '__main__': 
	app.run(debug=True)