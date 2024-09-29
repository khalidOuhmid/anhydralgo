/*
 ----------------------------------------------------------------------------
             Génération d'une base de données pour
                        SQL Server 2005
                       (7/6/2024 15:39:54)
 ----------------------------------------------------------------------------
     Nom de la base : MLR1
     Projet : Espace de travail
     Auteur : CRIIUT
     Date de dernière modification : 7/6/2024 15:39:25
 ----------------------------------------------------------------------------
*/
use master

go
ALTER DATABASE SAE_TEAM5 SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

ALTER DATABASE SAE_TEAM5 SET MULTI_USER

drop database SAE_TEAM5
go

/* -----------------------------------------------------------------------------
      OUVERTURE DE LA BASE SAE_TEAM5
----------------------------------------------------------------------------- */

create database SAE_TEAM5
go

use SAE_TEAM5
go



/* -----------------------------------------------------------------------------
      TABLE : T_DATA_DTA
----------------------------------------------------------------------------- */

create table T_DATA_DTA
  (
     DTA_ID int identity (1, 1)   ,
     DAT_ID int  not null  ,
     PYS_ID int  not null  ,
     ACT_ID int  null  ,
     EGY_ID int  null  ,
     DTA_VALEUR real  not null  ,
     DTA_NOM char(255)  not null  ,
     DTA_UNITE char(255)  not null  
     ,
     constraint PK_T_DATA_DTA primary key (DTA_ID)
  ) 
go



/*      INDEX DE T_DATA_DTA      */



/* -----------------------------------------------------------------------------
      TABLE : T_REGION_REG
----------------------------------------------------------------------------- */

create table T_REGION_REG
  (
     REG_ID int identity (1, 1)   ,
     REG_NOM char(32)  not null  
     ,
     constraint PK_T_REGION_REG primary key (REG_ID)
  ) 
go



/* -----------------------------------------------------------------------------
      TABLE : T_DATE_DAT
----------------------------------------------------------------------------- */

create table T_DATE_DAT
  (
     DAT_ID int identity (1, 1)   ,
     DAT_DATE datetime  null  
     ,
     constraint PK_T_DATE_DAT primary key (DAT_ID)
  ) 
go



/* -----------------------------------------------------------------------------
      TABLE : T_PAYS_PYS
----------------------------------------------------------------------------- */

create table T_PAYS_PYS
  (
     PYS_ID int identity (1, 1)   ,
     REG_ID int  not null  ,
     PYS_NOM char(255)  not null  
     ,
     constraint PK_T_PAYS_PYS primary key (PYS_ID)
  ) 
go



/*      INDEX DE T_PAYS_PYS      */



/* -----------------------------------------------------------------------------
      TABLE : T_ACTIVITY_ACT
----------------------------------------------------------------------------- */

create table T_ACTIVITY_ACT
  (
     ACT_ID int identity (1, 1)   ,
     ACT_NOM char(255)  not null  
     ,
     constraint PK_T_ACTIVITY_ACT primary key (ACT_ID)
  ) 
go



/* -----------------------------------------------------------------------------
      TABLE : T_ENERGY_EGY
----------------------------------------------------------------------------- */

create table T_ENERGY_EGY
  (
     EGY_ID int identity (1, 1)   ,
     EGY_NOM char(32)  not null  
     ,
     constraint PK_T_ENERGY_EGY primary key (EGY_ID)
  ) 
go



/* -----------------------------------------------------------------------------
      REFERENCES SUR LES TABLES
----------------------------------------------------------------------------- */



alter table T_DATA_DTA 
     add constraint FK_T_DATA_DTA_T_DATE_DAT foreign key (DAT_ID) 
               references T_DATE_DAT (DAT_ID)
go




alter table T_DATA_DTA 
     add constraint FK_T_DATA_DTA_T_PAYS_PYS foreign key (PYS_ID) 
               references T_PAYS_PYS (PYS_ID)
go



alter table T_DATA_DTA 
     add constraint FK_T_DATA_DTA_T_ACTIVITY_ACT foreign key (ACT_ID) 
               references T_ACTIVITY_ACT (ACT_ID)
go




alter table T_DATA_DTA 
     add constraint FK_T_DATA_DTA_T_ENERGY_EGY foreign key (EGY_ID) 
               references T_ENERGY_EGY (EGY_ID)
go



alter table T_PAYS_PYS 
     add constraint FK_T_PAYS_PYS_T_REGION_REG foreign key (REG_ID) 
               references T_REGION_REG (REG_ID)
go



/*
 -----------------------------------------------------------------------------
               FIN DE GENERATION
 -----------------------------------------------------------------------------
*/


ALTER TABLE T_PAYS_PYS
ALTER COLUMN PYS_NOM NVARCHAR(1000);
ALTER TABLE T_DATA_DTA
ALTER COLUMN DTA_VALEUR NVARCHAR(1000);
ALTER TABLE T_REGION_REG
ALTER COLUMN REG_NOM NVARCHAR(1000);

ALTER TABLE T_REGION_REG ALTER COLUMN REG_NOM NVARCHAR(255);
ALTER TABLE T_PAYS_PYS ALTER COLUMN PYS_NOM NVARCHAR(255);
ALTER TABLE T_ACTIVITY_ACT ALTER COLUMN ACT_NOM NVARCHAR(255);
ALTER TABLE T_DATA_DTA ALTER COLUMN DTA_NOM NVARCHAR(255);
ALTER TABLE T_DATA_DTA ALTER COLUMN DTA_UNITE NVARCHAR(255);
ALTER TABLE T_ENERGY_EGY ALTER COLUMN EGY_NOM NVARCHAR(255);

/*
 -----------------------------------------------------------------------------
               FIN DE GENERATION
 -----------------------------------------------------------------------------
*/
