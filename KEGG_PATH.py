import sys
import requests
import os
import re
import zipfile
import glob
import pandas as pd
import scipy.stats as stats
import xlrd
from Client import chartReport
from collections import OrderedDict
import time

# pip install scipy, pandas, requests, regex, xlrd, suds, openpyxl
uniport_idz = []
gene_list = []
datas = {'GENE_ENTRY(KEGG)': [], 'GENE_ENTRY(UNIPORT)': [], 'KEGG_PATHWAY_IDs': [], 'KEGG_PATHWAY_NAMEs': [],'GOTERM_BP_ALL': [], 'GOTERM_BP_ALL_Term':[],'GOTERM_CC_ALL':[],'GOTERM_CC_ALL_Term':[],'GOTERM_MF_ALL':[],'GOTERM_MF_ALL_Term':[]}# data frame for genes
Pathway_Col = []
Kegg_ID_Col = []
Id_dictionary = OrderedDict()
Go_term = []
Go_Id = []

def file_location():# This function is used to input the destination of the gene list file
    user_input = raw_input("Please enter the path of your file or type \\ for current directory: ")
    if user_input == "\\":
        print(os.getcwd())
    else:
        while (os.path.exists ('%s' % user_input) == False):
                user_input = raw_input("Error please type an existing directory:")
        if user_input == "\\":
            print(os.getcwd())
        else:
            os.chdir('%s' % user_input)
            print(os.getcwd())
    Species_ref()
    GENES_EXTRACTOR()
    os.chdir('../')
    os.remove("Species_ref.txt")

def Species_ref():#To download the species reference file
    print("Downloading reference species file, this may take a while..")
    if not os.path.exists('Species_ref.txt'):
        download = requests.get("http://rest.kegg.jp/list/organism")
        with open("Species_ref.txt", "wb") as Ref:
            Ref.write(download.content)

def GENES_EXTRACTOR(): # To download the gene files, with all the pathways, amino acid sequences, protein sequences
    organism_choice = str(raw_input("Please enter the name of the organism you want to find the shared gene(s) pathways for:"))
    # If the name of the organism isn't found then stop..... and prompt user that organism doesn't match
    found = False
    with open("Species_ref.txt", "r") as code_organism:
            for line in code_organism:
                ret = (re.findall('(?i)%s' % (organism_choice), line))
                if (len(ret) > 0):
                    found = True
                    organism_new_choice = (line.split('\t')[1])
            while(found==False):
                     organism_choice = str(raw_input("Sorry organism doesn't match please type again:"))
                     with open("Species_ref.txt", "r") as code_organism:
                        for line in code_organism:
                          ret = (re.findall('(?i)%s' % (organism_choice), line))
                          if (len(ret) > 0):
                            found = True
                            organism_new_choice = (line.split('\t')[1])
    # Listing only .txt files within chosen path
    items = os.listdir(".")
    newlist = []
    for names in items:
        if names !=("Species_ref.txt"):
            if names.endswith("."):
                newlist.append(names)
    print(newlist)
    file_choice = str(raw_input("Please enter the filename that contains the desired gene(s) to download:"))
    while(os.path.exists('%s' % file_choice)==False):
            file_choice = raw_input("Error please type an existing file name:")
    #To download the gene files that are named in the .txt file.
    with open("%s" % file_choice)as file_obj:
        start_time = time.time()
        for line in file_obj:
                data = requests.get(("http://rest.kegg.jp/get/%s:%s" % (organism_new_choice, line.strip(' \t\n\r'))))
                if data.status_code == 404:
                    print("Error, couldn't find gene %s." % line.rstrip())
                else:
                    print("fetching %s data..." % line.rstrip())  # rstrip removes the \n characters (enter)
                    PATHWAY_EXTRACTORzzz(data)
        end_time = time.time()
        temp_time = end_time - start_time
        hours = temp_time // 3600
        temp = temp_time - 3600 * hours
        minutes = temp_time // 60
        seconds = temp_time - 60 * minutes

        ###Dictyostelium discoideum
    if (os.path.isdir('Results')) == False:
        os.makedirs('Results')
    os.chdir('Results')
    file_name = Ensembl_Conv(organism_new_choice)
    print("The Job took '%d:%d:%d (hh:mm:ss)'" % (hours, minutes, seconds))
    df = pd.DataFrame(datas)
    df.to_excel('%s.xlsx' % file_name, index=False)
    print("Job Completed!")

