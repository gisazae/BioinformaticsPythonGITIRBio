#py get_assembly_contig_count_by_length
#args contigs_length_table_asembler1_file_name contigs_length_table_asembler2_file_name contigs_length_table_asembler3_file_name assembler_name1 assembler_name2 assembler_name3 output_image_name
args <- commandArgs(TRUE)
png(paste(args[7],".png",sep=""),width=6,height=6,units="in",res=1200)
assemblerInfo1 <- read.table(args[1],header=T,sep=",")
assemblerInfo2 <- read.table(args[2],header=T,sep=",")
assemblerInfo3 <- read.table(args[3],header=T,sep=",")
xrange <- range(0,assemblerInfo1$size,assemblerInfo2$size,assemblerInfo3$size)
yrange <- range(0,assemblerInfo1$sizeCount,assemblerInfo2$sizeCount)
#par(xpd=TRUE)
plot(xrange, yrange,
     type="n",
     xlab="Contig length (bp)",
     ylab="Contig count"
)
lines(assemblerInfo1$size, assemblerInfo1$sizeCount,
          type="l",
          lwd=2,
          col="blue"
)
lines(assemblerInfo2$size, assemblerInfo2$sizeCount,
          type="l",
          lwd=2,
          col="red"
)
lines(assemblerInfo3$size, assemblerInfo3$sizeCount,
          type="l",
          lwd=2,
          col="black"
)
#title("Assembly comparison(sector)", " ")
colors <- c("blue","red","black")
legend(xrange[2]-1200, yrange[2],
	c(args[4],args[5],args[6]),
	cex=0.8,                               
	col=colors,                            
	pch=-1,                          
	lty=1,
	title="Assembler"
)
dev.off()
