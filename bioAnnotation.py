# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# GITIRBio -> GITIR
from gitirBio.tools import *
import os
import csv

""" Anotacion por blast, se utiliza pipeline de terceros SFG (http://sfg.stanford.edu/index.html), las bases de datos utilizadas en formato binario (no fasta) de blast
son la nr (ftp://ftp.ncbi.nlm.nih.gov/blast/db/), la Swiss-Prot (http://www.uniprot.org/downloads), y la TrEMBL (http://www.uniprot.org/downloads)"""
def blastAnnotationSFG(options):
    if(os.path.exists("annotationResultBlast")):
        os.system("rm -fr annotationResultBlast")
    os.makedirs("annotationResultBlast/UniProt_flatfiles")
    """ convertir fasta de bases de datos a bases de datos binarias de blast para mayor velocidad utilizando makeblastdb """
    os.system("blastx -db nr.db -query annotationTarget/"+options["QUERY_ANNOTATION"]+" \
-out annotationResultBlast/"+options["QUERY_ANNOTATION"]+".nrout -outfmt 5 -evalue 0.0001 -gapopen 11 -gapextend 1 \
-word_size 3 -matrix BLOSUM62 -num_descriptions 20 -num_alignments 20 -num_threads "+options["THREADS"])
    os.system("blastx -db swissprot.db -query annotationTarget/"+options["QUERY_ANNOTATION"]+" -out annotationResultBlast/"\
+options["QUERY_ANNOTATION"]+".swssout -outfmt 7 -evalue 0.0001 -gapopen 11 -gapextend 1 -word_size 3 -matrix BLOSUM62 \
-num_descriptions 20 -num_alignments 20 -num_threads "+options["THREADS"])
    os.system("blastx -db trembl.db -query annotationTarget/"+options["QUERY_ANNOTATION"]+" -out annotationResultBlast/"\
+options["QUERY_ANNOTATION"]+".trmblout -outfmt 7 -evalue 0.0001 -gapopen 11 -gapextend 1 -word_size 3 -matrix BLOSUM62 \
-num_descriptions 20 -num_alignments 20 -num_threads "+options["THREADS"])
    os.system("parse_blast.py annotationResultBlast/"+options["QUERY_ANNOTATION"]+".nrparsed annotationResultBlast/"\
+options["QUERY_ANNOTATION"]+".nrout")
	""" Es necesario generar un archivo de filtros(vacio) el cual sera usado por el pipeline SFG (http://sfg.stanford.edu/index.html) """
    ofile  = open("annotationResultBlast/nrcolumnheadersandbadwords", "wb")
    writer = csv.writer(ofile, delimiter='\t', quoting=csv.QUOTE_NONE)
    writer.writerow(("Subject Name","Hsp Expect"))
    writer.writerow(("none","2"))
    ofile.close()
    os.system("totalannotation.py annotationTarget/"+options["QUERY_ANNOTATION"]+" annotationResultBlast/"\
+options["QUERY_ANNOTATION"]+".nrparsed annotationResultBlast/nrcolumnheadersandbadwords annotationResultBlast/"\
+options["QUERY_ANNOTATION"]+".swssout annotationResultBlast/"+options["QUERY_ANNOTATION"]+".trmblout 1E-4 \
annotationResultBlast/UniProt_flatfiles annotationResultBlast/"+options["QUERY_ANNOTATION"]+".sfgannotation")
	""" se filtra el resultado con el fin de solo dejar en el archivo de anotacion los contig que tuvieron alguna coincidencia """
    os.system("cat annotationResultBlast/"+options["QUERY_ANNOTATION"]+".sfgannotation | \
grep -v No_evalue > "+options["QUERY_ANNOTATION"]+".sfgannotation_hits")

""" Anotacion por hmm utilizando hmmer(http://hmmer.org/) , las bases de datos utilizadas son Pfam-A.hmm (ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/) 
y tigrfam.hmm (ftp://ftp.jcvi.org/pub/data/TIGRFAMs/) """
def hmmscanAnnotation(options):
	""" definicion paths de las bases de datos """
    pfam="/home/"+options["LINUX_USER"]+"/db/hmmDB/Pfam-A.hmm"
    tigrfm="/home/"+options["LINUX_USER"]+"/db/hmmDB/tigrfam.hmm"
    if(os.path.exists("annotationResultHmm")):
        os.system("rm -fr annotationResultHmm")
    os.mkdir("annotationResultHmm")
	""" Funcion para convertir el ensamblaje ADN a aminoacidos, es necesario para el proceso de anotacion por medio de hmm, las funciones 
	adicionales se encuentran en el script gitirBio/tools.py """
    nucl2amino(options["THREADS"],"annotationTarget/"+options["QUERY_ANNOTATION"])
	""" proceso de anotacion con hmmer con 2 bases de datos tigrfam y pfamA """
    os.system("hmmscan --cpu "+options["THREADS"]+" -o annotationResultHmm/"+options["QUERY_ANNOTATION"]+".pfm --tblout \
annotationResultHmm/"+options["QUERY_ANNOTATION"]+".tb.pfm  "+pfam+" transdecoder/"+options["QUERY_ANNOTATION"]+\
".transdecoder.pep")
    os.system("hmmscan --cpu "+options["THREADS"]+" -o annotationResultHmm/"+options["QUERY_ANNOTATION"]+".tgrfm --tblout \
annotationResultHmm/"+options["QUERY_ANNOTATION"]+".tb.tgrfm  "+tigrfm+" transdecoder/"+options["QUERY_ANNOTATION"]+\
".transdecoder.pep")

""" Funcion para generar graficas estadisticas a partir de la salida de la anotacion por blast sfg, los scripts que generan las graficas 
estan escritos en python y R """
def annotationStatistics(options):
    if(options["BLAST"]=="TRUE"):
        os.system("annotation1_1.py annotationResultBlast/"+options["QUERY_ANNOTATION"]+".sfgannotation \
annotationResultBlast/hit_nohit")
        os.system("annotation1_2.R annotationResultBlast/hit_nohit annotationResultBlast/sfg \
Blast")