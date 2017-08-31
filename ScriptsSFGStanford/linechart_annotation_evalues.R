#py get_hit_count_by_evalue
#args evalues_table_file_name output_image_name
library(ggplot2)
args <- commandArgs(TRUE)
annotationInfo <- read.table(args[1],header=T,sep=",")
evalue <- sub(" ","",annotationInfo$evalue)
evalue <- as.double(evalue)
nhits <- as.numeric(annotationInfo$number_of_hits)
png(paste(args[2],".png",sep=""),width=6,height=6,units="in",res=1200)
qplot(evalue, nhits, data=annotationInfo, geom="line", xlab="Evalue", ylab="Hit Count", main="Evalue Distribution")
dev.off()
