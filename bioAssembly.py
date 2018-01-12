# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# GITIRBio -> GITIR
import os

""" From GIsaza -> Integrado ABySS parallel y BUSCO Method. 
With  Mira Assembly (http://mira-assembler.sourceforge.net/docs/DefinitiveGuideToMIRA.html) soporta una gran variedad de tecnologias de 
secuenciamiento como electrophoresis sequencing (sanger), 454 pyro-sequencing (GS20, FLX or Titanium), Ion Torrent, Solexa (Illumina) 
ademas soporta tanto DNA como EST/RNASeq (transcriptoma) """
def miraAssembler(options):
""" Se crean los directorios para iniciar el proceso de ensamblaje """
    if(options["MIRA"]=="TRUE"):
        workDir=os.getcwd()
        if(not os.path.exists("assemblies")):
            os.mkdir("assemblies")
        if(os.path.exists("assemblies/mira")):
            os.system("rm -rf assemblies/mira")
        os.makedirs("assemblies/mira/assemblies/1sttrial")
        os.mkdir("assemblies/mira/data")
		""" Si el formato de los reads es fasta es necesario convertirlo a fastq para iniciar ensamblaje con mira """
        if(options["RAWSEQ_FORMAT"]=="FASTA"):
            os.system("perl fasta_to_fastq.pl sequence/"+options["PROCESS_ID"]+".fasta > sequence/"+\
options["PROCESS_ID"]+".fastq")
        rawSeq=options["PROCESS_ID"]+".fastq"
        os.system("cp sequence/"+rawSeq+" assemblies/mira/data")
		""" El ensamblador mira utiliza un archivo de parametros manifest.conf, el archivo es generado a partir de 
		los parametros ingresados por el usuario """
        manifest=open("assemblies/mira/assemblies/1sttrial/manifest.conf","wb")
        if(options["TECH"]=="454"):
            if(options["ASSEMBLY_TYPE"]=="DENOVO"):
                manifest.write("project = mira\njob = genome,denovo,accurate\nreadgroup = 454Reads\ndata = ../../data/"\
+options["PROCESS_ID"]+".fastq\ntechnology = 454")
        manifest.close()
		""" Es necesario cambiar el directorio de trabajo para iniciar proceso de ensamblaje con mira """
        os.chdir("assemblies/mira/assemblies/1sttrial")
		""" Inicia proceso de ensamblaje con mira """
        os.system("mira -t "+options["THREADS"]+" manifest.conf > mira.out")
		""" Se cambia el directorio de trabajo al original """
        os.chdir(workDir)

""" Funcion para generar graficas estadisticas a partir de la salida del ensamblaje, los scripts que generan las png 
estan escritos en python y R """
def assemblyStatistics(options):
    if(options["MIRA"]=="TRUE"):
        if(os.path.exists("assemblies/mira_statistics")):
            os.system("rm -rf assemblies/mira_statistics")
        os.mkdir("assemblies/mira_statistics")
        os.system("assembly1_1.py assemblies/mira/assemblies/1sttrial/mira_assembly/\
mira_d_results/mira_out.padded.fasta assemblies/mira_statistics/mira")
        os.system("assembly1_2.R assemblies/mira_statistics/mira assemblies/\
mira_statistics/mira mira Mira")
        os.system("assembly2.R assemblies/mira/assemblies/1sttrial/mira_assembly/\
mira_d_results/mira_out.padded.fasta Mira assemblies/mira_statistics/mira_base_count")
