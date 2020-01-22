FILENAME XLSX "/home/amk15b0/dataframePerminant.xlsx" TERMSTR=LF;

PROC IMPORT DATAFILE=XLSX
		    OUT=Tuition
		    DBMS=xlsx
		    REPLACE;
RUN;

PROC PRINT DATA=tuition (obs = 5); 
RUN;
FILENAME XLSX;

/* Model 1 */
proc sql;
create table tuition09 as
select List_Tuition, Constant_APGF, Constant_AFSLF, Applicants, private, Rank,
from tuition
where year > 2008
;
quit;

proc sgscatter data = tuition09;
	matrix List_Tuition Constant_APGF Constant_AFSLF Applicants private Rank 
	/ diagonal = (histogram);
run;

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank private;
run;

/* Model 2 */
proc sql;
create table tuition2 as
SELECT List_Tuition, Constant_APGF, Constant_AFSLF, Applicants, private, Rank 
from tuition
where year > 2009 
and institution_name <> "Howard University"
and institution_name <> "Brigham Young University-Provo"
;
run;


proc reg data = tuition2;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank private;
run;

/* Model 3 */
proc reg data = tuition2;
	model List_tuition = constant_apgf Applicants Rank private;
run;

/* Model 4 */
data tuition_private;
set tuition2;
if private = 0 then delete;
run;

proc sql;
create table tuition_private as
SELECT List_Tuition, Constant_APGF, Constant_AFSLF, Applicants, Rank
from tuition2
where private = 1
; 

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank;
run;


/* Model 5 */
proc sql;
create table tuition_public as
SELECT List_Tuition, Constant_APGF, Constant_AFSLF, Applicants, Rank
from tuition2
where private = 0
; 

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank;
run;