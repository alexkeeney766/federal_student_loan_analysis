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
data tuition09;
set tuition;
if year = 2008 then delete;
run;


proc sgscatter data = tuition09;
	matrix List_Tuition Constant_APGF Constant_AFSLF Applicants private Rank 
	/ diagonal = (histogram);
run;

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank private;
run;

/* Model 2 */
data tuition2;
set tuition09;
if institution_name = "Howard University" then delete;
if institution_name = "Brigham Young University-Provo" then delete;
run;

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank private;
run;

/* Model 3 */
proc reg data = tuition;
	model List_tuition = constant_apgf Applicants Rank private;
run;

/* Model 4 */
data tuition_private;
set tuition2;
if private = 0 then delete;
run;

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank;
run;


/* Model 5 */
data tuition_public;
set tuition2;
if private = 1 then delete;
run;

proc reg data = tuition;
	model List_tuition = constant_apgf constant_AFSLF Applicants Rank;
run;