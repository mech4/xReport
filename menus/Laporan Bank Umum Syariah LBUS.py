
def reportlistClick(sender, app):
  formid = "fReportContainer"
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formid, formid, 2, None, None)
    form = form.FormContainer
  #--
  form.Show()
  
def openlistreportOnClick(sender, app):
  formid   = "fMainContainer-LBUS"
  formname = "fMainContainer"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LBUS", "M")
  else:  
    form.Show() 
  