
def openlistreportOnClick(sender, app):
  formid   = "fMainContainer-LKPBU"
  formname = "fMainContainer"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LKPBU", "M")
  else:  
    form.Show() 
  
def generateGlobalonClick(sender, app):
  formid   = "fGlobalReport-LKPBU"
  formname = "fGlobalReport"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LKPBU", "M")
  else:  
    form.Show() 
