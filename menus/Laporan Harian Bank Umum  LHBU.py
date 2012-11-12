
def openlistreportOnClick(sender, app):
  formid   = "fMainContainer-LHBU"
  formname = "fMainContainer"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LHBU", "D")
  else:  
    form.Show() 
  
def generateGlobalonClick(sender, app):
  formid   = "fGlobalReport-LHBU"
  formname = "fGlobalReport"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LHBU", "D")
  else:  
    form.Show()