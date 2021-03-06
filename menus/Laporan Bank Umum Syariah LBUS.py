
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
  
def ShowQueryClick(menu, app) :
    formname = menu.StringTag
    state = app.FindForm(formname)
    if state != None :
      dlg = state.FormObject.PyFormObject
    else :
      dlg = app.CreateForm(formname,formname,2,None,None)
    dlg.Show()
    
def generateGlobalonClick(sender, app):
  formid   = "fGlobalReport-LBUS"
  formname = "fGlobalReport"
   
  form = app.FindForm(formid)
  if form == None:
    form = app.CreateForm(formname, formid, 2, None, None)
    form.Show("LBUS", "M")
  else:  
    form.Show() 
