def ViewClick(sender, context):
    frm = context.OwnerForm
    app = context.OwnerForm.ClientApplication
    has_attr = context.GetFieldValue('xhasattrib')
    if has_attr != 'T':
      app.ShowMessage('Tag tidak memiliki attribut.')
      return 0
      
    xid = context.GetFieldValue('xid')
    tagname = context.GetFieldValue('xtag')
    ph = app.CreateValues(['xid', xid], ['tagname', tagname])
    frm = app.CreateForm('XML/qryXAttrib', 'XML/qryXAttrib', 2, ph, None)
    frm.Show()
    context.Refresh()
    