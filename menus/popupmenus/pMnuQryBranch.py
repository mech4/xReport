def AddClick(sender, context):
    app = context.OwnerForm.ClientApplication
    frm = app.CreateForm('fAddBranch', 'fAddBranch', 0, None, None)
    frm.FormContainer.Show()
    context.Refresh()

def EditClick(sender, context):
    app = context.OwnerForm.ClientApplication
    ph = app.CreateValues(['key', context.KeyObjConst])
    frm = app.CreateForm('fEditBranch', 'fEditBranch', 0, ph, None)
    frm.FormContainer.Show()
    context.Refresh()

def ManageClick(sender, context):
    app = context.OwnerForm.ClientApplication
    ph = app.CreateValues(['key', context.KeyObjConst])
    frm = app.CreateForm('fManageBranch', 'fManageBranch', 0, ph, None)
    frm.Show()
    context.Refresh()
