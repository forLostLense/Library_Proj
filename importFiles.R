temp = list.files(path="HMC Math 158/ezproxy/spu", pattern="*.tsv")
temp
for (i in 1:length(temp)) {
  print("I IS:")
  print(i)
  #allCcl = lapply(paste("HMC Math 158/ezproxy/", temp[i], sep=""), read.delim)
  assign(
    temp[i],
    read.table(
      paste("HMC Math 158/ezproxy/", temp[i], sep=""),
      sep=",",
      fill=TRUE,
      header=TRUE
    )
  )
}


cclnames = function(df) {
  colnames(df) <- c("uuid", "session", "campus", "datetime", "ipSubnet")
}


ccl = rbind(
  ccl201601_report_hashed.csv,
  ccl201602_report_hashed.csv,
  ccl201603_report_hashed.csv,
  ccl201604_report_hashed.csv,
  ccl201605_report_hashed.tsv,
  ccl201606_report_hashed.tsv,
  ccl201607_report_hashed.tsv,
  ccl201608_report_hashed.tsv,
  ccl201609_report_hashed.tsv,
  ccl201610_report_hashed.tsv,
  ccl201611_report_hashed.tsv,
  ccl201612_report_hashed.tsv
)


spu = rbind(
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv,
  spu201601.tsv
)


library(tidyr)
ccl <- separate(ccl, datetime, into = c("start", "end"), sep=19)

library(anytime)
ccl$start <- anytime(ccl$start)
ccl$end <- anytime(ccl$end)




subsetting2 <- function() {
  filteredFallData <- wirelessData2c[, c(2,3,5,8:13,16:20,37)] 
  filteredFallData[filteredFallData == '-'] <- NA
  filteredFallData <- na.omit(filteredFallData)
  # Split by location
  myList <- split(filteredFallData, filteredFallData$WAPID)
  for (i in levels(as.factor(filteredFallData$WAPID))) {
    # Order each sub-list
    my1 <- as.data.frame(myList[[i]])
    my1 <- my1[order(my1[,4], my1[,5],my1[,6], my1[,7], my1[,8]),]
    # Create a csv for that file
    write.csv(my1, paste("statsdata", i, ".csv"))
  }
}
subsetting2()






