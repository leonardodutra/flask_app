FROM python:3.10-slim-buster
#RUN apt install -y default-jdk
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

RUN pip install pdfquery
RUN pip install pandas
RUN pip install python-brcode
RUN pip install qrcode
RUN pip install pypdf
RUN pip install pix-utils
RUN pip install Spire.PDF
RUN pip install pillow
RUN pip install pymupdf
RUN pip install python-dotenv
COPY . .
EXPOSE 5000
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host", "0.0.0.0"]