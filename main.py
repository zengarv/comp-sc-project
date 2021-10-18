import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime

# Get HTML source code
url = 'https://prsindia.org/covid-19/cases'


def graph():
    datasite = requests.get(url)
    soup = BeautifulSoup(datasite.text, "html.parser")
    # Get all script tags(because that's where the data is)
    extracted_script = soup.findAll('script')[2]

    # Find the lists we are looking for
    var_segment = ''
    for lines in extracted_script:
        if 'var' in lines:
            var_segment = lines
            break

    # Get daily dates in the form of lists
    dates = confirm = active = death = cure = count = []
    grp_list = [dates, confirm, active, death, cure, count]
    var_list = var_segment.strip().split('\n')
    for index in range(len(var_list)):
        grp_list[index] = var_list[index].lstrip(' var').lstrip('abcdefghijklmnopqrstuvwxyz ').lstrip(' =[').rstrip(
            '"]; ').split('","' if index == 0 else ',')
        if index != 0: grp_list[index] = [int(x) for x in grp_list[index]]

    def overall_stat():
        # plotting the points
        total = len(grp_list[2]) - 1
        plt.plot([x + 1 for x in range(total)], grp_list[2][1:], label="Active")
        plt.plot([x + 1 for x in range(total)], grp_list[1][1:], label='Confirmed')
        plt.plot([x + 1 for x in range(total)], grp_list[3][1:], label='Deaths')
        plt.plot([x + 1 for x in range(total)], grp_list[4][1:], label='Cured')

        # Labelling
        plt.xlabel('Days')
        plt.ylabel('Nums')
        plt.title('Day Wise Cases: India')
        plt.legend(loc="upper left")
        plt.savefig('assets\\overall stat.jpeg', bbox_inches='tight')
        plt.close()

    overall_stat()

    def last14day():
        plt.plot([x + 1 for x in range(14)], grp_list[2][-14:], label="Active")
        # plt.plot([x + 1 for x in range(14)], grp_list[1][-14:], label='Confirmed')
        # plt.plot([x + 1 for x in range(14)], grp_list[3][-14:], label='Deaths')
        # plt.plot([x + 1 for x in range(14)], grp_list[4][-14:], label='Cured')

        # Labelling
        plt.xlabel('Days')
        plt.ylabel('Nums')
        plt.title('Last 14 Days')
        plt.legend(loc="upper left")
        plt.savefig('assets\\last14daystat.jpeg', bbox_inches='tight')

    last14day()


graph()

title = 'The Covid Bugle'
class PDF(FPDF):
    def header(self):
        pdf.set_font('times', 'B', 16)
        self.cell(70, align='C')
        title_w = self.get_string_width(title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.set_draw_color(0, 80, 180)  # Border Colour: blue
        self.set_fill_color(230, 230, 0)  # Background Color of Title: yellow
        self.set_text_color(220, 50, 50)  # Text Color: red
        self.set_line_width(1)
        self.cell(title_w, 10, title, border=True, ln=1, align='C', fill=True)

        now = datetime.now()
        pdf.set_font('courier', '', 7)

        self.cell(190, 7, f'Generated on {now.strftime("%b %d, %Y at %H:%M")}', align='C')
        self.image('assets\\covpic.png', 10, 2, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-10)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)  # Grey color
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')
        WHOsite = 'https://www.who.int/health-topics/coronavirus#tab=tab_1'
        self.set_font('helvetica', '', 6)
        self.set_text_color(100, 100, 150)
        pdf.cell(-193, 2, 'Learn More: WHO', ln=1, link=WHOsite, align='C')


pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_title(title)
pdf.set_author('TheCovidBugle')
pdf.image('assets\\overall stat.jpeg', x=3, y=30, w=100, h=75)  # 640:480, 4:3
pdf.image('assets\\last14daystat.jpeg', x=103, y=30, w=100, h=75)

pdf.set_font('helvetica', '', 10)
pdf.cell(0, 170, 'Stats go here\nMore Stats', ln=True)

pdf.output('test_pdf.pdf')
