class lookupReportClass:
  def __init__(self, config, fr):
    self.config = config
    self.report_code = fr.report_code
    self.group_code  = fr.group_code
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = self.config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT r.report_code, r.report_name, r.class_id, r.form_id, r.periode_type
      FROM {reportclass} r, {reportclassgroup} g
    '''.format(
      reportclass=config.MapDBTableName('reportclass')
      , reportclassgroup=config.MapDBTableName('reportclassgroup'))
    rqsql.WHEREClause = '''
      r.group_id = g.group_id
      and g.group_code = {group_code!r}
      and r.report_code LIKE {report_code!r}
    '''.format(
      group_code=self.group_code
      , report_code='%'+self.report_code+'%%'
    ) 

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("report_code;report_name;class_id")
    rqsql.keyFieldName = "class_id"
    rqsql.setBaseOrderFieldNames("report_code")
  #--
#-- class lookupAccount

class lookupPeriod:
  def __init__(self, config, fr):
    self.config = config
    self.period_code = fr.period_code
    self.period_type = fr.period_type
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT period_code, description, period_id
      FROM {period}
    '''.format(
      period=config.MapDBTableName('period'))
    rqsql.WHEREClause = '''
      period_type = {period_type!r}
      and period_code LIKE {period_code!r}
    '''.format(
      period_type=self.period_type
      , period_code='%'+self.period_code+'%%'
    ) 

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("period_code;description;period_id")
    rqsql.keyFieldName = "period_id"
    rqsql.setBaseOrderFieldNames("period_code")
  #--
#-- class lookupAccount

class lookupBranch:
  def __init__(self, config, fr):
    self.config = config
    self.branch_code = fr.branch_code
    
  def initQueryObject(self, rqsql):
    config = self.config
    mlu = config.ModLibUtils
    rqsql.SELECTFROMClause = '''
      SELECT branch_code, branch_name, branch_id
      FROM {branch}
    '''.format(
      branch=config.MapDBTableName('branch'))
    rqsql.WHEREClause = '''
      branch_code LIKE {branch_code!r}
    '''.format(
      branch_code='%'+self.branch_code+'%%'
    ) 

    #rqsql.GROUPBYClause = "GROUP BY acc.account_code, acc.account_name, acc.account_type" 
    rqsql.setAltOrderFieldNames("branch_code;branch_name;branch_id")
    rqsql.keyFieldName = "branch_id"
    rqsql.setBaseOrderFieldNames("branch_code")
  #--
#-- class lookupAccount