from Bio import Entrez #pip install biopython==1.80
from Bio.Blast import NCBIWWW # Para blast

from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup #pip install beautifulsoup4

import time
import os

import ncbi

def blastx(driver, query):
    url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&BLAST_SPEC=&LINK_LOC=blasttab&LAST_PAGE=blastx"      # csn3+ovis+aries"
    driver.get(url)
    
    # Seleccionar cuadro de texto y escribir.
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#seq")))
    element.send_keys(query)

    
    # Seleccionar botón BLAST
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#blastButton1 > input")))
    if input("Pausa. (1 para primer ciclo)") == '1': 
        element.click()
    else: driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID-UUBPSF94013')
    input("OK")
    
    # Esperar a que se quite pantalla de carga
    element = WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#jtitle")))
    
    # Obtener tabla
    element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,'//*[@id="dscTable"]')))
    table = driver.find_element(By.XPATH,'//*[@id="dscTable"]').get_attribute('outerHTML')
    soup = BeautifulSoup(table, "html.parser")

    # Obtener valores de tabla
    # Descripciones
    descripciones = []
    for i in soup.find_all("td", {'class':'c2'}): descripciones.append(i.text)
    # Query Cover   
    query_cover = []
    for i in soup.find_all("td", {'class':'c8'}): query_cover.append(i.text)
    # E Value 
    evalue = []
    for i in soup.find_all("td", {'class':'c9'}): evalue.append(float(i.text))
    # Per Identity
    peridentity = []
    for i in soup.find_all("td", {'class':'c10'}): peridentity.append(float(i.text.replace("%","")))
    # Indice 
    indice = list(range(0,len(descripciones)))


    # Comprobar que sean identicos
    if len(query_cover) == len(descripciones) and len(descripciones) == len(evalue) and len(evalue) == len(peridentity) and len(peridentity) == len(indice):
        # Mayor porcentaje de identidad primero
        identidad_mas_alto = max(peridentity)
        # Creamos un indice de elementos que no queremos
        indice_scrap = [] # Elementos que no queremos
        for i in range(len(evalue)):        
            if peridentity[i] < identidad_mas_alto:
                indice_scrap.append(i)
        # Borramos elementos que no queremos, lo hacemos en reversa para evitar que nos afecte el cambio del índice al borrar
        for i in sorted(indice_scrap, reverse=True):
            query_cover.pop(i)
            descripciones.pop(i)
            evalue.pop(i)
            peridentity.pop(i)
            indice.pop(i)

        # Buscamos E Value más bajo
        evalue_mas_bajo = min(evalue)
        # Creamos un indice de elementos que no queremos
        indice_scrap = [] # Elementos que no queremos
        for i in range(len(evalue)):        
            if evalue[i] > evalue_mas_bajo:
                indice_scrap.append(i)
        # Borramos elementos que no queremos, lo hacemos en reversa para evitar que nos afecte el cambio del índice al borrar
        for i in sorted(indice_scrap, reverse=True):
            query_cover.pop(i)
            descripciones.pop(i)
            evalue.pop(i)
            peridentity.pop(i)
            indice.pop(i)
    
    
        if len(indice) == 1:
            resultado_optimo = indice[0]
        else:
            resultado_optimo = 0

    driver.find_element(By.CSS_SELECTOR, '#btnAlign').click()
    # Esperar que sea visible
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#alignments")))

    # Obtener resultados
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="alignments"]')))
    time.sleep(1) # Lo que logra la desesperación:(
    resultados = driver.find_element(By.XPATH,'//*[@id="alignments"]').get_attribute('outerHTML')
    # Limpiar html
    soup = BeautifulSoup(resultados,"html.parser")
    
    #################################
    # Selección del mejor resultado. 
    #################################
    resultado_optimo = 1
    #################################
    #################################
    
    soup = soup.find_all('div', {"class": "oneSeqAln"})[resultado_optimo]
    soup = soup.find('div', {"class": "dlfRow"})
    
    # Escribir salidas del resultado óptimo
    href = soup.find('a').get('href') # Enlace a genbank
    id_ncbi = soup.find('a').text
    # Consultar secuencia fasta        
    seq = ncbi.get_details(id_ncbi,db="protein")
    fasta_format = ">\n"+seq
    
    os.system('cls')
    
    return fasta_format

def p(sequence, entrez_query = None):
    '''
    Returns the name of the file generated. 
    '''
    NCBIWWW.email = "gerardoc@geneparadox.com"
    # help(NCBIWWW.qblast)
    
    print("Running...")
        
    result_handle = NCBIWWW.qblast(program="blastp", database="nr", sequence=sequence,entrez_query=entrez_query)
    
    filename = 'test_blastp.xml'
    with open(filename, "w") as out_handle:
        out_handle.write(result_handle.read())
    
    result_handle.close()

    
    return filename



def x(sequence, entrez_query= None):
    '''
    Returns the name of the file generated. 
    '''
    NCBIWWW.email = "gerardoc@geneparadox.com"
    # help(NCBIWWW.qblast)
    
    print("Running...")
    
    result_handle = NCBIWWW.qblast(program="blastx", database="nr", sequence=sequence,entrez_query=entrez_query)

    filename = 'test_blastx.xml'
    with open(filename, "w") as out_handle:
        out_handle.write(result_handle.read())
    
    result_handle.close()
    
    return filename


