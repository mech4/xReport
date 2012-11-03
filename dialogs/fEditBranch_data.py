
def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  key = params.FirstRecord.key
  uideflist.SetData('uipBranch',key)