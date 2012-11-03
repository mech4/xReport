import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def FormOnSetDataEx(uideflist, params):
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  form_loaditem.setData(uideflist, params)
  if uideflist.uipData.Dataset.RecordCount==0:
    config = uideflist.config
    ds = uideflist.uipData.Dataset
    akt = ('1. LENDING (Long)',
           '',
           '2. TREASURY & INVESTMENT',
           '  a. Long',
           '  b. Short',
           '',
           '3. TRADE FINANCE & BANK GUARANTEE',
           '  a. Long',
           '  b. Short',
           '',
           '4. FUNDING & DEBT INSTRUMENT (SHORT)',
           '',
           '5. LAIN-LAIN',
           '  a. Long',
           '  b. Short',
    )
    for teks in akt:
      rec = ds.AddRecord()
      rec.Aktivitas = teks
    #--
    
