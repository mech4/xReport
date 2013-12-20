  
def ShowQueryClick(menu, app) :
    formname = menu.StringTag
    fmode = menu.NumberTag or 0
    state = app.FindForm(formname)
    if state != None :
      dlg = state.FormObject.PyFormObject
    else :
      dlg = app.CreateForm(formname,formname,fmode,None,None)
    dlg.Show()
    
