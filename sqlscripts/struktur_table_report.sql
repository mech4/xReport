create table branch (
  branch_id INTEGER NOT NULL,
  branch_code VARCHAR(10),
  branch_name VARCHAR(32),
  description VARCHAR(32),

  primary key (branch_id)
);

create sequence seq_branch;

insert into branch (branch_id, branch_code, branch_name, description)
values (seq_branch.nextval, '517001', 'Bank Panin Syariah Slipi', '-');

insert into branch (branch_id, branch_code, branch_name, description)
values (seq_branch.nextval, '517003', 'Bank Panin Syariah Malang', '-');

insert into branch (branch_id, branch_code, branch_name, description)
values (seq_branch.nextval, '517004', 'Bank Panin Syariah HR Muhammad', '-');

insert into branch (branch_id, branch_code, branch_name, description)
values (seq_branch.nextval, '517005', 'Bank Panin Syariah Ngagel', '-');


create table branchmember (
  member_id INTEGER NOT NULL,
  branch_id INTEGER,
  Kode_Cabang VARCHAR(20),

  primary key (member_id)
);

create sequence seq_branchmember;

insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '000' from branch where branch_code = '517001';
insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '100' from branch where branch_code = '517001';
insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '101' from branch where branch_code = '517001';
insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '102' from branch where branch_code = '517001';

insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '403' from branch where branch_code = '517003';

insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '400' from branch where branch_code = '517004';
insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '402' from branch where branch_code = '517004';

insert into branchmember (member_id, branch_id, kode_cabang)
select seq_branchmember.nextval, branch_id, '401' from branch where branch_code = '517005';

create table enum_int (
  enum_name VARCHAR(32) NOT NULL,
  enum_value INTEGER NOT NULL,
  enum_description VARCHAR(50),
  
  primary key (enum_name, enum_value)
);

create table enum_varchar (
  enum_name VARCHAR(32) NOT NULL,
  enum_value VARCHAR(2) NOT NULL,
  enum_description VARCHAR(50),
  
  primary key (enum_name, enum_value)
);

create table reportclassgroup (
  group_id INTEGER NOT NULL,
  group_code VARCHAR(10),
  group_name VARCHAR(32),
  periode_type VARCHAR(1),
  
  primary key (group_id)
);

create sequence seq_reportclassgroup;

insert into reportclassgroup (group_id, group_code, group_name, periode_type)
values (seq_reportclassgroup.nextval, 'LBUS', 'Laporan Bank Umum Syariah', 'M');

insert into reportclassgroup (group_id, group_code, group_name, periode_type)
values (seq_reportclassgroup.nextval, 'LHBU', 'Laporan Harian Bank Umum', 'D');

insert into reportclassgroup (group_id, group_code, group_name, periode_type)
values (seq_reportclassgroup.nextval, 'LBBUS', 'Laporan Berkala Bank Umum Syariah', 'W');

insert into reportclassgroup (group_id, group_code, group_name, periode_type)
values (seq_reportclassgroup.nextval, 'LKPBU', 'Laporan Kantor Pusat Bank Umum', 'Q');

create table reportclass (
  class_id INTEGER NOT NULL,
  report_code VARCHAR(10),
  report_name VARCHAR(40),
  description VARCHAR(40),
  periode_type VARCHAR(1),
  form_id varchar(60),
  group_id INTEGER,
  
  primary key (class_id)
);

create sequence seq_reportclass;

insert into reportclass (class_id, report_code, report_name, description, periode_type, group_id, form_id)
select seq_reportclass.nextval, 'FORM03', 'LAPORAN FORM 03', '-', g.periode_type, g.group_id, 'FORM_03'
from reportclassgroup where group_code = 'LBUS';

insert into reportclass (class_id, report_code, report_name, description, periode_type, group_id, form_id)
select seq_reportclass.nextval, 'FORM04', 'LAPORAN FORM 04', '-', g.periode_type, g.group_id, 'FORM_04'
from reportclassgroup where group_code = 'LBUS';

update reportclass set form_id = 'FORM_04' where report_code = 'FORM04';

create table report (
  report_id INTEGER NOT NULL,
  report_code VARCHAR(10),
  report_name VARCHAR(32),
  description VARCHAR(32),
  class_id INTEGER,
  branch_id INTEGER,
  period_id INTEGER,
  
  primary key (report_id)
);

create sequence seq_report;

create table reportitem (
  item_id INTEGER NOT NULL,
  description VARCHAR(50),
  report_id INTEGER,
  
  primary key (item_id)
);

create sequence seq_reportitem;

create table period (
  period_id INTEGER NOT NULL,
  period_code VARCHAR(20),
  description VARCHAR(32),
  period_type VARCHAR(1),
  
  primary key (period_id)
);

create sequence seq_period;
