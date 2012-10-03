class fReportContainer:
  def __init__(self, formObj, parentForm):
    self.repform = None
  #--

  def bLoad(self, sender):
    # procedure(sender: TrtfButton)
    formObj = self.FormObject; app = formObj.ClientApplication

    formid = self.uipData.formid
    ph = app.CreateValues(['param', 0])
    if formid != '': 
      self.repform = self.frReport.Activate(formid, ph, None)
    #--
