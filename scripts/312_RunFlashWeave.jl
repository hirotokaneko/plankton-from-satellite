using FlashWeave

#Arguments
SIZ = ARGS[1]
OPO = ARGS[2]
TPR = ARGS[3]
FRQ = ARGS[4]
NRM = ARGS[5]

#Define varibles
opo2 = (OPO == "all") ? "" : "$(OPO)."
tpr2 = (TPR == "keep") ? "" : "thinned$(TPR)."
data_path = "../input/asv.$(SIZ).filt.dd.grid.sat.$(opo2)$(tpr2)frq$(FRQ).tsv"

#Loading data
data, header, meta_data, meta_header = load_data(data_path)

#Scaling methods
list_test = ["fz","fz_nz","mi","mi_nz"]

#Output scaled data
for test_name in list_test
	data_sc, header_sc, meta_mask = normalize_data(data, test_name=test_name, header=header, make_sparse=false)

	#Path of output file
	write_path = "flashweave/$(SIZ).$(opo2)$(tpr2)frq$(FRQ).$(test_name)."

	#Writing data & header
	open(write_path*"header","w") do file
		Base.print_array(file, header_sc)
	end
	open(write_path*"mat","w") do file
		Base.print_array(file, Matrix{Float64}(data_sc))
	end
end

#Reconstructing network
sensitive = contains(NRM, "fz")
heterogeneous = contains(NRM, "nz")
netw_results = learn_network(data_path, sensitive=sensitive, heterogeneous=heterogeneous, alpha=0.05)

#Save network
write_path = "flashweave/$(SIZ).$(opo2)$(tpr2)frq$(FRQ).$(NRM)."
save_network(write_path*"edgelist", netw_results)

