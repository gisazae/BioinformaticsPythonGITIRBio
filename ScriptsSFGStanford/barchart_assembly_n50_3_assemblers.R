#py get_assembly_n50_3_assemblers
#args n50_table_file_name output_image_name
args <- commandArgs(TRUE)
n50T <- read.table(args[1],header=T)
png(paste(args[2],".png",sep=""),width=6,height=6,units="in",res=1200)
barplot(n50T$n50, main="N50",names.arg=n50T$assembler,ylab="Length (bp)")
dev.off()
