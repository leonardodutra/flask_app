from distutils.log import debug 
from fileinput import filename 
import pandas as pd
from pdfquery import PDFQuery
import qrcode

from decimal import Decimal
from brcode import BRCode
from flask import *
app = Flask(__name__) 

@app.route('/') 
def main(): 
	return render_template("index.html") 

@app.route('/success', methods = ['POST']) 
def success(): 
	if request.method == 'POST': 
		f = request.files['file'] 
#		f.save(f.filename)
		#pdf = pdfquery.PDFQuery(f.filename)
		#carga = pdf.load()
		#pdf.tree.write(f.filename + '.xml', pretty_print = True)
		#file = PyPDF2.PdfReader(f.filename)
		#ff = file.get_fields()
		pdf = PDFQuery(f.filename)
		pdf.load()
		text_elements = pdf.pq('LTTextLineHorizontal')
		text = [t.text for t in text_elements]
		#raw = parser.from_file("BOL_430671_516622_1.pdf")
		brcode = BRCode(
            name="TOTAL EXPRESS",
            key="12274351000170",
            city="SAO PAULO",
            amount=Decimal(10.00),                    # optional
            description=text[64],   # optional
            transaction_id="999888",                     # optional
        )
		img = qrcode.make(str(brcode))
		img.save(f.filename + ".png")
	return render_template("Acknowledgement.html", name = (text[40] + text[41] + text[64] + text[65] + "qrcode:" + (str(brcode)))) 

if __name__ == '__main__': 
	app.run(debug=True)