def PATHWAY_EXTRACTORzzz(dataz):
    ### extracting Kegg Id's
    linezzz = dataz.iter_lines()
    for linz in dataz.iter_lines():
        if "PATHWAY" in linz:
            for linz in linezzz:
                if "ENTRY"in linz:
                    linz = linz.rstrip().split(None, 3)
                    gene_list.append(linz[1])
                    datas['GENE_ENTRY(KEGG)'].append('%s' % str(linz[1]))
                elif "PATHWAY"in linz:
                    linz = linz.rstrip().split(None,1)
                    wordz = linz[1].split(None,1)
                    Kegg_ID_Col.append(wordz[0].rstrip())
                    Pathway_Col.append(wordz[1].rstrip())
                    for lin in linezzz:
                        if lin[0].isalpha():
                            break
                        else:
                            lin = lin.rstrip().split(None, 1)
                            Kegg_ID_Col.append(lin[0].rstrip())
                            Pathway_Col.append(lin[1].rstrip())
            if len(Kegg_ID_Col) != 0:
                datas['KEGG_PATHWAY_IDs'].append('; '.join(Kegg_ID_Col))
            if len(Pathway_Col) != 0:
                datas['KEGG_PATHWAY_NAMEs'].append('; '.join(Pathway_Col))
    Pathway_Col[:] = []
    Kegg_ID_Col[:] = []

def Ensembl_Conv(organism):
    print("Converting to uniport id's...")
    if not gene_list:
        print "No genes found, exitting program, Please start over."
        file_location()
    else:
        for items in gene_list:
            api = requests.get("http://rest.kegg.jp/conv/uniprot/%s:%s" % (organism, items))
            page = api.text
            line = page.split()
            word = line[1].split(":")
            uniport_idz.append("%s" % word[1])
            Id_dictionary["%s" % items] = ("%s" % str(word[1]))
            if Id_dictionary. has_key("%s" % str(word[1])) == False:
                datas['GENE_ENTRY(UNIPORT)'].append(word[1])
        return David(uniport_idz)

def Parsing_GO (Term,process):
    ###Dictyostelium discoideum
    for key, value in Id_dictionary.iteritems():
        Go_Term(Term,process,value)

def David(idz):
    #print Id_dictionary
    usr_id = raw_input("Please enter your David user id E-mail:")
    dav = (','.join(idz))
    filename = raw_input("Please enter a file name to save your files:")
    usr_id = chartReport.David_Chart(dav, 'KEGG_PATHWAY', usr_id, filename)
    usr_id = chartReport.David_Chart(dav, 'GOTERM_BP_ALL', usr_id, filename)
    Parsing_GO('GOTERM_BP_ALL','biological_process')
    usr_id = chartReport.David_Chart(dav, 'GOTERM_MF_ALL', usr_id, filename)
    Parsing_GO('GOTERM_MF_ALL','molecular_function')
    usr_id = chartReport.David_Chart(dav, 'GOTERM_CC_ALL', usr_id, filename)
    Parsing_GO('GOTERM_CC_ALL','cellular_component')
    return filename

def Go_Term(Term,process,id):
    # processes
    #biological_process
    #molecular_function
    #cellular_component
    requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/downloadStats?aspect=%s&geneProductId=%s" % (process, id)
    r = requests.get(requestURL, headers={"Accept": "application/json"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    responseBody = r.text
    for ch in ['{', '[', ']', '}']:
        if ch in responseBody:
            responseBody = responseBody.replace(ch, '')
    listz = responseBody.split(',')
    current_position = 0
    for itemz in listz:
        current_position += 1
        if '"key":"GO:' in itemz:
            if (itemz.replace('"', '').split("key:", 1)[1]) not in Go_Id and (listz[current_position + 2 % (len(listz))].replace('"', '').split("name:", 1)[1]) not in Go_term:
                Go_Id.append(itemz.replace('"', '').split("key:", 1)[1])
                Go_term.append(listz[current_position + 2 % (len(listz))].replace('"', '').split("name:", 1)[1])
    datas['%s_Term' % Term].append('; '.join(Go_term))
    datas['%s' % Term].append('; '.join(Go_Id))
    Go_term[:] = []
    Go_Id[:] = []

def main():# Running program
    file_location()

if __name__=="__main__":
	main()


