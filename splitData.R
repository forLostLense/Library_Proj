subsetting2 <- function() {
  filteredFallData <- X2016FallSemWireless[, c(2,3,5,8:13,16:20)] 
  filteredFallData[filteredFallData == '-'] <- NA
  filteredFallData <- na.omit(filteredFallData)
  
  # convert all 0 00 to 24 00
  
  filteredFallData$disconnect_day <- ifelse(filteredFallData$disconnect_hour == '0', filteredFallData$disconnect_day + 1, filteredFallData$disconnect_day)
  
    filteredFallData$connect_day <- ifelse(filteredFallData$connect_hour == '0', filteredFallData$connect_day + 1, filteredFallData$connect_day)
  
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
