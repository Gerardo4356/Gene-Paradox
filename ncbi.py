import os
import requests
from bs4 import BeautifulSoup #pip install beautifulsoup4

from Bio import Entrez #pip install biopython==1.80


# This function gets the id from ncbi trough web scraping
def get_id(consulta, interface=False): 
    
    url="https://www.ncbi.nlm.nih.gov/nuccore/?term=" # csn3+ovis+aries"
    url = url + consulta.replace(" ","+")

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content    
    soup = BeautifulSoup(html_content, "html.parser")

    results = soup.find_all('div', {"class": "rslt"})

    # Getting the data from search
    titles = []
    lengths = []
    links = []
    ids = []
    
    for num,i in enumerate(results):
        if num<4: # Get only this number of results
            line = i.find_all("p")
            print("-----"+str(num)+"-----")                         # Divider
        
            print(line[0].text)                                     # Title of result
            print("   "+line[1].text)                               # Size of ___ (ask Mariel)
            print("   "+i.find('a').get("href"))                    # Link of result
            print("   "+i.find_all('dd')[0].text)                   # ID
            
            # Adding to list
            titles.append(line[0].text)
            lengths.append(line[1].text)
            links.append(i.find('a').get("href"))
            ids.append(i.find_all('dd')[0].text)
    
    
    print("▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣▣")
    
    if not interface: 
        id_selected = int(input("Selecciona ID: "))
        os.system('cls')
        print(titles[id_selected])
        print("   "+lengths[id_selected])
        print("   "+links[id_selected])
        input("--->"+ids[id_selected]+"<---")
        
    if interface:
        return titles, lengths, links, ids
    return ids[id_selected] #ID

def get_details(id,db="nuccore"):
    Entrez.email = 'gerardoc@geneparadox.com'
    
    # Código provicional, sirve para hacer consultas, no da el orden de relevacia de IDS correctos
    # print("resultados")
    # handle = Entrez.esearch(db="nuccore", term=consulta, idtype="acc")
    # record = Entrez.read(handle)
    # for i in record:
    #     print(i)
    
    # Search
    handle = Entrez.efetch(db=db, id=id, retmode="xml")
    records = Entrez.read(handle)
        
    # Filter and save
    # if db=="nuccore":
    #     proteina = records[0]['GBSeq_feature-table'][2]['GBFeature_quals'][6]['GBQualifier_value']
    # Its not required. We shoudld work in removing this feature
    proteina = None
    gen = records[0]['GBSeq_sequence']
      
      
    # Print
    # if db=="nuccore":
    #     print(proteina)  #Proteína
    '''
    print(gen) #Gen
    input("")
    os.system('cls')
    '''
    
    if db=="nuccore": 
        return proteina, gen
    else: 
        return gen

