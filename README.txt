KEGG_PATH Version 2.0 
Developed By Barah Chbib.
This program is used for KEGG Pathway enrichment analysis, as well as GO analysis.
Tested using Python 2.7, some of the modules aren't available in Python 3.0+ therefor it's recommended to be used in a 2.0+ environment.


1. To begin, after installing python 2.7 make sure that you have pip installed the following:
	scipy, pandas, requests, regex, xlrd, suds, openpyxl. 
2. After changing to the directory which contains the KEGG_PATH. py file, Run the KEGG_PATH.py file by typing in cmd or bash:  python KEGG_PATH.py

OUTPUT:
** Please enter the path of your file or type \ for current directory:
	
3. Here you enter the directory containing the .txt file which contains the gene IDs (best works with UNIPROT ID's). 
   some abbreviations for genes however work, as in the example file (test.txt).

OUTPUT:
** Downloading reference species file, this may take a while..
   Please enter the name of the organism you want to find the shared gene(s) pathways for:

4. Here you enter the name of the Organism which you would like to find the shared pathways for
**** Note in some cases it's you might not find gene entries for certain species, 
	 Also make sure if you have the UNIPROT IDs to choose the right species, 
	 as in the test.txt file, if you choose any organism other than Dictyostelium discoideum the program won't work (because the gene id's are specific to that species).
	 On the other hand you can try different species for test1.txt, since they are only gene abbreviations.(test1.txt was tested using homo sapiens)

 
OUTPUT:
** ['test.txt', 'test1.txt', 'test2.txt']  (this is a list of the .txt files in the directory that you chose)
** Please enter the filename that contains the desired gene(s) to download:

5. Here you should choose the desired .txt file, make sure to include .txt (e.g test1.txt after choosing homo sapiens as species)

OUTPUT:
** Fetching RUNX1 data.... (here the script is interacting with the api from KEGG to extract the different pathways for the genes)
   Fetching ....... ....  
   Converting to uniport id's.... (here the program is converting the keggid's to the uniport ids to interact with the david API)
   Please enter your David user id E-mail: 
6. Here you need to enter the E-mail address you had registered for the DAVID Webservice,
   if you haven't registered please follow the following link:
   https://david.ncifcrf.gov/webservice/register.htm 
   it won't send you a confirmation via E-mail however once done filling out the information you would be ready to use your E-mail.
***** Note if your e-mail doesn't work you will see an error 

OUTPUT:
** Please enter a file name to save your files:

7. Here you would have to enter a common file name for all the different files, 
   e.g: you entered test1, based on the data gathered from DAVID you will have up to 5 files, depending on if there were GO_terms, and KEGG_PATHWAYs for the gene entries.
		These 5 files would be named:
		test1.xlsx (this file gathers all the pathways as well as the go terms for the genes list)
		The files below contain different enrichment data files using DAVID
		test1.KEGG_PATHWAY.chartReport.txt 
		test1.GOTERM_MF_ALL.chartReport.txt
		test1.GOTERM_BP_ALL.chartReport.txt
		test1.GOTERM_CC_ALL.chartReport.txt
8. Finally once the program says Job Completed! you will find your files in the results folder created in the directory where you have your gene list file.




   

   
   
	

 