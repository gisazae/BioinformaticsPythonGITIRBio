#! /usr/bin/python

""" script que contiene todo el proceso bioinformatico """
def workFlow():
    """ usuario del sistema operativo (linux), se utiliza para identificar los directorios de salida 
	y de parametros de entrada  """
    user="ganoderma"
	""" el cliente envia los parametros o opciones con las que se desea ejecutar el proceso bioinformatico, 
	estas opciones son escritas en un archivo qeu luego es leido por el programa """
    parameter = ConfigParser.ConfigParser()
    parameter.read("gitirBio.parameter")
    """ Preprocesamiento del archivo de entrada (no implementado aun) """
    """ Generar graficos estadisticos de calidad de los reads (reads length y reads quality) """
    """ Ambiguos bases (diferentes letras a: a t g c), low quality (a decision de usuario), 
	eliminar secuencias cortas (a decision del usuario) """
    """ Ensamblaje """
	""" Lectura de parametros (utilizando libreria ConfigParser de python) """
    if(parameter.get('PARAMETER', 'ASSEMBLY')=="TRUE"):
        options={"THREADS":parameter.get('PARAMETER', 'CORES'), "MIRA":parameter.get('PARAMETER', 'MIRA'),\
"RAWSEQ_FORMAT":parameter.get('PARAMETER', 'RAWSEQ_FORMAT'), "PROCESS_ID":parameter.get('PARAMETER', 'PROCESS_ID'),\
"TECH":parameter.get('PARAMETER', 'TECH'), "ASSEMBLY_TYPE":parameter.get('PARAMETER', 'ASSEMBLY_TYPE'),\
"LINUX_USER":user}
	""" se llama la funcion para ensamblar por medio del ensamblador mira con las opciones definidas por el usuario,
	las funciones de ensamblaje estan definidas en el script gitirBio/bioAssembly.py """
        miraAssembler(options)
		""" se llama la funcion para generar graficas estadisticas, las funciones de generacion de graficas para ensamblaje
		estan definidas en el script gitirBio/bioAssembly.py"""
        assemblyStatistics(options)
		""" si el usuario quiere todo el proceso los directorios son creados y el resultado del ensamblaje
		es copiado a otro directrio para la anotacion	"""
        if(parameter.get('PARAMETER', 'ALL_PROCESS')=="TRUE"):
            if(os.path.exists("annotationTarget")):
		os.system("rm -rf annotationTarget")
            os.mkdir("annotationTarget")
            os.system("cp assemblies/mira/assemblies/1sttrial/mira_assembly/mira_d_results/mira_out.padded.fasta \
annotationTarget/")
            query_annotation="mira_out.padded.fasta"
    """ Anotacion """
    """ Anotacion por homology-based inference (old score methodology blast) """
	""" Lectura de parametros (utilizando libreria ConfigParser de python) """
    if(parameter.get('PARAMETER', 'ANNOTATION')=="TRUE"):
         if(parameter.get('PARAMETER', 'BLAST')=="TRUE"):
            if(parameter.get('PARAMETER', 'ALL_PROCESS')=="FALSE"):
                query_annotation=parameter.get('PARAMETER', 'QUERY_ANNOTATION')
            options={"BLAST":parameter.get('PARAMETER', 'BLAST'),\
"THREADS":parameter.get('PARAMETER', 'CORES'), "QUERY_ANNOTATION":query_annotation}
			""" se llama a la funcion para iniciar la anotacion por blast utilizando un pipeline 
			bioinformatico de terceros (http://sfg.stanford.edu/index.html) con las opciones definidas por el usuario, 
			las funciones de anotacion estan definidas en el script gitirBio/bioAnnotation.py """
            blastAnnotationSFG(options)
			""" se llama la funcion para generar graficas estadisticas, las funciones de generacion de graficas para anotacion
			estan definidas en el script gitirBio/bioAnnotation.py """
            annotationStatistics(options)
            """" Anotacion por homology-based inference con hmm (hidden markov model)(hmmer http://hmmer.org/) """
			""" Lectura de parametros (utilizando libreria ConfigParser de python) """
            if(parameter.get('PARAMETER', 'HMM')=="TRUE"):
                if(parameter.get('PARAMETER', 'ALL_PROCESS')=="FALSE"):
                    query_annotation=parameter.get('PARAMETER', 'QUERY_ANNOTATION')
                options={"THREADS":parameter.get('PARAMETER', 'CORES'),\
"QUERY_ANNOTATION":query_annotation,"LINUX_USER":user}
				""" se llama a la funcion para iniciar la anotacion por hmm con las opciones definidas por el usuario, 
				las funciones de anotacion estan definidas en el script gitirBio/bioAnnotation.py """
                hmmscanAnnotation(options)

if __name__ == "__main__":
    """ Entrada del programa (main) """
	""" Manejo de excepciones de los import de las librerias y scripts (gitirBio/bioAnnotation.py, gitirBio/bioAssembly.py) """
    try:
        import ConfigParser
        import os
        #import datetime
        from gitirBio.bioAssembly import *
        from gitirBio.bioAnnotation import *
        #print (datetime.datetime.now())
		""" Incio del proceso bioinformatico """
        workFlow()
        #print (datetime.datetime.now())
    except ImportError as importE:
        print "Import error"
        print importE
    except ConfigParser.NoOptionError as paramsParserE:
        print "Error with Params file: "
        print paramsParserE
    except OSError as osE:
        print "Shell or directory error "
        print osE
    except IndentationError as IndentE:
        print "Error with code identantion: "
        print IndentE
    except Exception as e:
        print "Unexpected error: "
        print e
