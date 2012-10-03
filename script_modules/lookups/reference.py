class lookupRefByDesc:
  def __init__(self, config, fr):
    self.config = config
    self.reference_desc = fr.reference_desc
    self.reference_name = fr.reference_name
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = self.config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT d.reference_code, d.reference_desc, d.refdata_id
      FROM {referencedata} d, {referencetype} t
    '''.format(
      referencedata=config.MapDBTableName('enterprise.referencedata')
      , referencetype=config.MapDBTableName('enterprise.referencetype'))
    rqsql.WHEREClause = '''
      d.reftype_id = t.reftype_id
      and t.reference_name = {reference_name!r}
      and reference_desc LIKE {reference_desc!r}
    '''.format(
      reference_name=self.reference_name
      , reference_desc='%'+self.reference_desc+'%%'
    ) 

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("reference_desc;reference_code;refdata_id")
    rqsql.keyFieldName = "refdata_id"
    rqsql.setBaseOrderFieldNames("reference_desc")
  #--
#-- class lookupAccount

class lookupRefByCode:
  def __init__(self, config, fr):
    self.config = config
    self.reference_code = fr.reference_code
    self.reference_name = fr.reference_name
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT d.reference_code, d.reference_desc, d.refdata_id
      FROM {referencedata} d, {referencetype} t
    '''.format(
      referencedata=config.MapDBTableName('enterprise.referencedata')
      , referencetype=config.MapDBTableName('enterprise.referencetype'))
    rqsql.WHEREClause = '''
      d.reftype_id = t.reftype_id
      and t.reference_name = {reference_name!r}
      and reference_code LIKE {reference_code!r}
    '''.format(
      reference_name=self.reference_name
      , reference_code='%'+self.reference_code+'%%'
    ) 

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("reference_code;reference_desc;refdata_id")
    rqsql.keyFieldName = "refdata_id"
    rqsql.setBaseOrderFieldNames("reference_code")
  #--
#-- class lookupAccount