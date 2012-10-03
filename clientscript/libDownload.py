class libDownload:
  def previewStream(self, app, streamWrapper):
    sFileName = app.GetTemporaryFileName("dl")
    fileExt = app.GetExtensionFromMIMEType(streamWrapper.MIMEType)
    if fileExt != "":
      sFinalFileName = sFileName + fileExt
      streamWrapper.SaveToFile(sFinalFileName)
      app.DeleteFile(sFileName)
      app.ShellExecuteFile(sFinalFileName)
    else:
      app.ShowMessage("File extension cannot be identified")
    return
    
  def printStream(self, app, streamWrapper):
    sFileName = app.GetTemporaryFileName("dl")
    fileExt = app.GetExtensionFromMIMEType(streamWrapper.MIMEType)
    if fileExt != "":
      sFinalFileName = sFileName + fileExt
      streamWrapper.SaveToFile(sFinalFileName)
      app.DeleteFile(sFileName)
      app.PrintTextFile(sFinalFileName, "Lucida Console", 8)
    else:
      app.ShowMessage("File extension cannot be identified")
    return


