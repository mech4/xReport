def formManage(sender, context):
    app = context.OwnerForm.ClientApplication
    dtsid = context.GetFieldValue('dtsid')
    ph = app.CreateValues(['dtsid', dtsid])
    frm = app.CreateForm('XBRL/QryForm', 'XBRL/QryForm', 2, ph, None)
    frm.Show()
    context.Refresh()

def aliasManage(sender, context):
    app = context.OwnerForm.ClientApplication
    dtsid = context.GetFieldValue('dtsid')
    ph = app.CreateValues(['dtsid', dtsid])
    frm = app.CreateForm('XBRL/QryAlias', 'XBRL/QryAlias', 2, ph, None)
    frm.Show()

def enumManage(sender, context):
    app = context.OwnerForm.ClientApplication
    dtsid = context.GetFieldValue('dtsid')
    ph = app.CreateValues(['dtsid', dtsid])
    frm = app.CreateForm('XBRL/QryEnum', 'XBRL/QryEnum', 2, ph, None)
    frm.Show()
