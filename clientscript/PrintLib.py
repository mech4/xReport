# request
save     = 0
preview  = 1
printout = 2

class PrintLib:
  def __init__(self):
    # set default request
    self.default_request = printout
        
  def doProcess(self,app,packet,request):
    # handle packet and request type :
    # 0 = Save As
    # 1 = Preview
    # 2 = Print
        
    request = int(request)    
    if packet.StreamWrapperCount > 0:
      streamWrapper = packet.GetStreamWrapper(0)
      self.doRequest(request,app,streamWrapper)
    else:
      app.ShowMessage("Download stream not found")
      
  def doProcessByStreamName(self,streamName,app,packet,request):
    
    request = int(request)
    if packet.StreamWrapperCount > 0:
      streamWrapper = packet.GetStreamWrapperByName(streamName)
      self.doRequest(request,app,streamWrapper)
    else:
      app.ShowMessage("Download stream not found")
  
  def doRequest(self,request,app,streamWrapper):
    # handle packet and request type :
    # 0 = Save As
    # 1 = Preview
    # 2 = Print
    if request == 0:
        self.doSaveAs(app, streamWrapper)
    elif request == 1:
      self.doPreview(app, streamWrapper)
    elif request == 2:
      # *** WISNU **** -- Sementara semua proses print di ubah menjad preview      
      self.doPrint(app, streamWrapper)
      #self.doPreview(app, streamWrapper)
           
  def doSaveAs(self, app, streamWrapper):
    # handle "Save as" request
    sFilter = "All files (*.*)|*.*"
    fileExt = app.GetExtensionFromMIMEType(streamWrapper.MIMEType)
    if fileExt != "":
      sFilter = streamWrapper.MIMEType + " files (*" + fileExt + ")|*" + fileExt + \
        "|" + sFilter
    fileName = app.SaveFileDialog("Save as..", sFilter)
    if fileName != "":
      streamWrapper.SaveToFile(fileName)
    return

  
  def doPreview(self, app, streamWrapper):
    # handle "view" request
    sFileName = app.GetTemporaryFileName("dl")
    fileExt = app.GetExtensionFromMIMEType(streamWrapper.MIMEType)
    if fileExt != "":
      sFinalFileName = sFileName + fileExt
      streamWrapper.SaveToFile(sFinalFileName);
      app.DeleteFile(sFileName)
      if fileExt == ".htm" or fileExt == ".html":
        frmWebViewer = app.CreateForm("fWebViewer", "fWebViewer", 0, None, None)
        frmWebViewer.showWebPage("file://" + sFinalFileName)
      else:
        app.ShellExecuteFile(sFinalFileName)
    else:
      app.ShowMessage("File extension cannot be identified")
    return

  def doPrint(self, app, streamWrapper):
    # handle "print" request    
    if self.CheckMinVersion(app,app.GetVersion(), [3, 0, 7, 0]):
        #streamWrapper.PrintRawText()
        app.PrintRawText(streamWrapper)
    else:      
        #streamWrapper.PrintText("Courier New", 8)
        sFileName = app.GetTemporaryFileName("dl")
        streamWrapper.SaveToFile(sFileName)
        #app.PrintTextFile(sFileName, "Lucida Console", 8)
        #app.ExecuteLocalProgram("prfile.exe",sFileName)    
        app.PrintTextFile(sFileName, "Courier New", 8)

  def CheckMinVersion(self,app,aVersion, aReqVersion):
    return (
        aVersion[0] > aReqVersion[0] or aVersion[0] == aReqVersion[0] and (
            aVersion[1] > aReqVersion[1] or aVersion[1] == aReqVersion[1] and (
                aVersion[2] > aReqVersion[2] or aVersion[2] == aReqVersion[2] and 
                    aVersion[3] >= aReqVersion[3]
            )
        )
    )