from flask import Flask, render_template, request, redirect, url_for
import sys, os
#Este código agrega la carpeta padre a la lista de búsqueda de módulos de Python. 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import blast
import ncbi
import interpro
from Bio.Blast import NCBIXML


app = Flask(__name__)

@app.route('/')
def hello_world():
   print()
   return render_template("s1.html", )

# Definición de la ruta "/genbank_search" que acepta solicitudes POST
@app.route("/genbank_search", methods=["POST"])
def genbank_button_search():
   # Comprueba si la solicitud es una solicitud POST
   if request.method == "POST":
      print("Genbank button pressed")
      search = request.form["genbank_search"]
      titles, lengths, links, ids = ncbi.get_id(search,interface=True)
      
      # Check if the search is valid. If not, change the class of the search bar
      if len(titles)==0:
         genbank_invalid=True
      else:
         genbank_invalid=False
         
      # Get info from NCBI (using BioPython)
      # protein, gen = ncbi.get_details(id)
   return render_template("s1.html", titles=titles, lengths=lengths, links=links, ids=ids, show="block", genbank_invalid=genbank_invalid)

@app.route("/genbank_details/<string:id>")
def genbank_details(id):
   print(id)
   # Get info from NCBI (using BioPython)
   protein, gene = ncbi.get_details(id)
   gene = ">\n"+gene
   return render_template("s1.html",gene=gene)

@app.route("/blastx", methods=["POST"])
def blastx():
   if request.method == "POST":
      gen = request.form["fasta_blastx"]
      organism = request.form["organism_blastx"]
      entrez_query = organism + '[ORGN]' #[organism]
      
      # filename = blast.x(gen, entrez_query=entrez_query) 
      filename = "test_blastx.xml"

      result_handle = open(filename)
      print("...end of BlastX process.")

      #Reading results
      blast_records = NCBIXML.parse(result_handle)

      E_VALUE_THRESH = 0.1
      data = []
      for blast_record in blast_records:
         for i, alignment in enumerate(blast_record.alignments):
               if i < 3:
                  for hsp in alignment.hsps:
                     if hsp.expect < E_VALUE_THRESH: 
                           print("---------- Alignment " + str(i) +" ----------")
                           print("sequence:", alignment.title)
                           print("ID: ", alignment.hit_id)
                           print("length:", alignment.length)
                           print("e value:", hsp.expect)
                           print("identity: ", hsp.identities*100/alignment.length)
                           identity = hsp.identities*100/alignment.length
                           
                           data.append([alignment.hit_id,alignment.title.replace(">","\n >"), alignment.length, hsp.expect, round(identity,2)])
      os.system('cls')
   return render_template("s1.html", blastx=data)

@app.route("/interpro", methods=["POST"])                
def interpro():
   interpro_query = request.form.getlist("interpro-query-list")
   print(interpro_query)
   return str(interpro_query)


if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True)
    











