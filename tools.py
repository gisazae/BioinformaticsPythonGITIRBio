# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
    
""" funcion que convierte ensamblaje ADN a aminoacidos, se utiliza la herramienta TransDecoder (https://transdecoder.github.io/), se recomienda cambiar la herramieta
ya que los cambios realizados por sus desarrolladores ya no permite la conversion como un paso individual, la recomendacion es una herramienta que permita convertir
un archivo fasta de ADN (ensamblaje o reads) a aminoacidos y que de forma automatica escoja el marco de lectura mas apropiado 
(transeq (http://emboss.sourceforge.net/apps/cvs/emboss/apps/transeq.html) convierte a los 6 marcos de lectura 
pero no permite escoger automaticamente el marco de lectura mas apropiado) """	
def nucl2amino(nThreads,target):
    if(os.path.exists("transdecoder")):
        os.system("rm -fr transdecoder")
    os.mkdir("transdecoder")
    os.system("TransDecoder -t "+target+" --CPU "+nThreads+" --workdir transdecoder -v > \
transdecoder/transdecode.out")