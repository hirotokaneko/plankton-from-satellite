library("igraph")

#Arguments
args <- commandArgs(trailingOnly=TRUE)
SIZ <- args[1]
OPO <- args[2]
TPR <- args[3]
FRQ <- args[4]
NRM <- args[5]

print("Construct graph") #---------------------------------------
#Load FlashWeave edges
opo2 <- ifelse(OPO=="all","",paste(OPO,".",sep=""))
tpr2 <- ifelse(TPR=="keep","",paste("thinned",TPR,".",sep=""))
subdirec <- paste(SIZ,".",opo2,tpr2,"frq",FRQ,sep="")
filename <- paste("network.",SIZ,".",opo2,tpr2,"frq",FRQ,".",NRM,".tsv",sep="")
DFedges <- read.table(paste(subdirec,filename,sep="/"), stringsAsFactors=FALSE)
print(paste("#edges =",dim(DFedges)[1]))

#Keep positive edges
DFedges_pos <- DFedges[DFedges$V3 > 0,]
print(paste("#positive edges =",dim(DFedges_pos)[1]))

#Convert edges table into a Graph DataFrame
go <- graph.data.frame(DFedges_pos[1:2], directed=FALSE)
E(go)$weight <- DFedges_pos[[3]]

#Detect connected components
components <- igraph::clusters(go, mode="weak")
print("Connected comp sizes:")
components$csize
#Keep largest component
biggest_comp_id <- which.max(components$csize)
vert_ids <- V(go)[components$membership == biggest_comp_id]
g <-igraph::induced_subgraph(go, vert_ids)

print("Detect community") #---------------------------------------
RNGkind(sample.kind = "Rounding")

print("Greedy algorithm")
imc <- cluster_fast_greedy(g)
mem_fast_greedy <- membership(imc)
print(modularity(g, membership(imc)))

print("Infomap")
m_max <- 0.0
for (i in 1:100) {
    set.seed(i)
    imc <- cluster_infomap(g)
    m_i <- modularity(g, membership(imc))
    if (m_max < m_i) {
        m_max <- m_i
        mem_infomap <- membership(imc)
    }
}
print(m_max)

print("Label propagation")
m_max <- 0.0
for (i in 1:100) {
    set.seed(i)
    imc <- cluster_label_prop(g)
    m_i <- modularity(g, membership(imc))
    if (m_max < m_i) {
        m_max <- m_i
        mem_label_prop <- membership(imc)
    }
}
print(m_max)

print("Eigenvector")
imc <- cluster_leading_eigen(g, options=list(maxiter=100000))
mem_leading_eigen <- membership(imc)
print(modularity(g, membership(imc)))

print("Leiden algorithm")
m_max <- 0.0
for (i in 1:100) {
    set.seed(i)
    imc <- cluster_leiden(g, objective_function="modularity")
    m_i <- modularity(g, membership(imc))
    if (m_max < m_i) {
        m_max <- m_i
        mem_leiden <- membership(imc)
    }
}
print(m_max)

print("Louvain algorithm")
imc <- cluster_louvain(g)
mem_louvain <- membership(imc)
print(modularity(g, membership(imc)))

print("Spinglass algorithm")
m_max <- 0.0
for (i in 1:100) {
    set.seed(i)
    imc <- cluster_spinglass(g)
    m_i <- modularity(g, membership(imc))
    if (m_max < m_i) {
        m_max <- m_i
        mem_spinglass <- membership(imc)
    }
}
print(m_max)

print("Random walk")
imc <- cluster_walktrap(g)
mem_walktrap <- membership(imc)
print(modularity(g, membership(imc)))

#Make a table of communities detected by various methods
DFmems <- as.data.frame(cbind(mem_fast_greedy,mem_infomap,mem_label_prop,mem_leading_eigen,
	mem_leiden,mem_louvain,mem_spinglass,mem_walktrap), stringsAsFactors=FALSE)
#Save the table
filename <- paste("community.",SIZ,".",opo2,tpr2,"frq",FRQ,".",NRM,".tsv",sep="")
write.table(DFmems, file=paste(subdirec,filename,sep="/"), sep="\t", quote=FALSE, col.names=NA)

