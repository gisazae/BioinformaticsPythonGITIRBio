#py annotation_organism_filter
#args organisms_table_file_name output_image_name annotation_hits_count family_name
args <- commandArgs(TRUE)
annotationInfo <- read.table(args[1],header=T)
organism <- annotationInfo$organism
png(paste(args[2],".png",sep=""),width=8,height=6,units="in",res=1200)
barplot(table(organism)/as.integer(args[3])*100,ylab="Percentage of hits",space=0.05, main=args[4],xlim=c(0,1),width=0.15)
dev.off()
