import os
import blast
import ncbi
import interpro

import scraping

from Bio.Blast import NCBIXML
os.system('cls')


if __name__ == "__main__":
    
    #region Genbank
    #########################################
    #             GenBank  NCBI             #          
    #########################################

    # Get ID from NCBI search. (Because if we do this by BioPython, it doesnt order the result by importance)
    # search = "csn3 ovis aries"
    search = input("Search: ")
    id = ncbi.get_id(search)
    # Get info from NCBI (using BioPython)
    protein, gen = ncbi.get_details(id)
    #endregion GenBank

    #region BlastX
    #########################################
    #                Blast X                #          
    #########################################
    # Converting gen to fasta format.
    gen = ">\n"+gen
    os.system("cls")
    print("--Gene Alignments--")
    input(gen)

    # Filter organism using entrez_query
    organism = input("Please write the organism to filter in BlastX: \n")
        # Creating the entrez query
        # Entrez query filter our organism
    entrez_query = organism + '[ORGN]' #[organism]
    # Starting blastx online
    # filename = blast.x(gen, entrez_query=entrez_query) 
    filename = "test_blastx.xml"
    result_handle = open(filename)
    print("...end of process.")

    #Reading results
    blast_records = NCBIXML.parse(result_handle)

    input("...enter for continue...")
    os.system('cls')

    E_VALUE_THRESH = 0.1
    hit_ids = []
    for blast_record in blast_records:
        for i, alignment in enumerate(blast_record.alignments):
            if i < 3:
                for hsp in alignment.hsps:
                    if hsp.expect < E_VALUE_THRESH: 
                        print("---------- Alignment " + str(i) +" ----------")
                        print("sequence:", alignment.title)
                        print("ID: ", alignment.hit_id)
                        hit_ids.append(alignment.hit_id) # Saving ids in a list
                        print("length:", alignment.length)
                        print("e value:", hsp.expect)
    
    #endregion BlastX

    #region GenBank2
    #########################################
    #             GenBank  NCBI             #          
    #########################################
    # Getting FASTA sequences of previous results from (BlastX)
    targeted_fastas = []
    if len(hit_ids)>=3:   
        for i in range(3):
            target_fasta = ">\n" + ncbi.get_details(hit_ids[i],db='protein')
            # Saving the fastas that we want
            targeted_fastas.append(target_fasta)
    else:
        for i in range(len(hit_ids)):
            target_fasta = ">\n" + ncbi.get_details(hit_ids[i],db='protein')
            # Saving the fastas that we want
            targeted_fastas.append(target_fasta)
    

    #endregion GenBank2
    
    #region Interpro
    #########################################
    #               Interpro                #          
    #########################################
    # We run interpro with those results, and save those ids
    
    interpro_jobs = []
    for fasta in targeted_fastas:
        interpro_jobs.append(interpro.run(fasta.upper()))
        
    # Checking if the results are ready.
    for i,job in enumerate(interpro_jobs):
        if interpro.check(job) != "FAIL":
            print("Success interpro job number ",str(i))
    
    # Cleaning the console        
    os.system('cls')
    # Printing links to results, so the investigator can do the next part.
    print("Links to interpro results.")
    interpro_link = 'https://www.ebi.ac.uk/interpro/result/InterProScan/'
    for i,job in enumerate(interpro_jobs):
        print(str(i)+" - "+interpro_link+job+'/')
        
        
    print("-------")
    #endregion Interpro

    #region Functional domain 
    # Select the functional domain region at Genbank
    #########################################
    #           Functional domain           #          
    #########################################
    
    # This part requires humans to choose the right region
    # The investigator uses the previous results to choose
    ready = ""
    while ready != "ready":
        ready = input("Write ready to continue... ")
    
    best_result = input("\nChoose the best result: ")
    
    print("Please select region")
    
    # Substracting 1 so, we give the same region that genebank gives.
    region_begin = int(input("begin: "))-1  
    if region_begin < 1: region_begin = 1
    region_end = int(input("end: "))
    
    # We're getting the protein, but removing the fasta format
    protein = targeted_fastas[int(best_result)]
    protein = protein[2:] # We're cutting > symbol and the \n 

    # Filtering our region
    region = protein[region_begin:region_end]

    #endregion Functional domain

    #region BlastP
    #########################################
    #                Blast P                #          
    #########################################
    fasta_region = ">\n" + region
    os.system('cls')
    print("--Protein Alignments--")
    input(fasta_region)
    
    # Filter organism using entrez_query
    organism = input("Please write the organism to filter: \n")
        # Creating the entrez query
        # Entrez query filter our organism
    entrez_query = organism + '[ORGN]' #[organism]
    # Starting blastx online
    filename = blast.p(region, entrez_query=entrez_query) 
    result_handle = open(filename)
    print("...end of process.")

    # Reading results
    blast_records = NCBIXML.parse(result_handle)
    
    E_VALUE_THRESH = 0.1
    hit_ids = []
    for blast_record in blast_records:
        for i,alignment in enumerate(blast_record.alignments):
            if i<3:
                for hsp in alignment.hsps:
                    if hsp.expect < E_VALUE_THRESH: 
                        print("---------- Alignment " + str(i) +" ----------")
                        print("sequence:", alignment.title)
                        print("ID: ", alignment.hit_id)
                        hit_ids.append(alignment.hit_id) # Saving ids in a list
                        print("length:", alignment.length)
                        print("e value:", hsp.expect)
                    input("")

    #endregion BlastP

    print("End of the road")


'''

CSNK1A1 ovis aries
Chlamydomonas reihhardtii 
0
172
ovis aries

'''
