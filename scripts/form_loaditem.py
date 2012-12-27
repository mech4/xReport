# GLOBALS
DEBUG_MODE    = False
ATTR_ORACLE   = 0x01
ATTR_MONGODB  = 0x02 
ATTR_TYPE     = ATTR_ORACLE
MaxLoad       = 100  

import com.ihsan.foundation.pobjecthelper as phelper
import com.ihsan.util.attrutil as attrutil

'''
if ATTR_TYPE == ATTR_ORACLE: 
  from pymongo import Connection
'''

def setData(uideflist, params):
  global MaxLoad
  
  config = uideflist.config
  app = config.AppObject
  app.ConCreate('out')
  helper = phelper.PObjectHelper(config)

  rec = params.FirstRecord
  reportAttr = {}
  attrutil.transferAttributes(helper, 
    ['class_id', 'period_id', 'branch_id']
    , reportAttr, rec)
  attrlist = eval(rec.attrlist)
  beginRow = rec.beginRow

  oReport   = helper.GetObjectByNames('Report', reportAttr)
  if oReport.isnull: return
  report_id = oReport.report_id or -1
  
  if ATTR_TYPE == ATTR_MONGODB:
    '''
    conn  = Connection()
    db    = conn[rec.group_code]
    table = db[rec.report_code]
    '''
    pass
  else:
    itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
  #--
   
  uipData = uideflist.uipData.Dataset
  if ATTR_TYPE == ATTR_MONGODB:
    '''
    for data in table.find({"report_id": report_id}).sort("item_id"):
      item = uipData.AddRecord()
      attrutil.transferAttributes(helper, attrlist, item, data)
    #-- for
    '''
    pass
  else:
    app.ConWriteln('Start loading data...')
    res = config.CreateSQL('''
      select item_id from {0} where report_id = {1}
      order by item_id 
    '''.format(itemName, report_id)).rawresult
    
    app.ConWriteln('Skip data until beginning row...')
    i = 1
    lrow = 0    
    while not res.Eof and lrow < MaxLoad:
      if i >= beginRow:
        oItem = config.CreatePObjImplProxy(itemName)
        oItem.Key = res.item_id
        item = uipData.AddRecord()
        
        attrutil.transferAttributes(helper, attrlist, item, oItem)
      
        lrow += 1
        app.ConWriteln('Load data row ke-%s' % str(i))
      #--
      res.Next()
      i += 1
    #--
  #--
  