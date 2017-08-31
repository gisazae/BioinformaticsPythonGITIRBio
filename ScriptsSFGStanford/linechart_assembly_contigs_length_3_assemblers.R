#args contigs_length_table_asembler1_file_name contigs_length_table_asembler2_file_name contigs_length_table_asembler3_file_name
png("assemblycomparison3.png",width=6,height=6,units="in",res=1200)
args <- commandArgs(TRUE)
assemblerInfo1 <- read.table(args[1],header=T,sep=",")
assemblerInfo2 <- read.table(args[2],header=T,sep=",")
assemblerInfo3 <- read.table(args[3],header=T,sep=",")
xrange <- range(0,assemblerInfo1$size,assemblerInfo2$size,assemblerInfo3$size)
yrange <- range(0,assemblerInfo1$sizeCount,assemblerInfo2$sizeCount,assemblerInfo3$sizeCount)
assembler1 <- assemblerInfo1$assembler
assembler2 <- assemblerInfo2$assembler
assembler3 <- assemblerInfo3$assembler
plot(xrange, yrange,
     type="n",
     xlab="Contig length",
     ylab="#contigs"
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
title("Assembly comparison", " ")
dev.off()
