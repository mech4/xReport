def ShowQueryClick(menu, app) :
    formname = menu.StringTag
    fmode = menu.NumberTag or 0
    state = app.FindForm(formname)
    if state != None :
      dlg = state.FormObject.PyFormObject
    else :
      dlg = app.CreateForm(formname,formname,fmode,None,None)
    dlg.Show()
    
def PengelolaanForm(menu, context) :
    app = context.OwnerForm.ClientApplication
    pyObj = context.OwnerForm.PyFormObject
    pyObj.CallPengelolaan()
    return
    '''           
    ofClass = app.FindForm('XBRL/fReportChecklist')
    app.ShowMessage(ofClass.uipart1.Name)
    st = context.GetFieldValue('reportStatus')
    if st != 'B':
      app.ShowMessage('Pengelolaan hanya untuk form yang belum terisi')
      return
    formname = XBRL/fReportEditor
    fmode = 2
    state = app.FindForm(formname)
    if state != None :
      dlg = state.FormObject.PyFormObject
    else :
      dlg = app.CreateForm(formname,formname,fmode,None,None)
    dlg.Show()
    '''
