#args identity_table_file_name output_image_name
args <- commandArgs(TRUE)
annotationInfo <- read.table(args[1],header=T,sep="\t")
contig <- as.numeric(gsub("\\D", "", annotationInfo$ContigName))
xrange <- range(contig)            
yrange <- range(annotationInfo$X._identity)
png(paste(args[2],".png",sep=""),width=6,height=6,units="in",res=1200)
plot(xrange, yrange,                          
     type="n",                
     xlab="Contig",                                  
     ylab="% Identity"                           
)
points(contig ,annotationInfo$X._identity,                  
          type="p",                                      
          pch=".",                                                          
          col="blue",
          cex=2.5                            
)
title(args[2], " ")
 
dev.off()
