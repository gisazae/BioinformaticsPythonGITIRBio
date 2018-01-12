# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
    
""" Convierte ensamblaje ADN a aminoacidos, se utiliza via TransDecoder (https://transdecoder.github.io/), que permita convertir
un archivo fasta de ADN (ensamblaje o reads) a aminoacidos y que de forma automatica seleccione el marco de lectura mas apropiado 
(transeq (http://emboss.sourceforge.net/apps/cvs/emboss/apps/transeq.html) convierte a los 6 marcos de lectura 
pero no permite escoger automáticamente el marco de lectura más apropiado) """	
def nucl2amino(nThreads,target):
    if(os.path.exists("transdecoder")):
        os.system("rm -fr transdecoder")
    os.mkdir("transdecoder")
    os.system("TransDecoder -t "+target+" --CPU "+nThreads+" --workdir transdecoder -v > \
transdecoder/transdecode.out")
