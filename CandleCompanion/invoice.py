import os
from fpdf import FPDF


class Make:
    """
    Makes a pdf invoice
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, product, scent, decoration, quantity, price, customer):
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.image("img/RoarinLogo.png", w=75, h=75)

        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt='Roaring Aromas Invoice', border=0, align='C', ln=1)

        pdf.set_font(family='Times', size=13, style='B')
        pdf.cell(w=100, h=40, txt='Items:', border=0, align='L')
        pdf.cell(w=100, h=40, txt="{} {} {} {}".format(product, scent, decoration, quantity), border=0,
                 align='L', ln=1)
        pdf.cell(w=100, h=40, txt="Price: ")
        pdf.cell(w=100, h=40, txt="£{}".format(price), ln=1, align='L')
        pdf.cell(w=150, h=40, txt="For {}, thank you for your custom".format(customer))

        os.chdir("output")
        pdf.output(self.filename)


invoice = Make(filename="invoice.pdf")
invoice.generate(product="Candle", scent="Cinnamon", decoration="Glitter", quantity=5, price=15, customer="Sarah")
