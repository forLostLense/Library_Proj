subsetting2 <- function() {
  filteredFallData <- X2016FallSemWireless[, c(2,3,5,8:13,16:20)] 
  filteredFallData[filteredFallData == '-'] <- NA
  filteredFallData <- na.omit(filteredFallData)
  # Split by location
  myList <- split(filteredFallData, filteredFallData$WAPID)
  for (i in levels(as.factor(filteredFallData$WAPID))) {
    # Order each sub-list
    my1 <- myList[[i]]
    my1 <- my1[order(my1[,4], my1[,5],my1[,6], my1[,7], my1[,8]),]
    # Create a csv for that file
    write.csv(my1, paste("statsdata", i, ".csv"))
  }
}
subsetting2()
