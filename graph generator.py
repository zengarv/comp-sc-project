import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from fpdf import FPDF

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
        plt.savefig('overall stat.jpeg', bbox_inches='tight')
    overall_stat()
    def last14day():
        # plt.plot([x + 1 for x in range(14)], grp_list[2][-14:], label="Active")
        plt.plot([x + 1 for x in range(14)], grp_list[1][-14:], label='Confirmed')
        # plt.plot([x + 1 for x in range(14)], grp_list[3][-14:], label='Deaths')
        plt.plot([x + 1 for x in range(14)], grp_list[4][-14:], label='Cured')

        # Labelling
        plt.xlabel('Days')
        plt.ylabel('Nums')
        plt.title('Day Wise Cases: India')
        plt.legend(loc="upper left")
        plt.savefig('last14daystat.jpeg', bbox_inches='tight')
    # last14day()

graph()

pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_font('times', 'B', 16)

pdf.cell(190, 10, 'Covid Statistics', 1, 1, 'C')
pdf.image('overall stat.jpeg', x=5, y=25, w=100, h=75)  # 640:480, 4:3

pdf.output('test_pdf.pdf')
