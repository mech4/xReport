def formCreate(sender, context):
  app = context.OwnerForm.ClientApplication
  tempready = context.GetFieldValue('tempready')
  if tempready != 'F':
    app.ShowMessage('Form telah disetting sebelumnya, \ngunakan pengelolaan form untuk merubah setting.')
    return
  dtsformid = context.GetFieldValue('dtsformid')
  dtsformcode = context.GetFieldValue('dtsformcode')
  ph = app.CreateValues(['dtsformid', dtsformid],['dtsformcode', dtsformcode])
  context.OwnerForm.PyFormObject.ProcData(ph)
  context.Refresh()

def ManForm(sender, context):
  app = context.OwnerForm.ClientApplication
  dtsformid = int(context.GetFieldValue('dtsformid'))
  key = 'PObj:DTSForm#DTSFormId={0}'.format(str(dtsformid))
  ph = app.CreateValues(['key', key])
  dlg = app.CreateForm('XBRL/fFormEditor','XBRL/fFormEditor',2,ph,None)
  dlg.Show()
  context.Refresh()

def setEmpty(sender, context):
  app = context.OwnerForm.ClientApplication
  tempready = context.GetFieldValue('tempready')
  if tempready != 'F':
    app.ShowMessage('Form telah disetting sebelumnya, \ngunakan pengelolaan form untuk merubah setting.')
    return
  dtsformid = context.GetFieldValue('dtsformid')
  dtsformcode = context.GetFieldValue('dtsformcode')
  ph = app.CreateValues(['dtsformid', dtsformid],['dtsformcode', dtsformcode])
  context.OwnerForm.PyFormObject.setEmpty(ph)
  context.Refresh()
