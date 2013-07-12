class lookupDTS:
  def __init__(self, config, fr):
    self.config = config
    self.DTSName = fr.DTSName
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = self.config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT DTSId, DTSName, PeriodType
      FROM DTS
    '''
    rqsql.WHEREClause = '''
      DTSName like '{0}'
    '''.format('%'+self.DTSName+'%%')

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("DTSName;PeriodType;DTSId")
    rqsql.keyFieldName = "DTSId"
    rqsql.setBaseOrderFieldNames("DTSName")
  #--
#--
 
class lookupReport:
  def __init__(self, config, fr):
    self.config = config
    self.DTSFormCode = fr.DTSFormCode
    self.DTSId = fr.DTSId
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = self.config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT a.DTSFormCode, a.DTSFormDesc, a.DTSFormId, b.DTSFolderId, b.DTSFileName, a.FormType, a.IsEmpty
      FROM DTSForm a, DTSFile b, DTSFolder c
    '''
    rqsql.WHEREClause = '''
      a.DTSFormId = b.DTSFileId
      and b.DTSFolderId = c.DTSFolderId
      and c.DTSId = {0}
      and a.DTSFormCode like '{1}'
    '''.format(str(self.DTSId), '%'+ self.DTSFormCode +'%%')

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("a.DTSFormCode;a.DTSFormDesc;a.DTSFormId;b.DTSFolderId;b.DTSFileName;a.FormType;a.IsEmpty")
    rqsql.keyFieldName = "a.DTSFormId"
    rqsql.setBaseOrderFieldNames("a.DTSFormCode")
  #--
#-- 