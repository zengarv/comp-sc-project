import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime
import os
import pandas as pd


def graph():
    prs = 'https://prsindia.org/covid-19/cases'
    datasite = requests.get(prs)
    soup = BeautifulSoup(datasite.text, "html.parser")
    # Get all script tags(because that's where the data we need is)
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
        plt.close()

    def statewise_stat():
        statestaturl = 'https://www.ndtv.com/coronavirus/india-covid-19-tracker'

        datasite = requests.get(statestaturl)
        soup = BeautifulSoup(datasite.text, "html.parser")
        table = soup.findAll('p', class_='mid-wrap')

        st_cases = []
        st_active = []
        st_recovered = []
        st_death = []

        for index in range(len(table) // 4):
            st_cases.append(int(table[4 * index].get_text().split()[0]))
            st_active.append(int(table[4 * index + 1].get_text().split()[0]))
            st_recovered.append(int(table[4 * index + 2].get_text().split()[0]))
            st_death.append(int(table[4 * index + 3].get_text().split()[0]))

        states_list = []
        for states in soup.findAll('label'):
            state = states.get_text()
            if len(state) > 12:
                state = ' '.join(x[:3] for x in state.split())
            states_list.append(state)
        states_list.pop(len(states_list) - 1)
        states_list.pop(len(states_list) - 1)

        # creating the bar plot

        plt.figure(figsize=(10, 5))
        plt.bar(states_list, st_cases, label='Cases')
        plt.bar(states_list, st_active, label='Active')
        plt.xticks(rotation=90)
        plt.yscale('log')

        plt.text(24, 5000000, 'Note: Scale is Logarithmic', fontsize=8)
        plt.xlabel("States")
        plt.ylabel("Cases")
        plt.title("Statewise Demographics")
        plt.legend(loc="upper right")
        plt.savefig('assets\\statewisestat.jpeg', bbox_inches='tight')
        plt.close()
    
    def generate_ccvp():  # Countrywise Covid Vaccination Percentage
        url = 'https://covid19.who.int/table'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        table_data = soup.findAll('div', class_='column_Total_Fully_Vacc_Per_100 td')
        filtered_table_data = [float(data.text) for data in table_data if data.text != '']

        countries = soup.findAll('span')[-1:-1*len(filtered_table_data)-1:-1][::-1]
        filtered_countries = [country.text for country in countries if country.text != '']

        # Code to shorten country names
        def list_replace(list_, target, value):
            if target in list_:
                list_[list_.index(target)] = value

        list_replace(filtered_countries, 'Iran (Islamic Republic of)', 'Iran')
        list_replace(filtered_countries, 'United States of America', 'USA')
        list_replace(filtered_countries, 'The United Kingdom', 'UK')
        list_replace(filtered_countries, 'Russian Federation', 'Russia')

        # print(filtered_countries, filtered_table_data, sep='\n')
        plt.barh(filtered_countries, filtered_table_data, label='Vaccination Coverage', color=list('g'))
        plt.gcf().set_size_inches(8, 10)

        plt.xticks(rotation=90)

        plt.xlabel("Persons fully vaccinated per 100 population", color='b', loc='center')

        plt.ylabel("Countries", color='r')
        plt.title("Percentage of Population Vaccinated by Country")
        plt.legend(loc="upper right")

        # plt.savefig('assets\\statewisestat.jpeg', bbox_inches='tight')
        plt.savefig('assets\\vaccination_stats.jpeg', bbox_inches='tight')
        plt.close()


    overall_stat()
    last14day()
    statewise_stat()
    generate_ccvp()

def get_articles():
    url = 'https://www.google.com/search?q=covid+19&oq=covid+19&aqs=chrome..69i57j69i59l4j69i60.1448j0j9&sourceid=chrome&ie=UTF-8#wptab=s:H4sIAAAAAAAAAONgVuLVT9c3NMwySk6OL8zJecRowS3w8sc9YSn9SWtOXmPU5OIKzsgvd80rySypFJLmYoOyBKX4uVB18uxi4vZITcwpyQguSSwpXsQqmJxflJ-XWJZZVFqsUAwSAwD24HAsbgAAAA'
    datasite = requests.get(url)
    soup = BeautifulSoup(datasite.text, "html.parser")
    fact = soup.findAll('span', class_='UMOHqf EDgFbc')

    global fax
    fax = []
    for stuff in fact:
        fax.append(stuff.get_text().replace('\n', '').replace('’', "'"))
    fax.pop(len(fax) - 1)
    fax.pop(0)
    # fax.pop(-1)

def vacc_dets():
    vaccination_data = pd.read_csv('https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv?raw=true')
    india_vaccination_data = vaccination_data[vaccination_data['location'] == 'India']
    return india_vaccination_data.iloc[-1].to_dict()

def get_global_stats():
    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    return tuple([x.text.replace('\n', '') for x in soup.findAll('div', class_='maincounter-number')])  # Global Cases, Deaths, Recovered

graph()
get_articles()
gcases, gdeaths, grecovered = get_global_stats()

now = datetime.now()
title = 'The Covid Bugle'
pdf_name = f'The Covid Bugle, {now.strftime("%B %d, %Y")}.pdf'

vacc = vacc_dets()
todays_vaccinations, total_vaccination_data = int(vacc['daily_people_vaccinated']), int(vacc['total_vaccinations'])

class PDF(FPDF):
    def header(self):
        self.set_font('times', 'B', 16)
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
        self.set_font('courier', '', 7)
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
        self.cell(-193, 2, 'Learn More: WHO', ln=1, link=WHOsite, align='C')


def generate_pdf():
    # Setup
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_title(title)
    pdf.set_author('TheCovidBugle')

    # Page 1
    pdf.image('assets\\overall stat.jpeg', x=3, y=30, w=100, h=75)  # 640:480, 4:3
    pdf.image('assets\\last14daystat.jpeg', x=103, y=30, w=100, h=75)
    pdf.image('assets\\statewisestat.jpeg', x=20, y=180, w=155)

    pdf.set_font('times', 'BU', 15)
    pdf.cell(0, 160, 'Top Stories')
    pdf.set_font('helvetica', '', 10)
    pdf.set_y(115)
    for articles in fax[:-1]:
        articles = articles.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(w=180, h=6, txt='- '+articles, ln=True, border=False)
    
    pdf.add_page()
    pdf.set_font('times', 'BU', 20)
    pdf.cell(0, 10, 'Vaccination Data')
    pdf.set_x(110)
    pdf.cell(50, 10, 'Global Coverage')

    pdf.set_y(30)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 30, f'Total Vaccinations: {total_vaccination_data}')
    pdf.set_x(110)
    pdf.cell(50, 30, f'Cases: {gcases}')

    pdf.set_y(30)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 40, f'Today\'s Vaccinations: {todays_vaccinations}')
    pdf.set_x(110)
    pdf.cell(50, 40, f'Deaths: {gdeaths}')
    pdf.set_x(110)
    pdf.cell(0, 50, f'Recovered: {grecovered}')

    pdf.image('assets\\vaccination_stats.jpeg', x=20, y=70, w=155, h=200)

    # Saving
    pdf.output(pdf_name)
    print(f'PDF generated at {os.getcwd()}\\{pdf_name}')
    

    # Deleting all graphs
    for img in os.listdir('assets'):
        if img not in ['covpic.png']:
            os.remove(f'assets\\{img}')


generate_pdf()
