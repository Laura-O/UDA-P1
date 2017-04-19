library(reshape2)

results = read.table("/Users/lohrndorf/Dropbox/Lokal/Privat/cubing-scripts/WCA_export_Results.tsv" , sep = "\t", quote = "", header = TRUE)
competitions = read.table("/Users/lohrndorf/Dropbox/Lokal/Privat/cubing-scripts/WCA_export_Competitions.tsv", sep = "\t", quote = "", header = TRUE, fill = TRUE)

results_years <- merge(x=results, y=competitions[, c("id","year")], by.x="competitionId", by.y="id")
results_years$year <- as.factor(results_years$year)

results_years_melt = melt(results_years, id.vars = c("eventId", "year"),
             measure.vars = c("value1", "value2", "value3", "value4", "value5"))