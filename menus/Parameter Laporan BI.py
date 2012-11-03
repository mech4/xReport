  
def ShowQueryClick(menu, app) :
    formname = menu.StringTag
    state = app.FindForm(formname)
    if state != None :
      dlg = state.FormObject.PyFormObject
    else :
      dlg = app.CreateForm(formname,formname,2,None,None)
    dlg.Show()
    
