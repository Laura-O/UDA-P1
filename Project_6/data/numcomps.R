results = read.table("../cubing-scripts/WCA_export_Results.tsv" , sep = "\t", quote = "", header = TRUE)
persons = read.table("../cubing-scripts/WCA_export_Persons.tsv", sep = "\t",quote = "", header = TRUE)

# aggregate data
numComps <- aggregate(results$competitionId ~ results$personId, FUN = function(x) length(unique(x)))

# set new column names
colnames(numComps) <- c("id","value")

# subset
numComps <- subset(numComps, value > 50)

# add the name + country
numComps <- merge(x=numComps, y=persons[, c("id","name","countryId")], by.x="id", by.y="id")

# sort 
numComps <- numComps[order(numComps$value, decreasing = T),]

# export to csv
write.csv(numComps, file = "numComps.csv", row.names=FALSE)
