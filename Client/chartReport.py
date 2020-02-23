import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from suds import *
from suds.client import Client
from datetime import datetime

def David_Chart(list,GO, login,filename):

    errors = 0
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    print 'url=%s' % url

    #
    # create a service client using the wsdl.
    #
    client = Client(url)
    client.wsdl.services[0].setlocation('https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/')
    #
    # print the service (introspection)
    #
    #print client

    #authenticate user email
    resp = client.service.authenticate('%s' % login)
    while resp != 'true':
        login = raw_input("Error, not valid E-mail, please try again:")
        resp = client.service.authenticate('%s' % login)

    #add a list

    inputIds = '%s' % list
    idType = 'UNIPROT_ACCESSION'
    listName = 'make_up'
    listType = 0
    print client.service.addList(inputIds, idType, listName, listType)

    #print client.service.getDefaultCategoryNames()
    # setCategories
    categorySting = str(client.service.setCategories('%s' % GO))

    #getChartReport
    thd = 0.1
    ct = 2
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print 'Total chart records:', chartRow


    #parse and print chartReport
    resF = '%s.%s.chartReport.txt' % (filename, GO)
    with open(resF, 'w') as fOut:
        fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
        for simpleChartRecord in chartReport:
                categoryName = simpleChartRecord.categoryName
                termName = simpleChartRecord.termName
                listHits = simpleChartRecord.listHits
                percent = simpleChartRecord.percent
                ease = simpleChartRecord.ease
                Genes = simpleChartRecord.geneIds
                listTotals = simpleChartRecord.listTotals
                popHits = simpleChartRecord.popHits
                popTotals = simpleChartRecord.popTotals
                foldEnrichment = simpleChartRecord.foldEnrichment
                bonferroni = simpleChartRecord.bonferroni
                benjamini = simpleChartRecord.benjamini
                FDR = simpleChartRecord.afdr
                rowList = [categoryName, termName, str(listHits), str(percent), str(ease), Genes, str(listTotals), str(popHits), str(popTotals), str(foldEnrichment),str(bonferroni),str(benjamini),str(FDR)]
                fOut.write('\t'.join(rowList)+'\n')
        print 'write file:', resF, 'finished!'
    return login
