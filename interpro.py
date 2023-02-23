import requests
import time


def run(fasta):
    # We're using this API
    url = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/run"
    
    # RUN Interpro
    data={'email': "gerardoc@geneparadox.com", 'sequence': fasta}
    r = requests.post(url, headers = {'content-type': 'application/x-www-form-urlencoded', 'Accept':'text/plain'}, data=data)

    # Get RUN ID
    jobId = r.text
    print(jobId)
    return jobId

def check(jobId):
    # Esperamos respuesta favorable del servidor
    tiempo = 0
    status = ""
    while tiempo<600 and status != "FINISHED" and status != "FAILURE":
        url  = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/status/"+jobId
        r = requests.get(url, headers = {'Accept':'text/plain'})
        status = r.text
        print(r.text)
        #Darle más tiempo
        time.sleep(5)
        tiempo = tiempo + 5
    
    if status == "FAILURE": print("Interpro job failed")
    if status == "FINISHED":
        return jobId
    else: return "FAIL"
    
def get(jobId):
    # Pedimos resultados en JSON
    url  = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/result/"+jobId+"/"+"json"
    r = requests.get(url, headers = {'Accept':'text/plain'})
    import pprint
    # pprint.pprint(r.json())

    results = r.json()

    number_of_results = len(results['results'][0]['matches'])

    for i in range (number_of_results):
        try:
            results['results'][0]['matches'][i]['locations'][0]['sites'][0]['description']
            print("-----")
            descripcion = results['results'][0]['matches'][i]['locations'][0]['sites'][0]['description']
            coordenadas = results['results'][0]['matches'][i]['locations'][0]['location-fragments']
            start = coordenadas[0]['start']
            end = coordenadas[0]['end']
            print(descripcion)
            print("Start: " + str(start))
            print("End: " + str(end))
        except:
            pass
   


if __name__=="__main__":
    check





        
        
        
        

