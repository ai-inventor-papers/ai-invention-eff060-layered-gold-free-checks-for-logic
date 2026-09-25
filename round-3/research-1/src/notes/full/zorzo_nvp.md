URL: https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf | FULL FETCH | 2026-09-24T03:00:18Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf
Type: PDF
Length: 45336 chars

--- Content ---

N-VERSION PROGRAMMING : A FAULT-TOLERANCE 
APPROACH TO RELIABILITY OF SOFTWARE OPERATION 
Liming CHEN 
Algirdas AVlZlENlS 
University of California 
Los Angeles, CA 90024 USA 
Xerox Corporation 
Computer Science Department 
El Segundo, CA 90245 USA 
Abstract 
N-version programing is defined a s the independent 
generation of N2 2 functionally equivalent prograns 
fran the sme i n i t i a l specification. 
A methodology of 
N-version 
programing has been devised and three types 
of special mechanisms have been 
identified 
that are 
needed to coordinate the execution of an N-version 
software unit and to canpare the correspondent r e s u l t s 
generated 
by each version. Two experiments have been 
conducted 
to test the 
f e a s i b i l i t y 
of 
N-version 
programing. 
The results of these experiments a r e 
discussed. In addition, constraints are identified t h a t 
must 
be met 
for effective application of N-version 
programing. 
1. 
Approaches to Software Fault-Tolerance 
The usual method to a t t a i n r e l i a b i l i t y of software 
operation is fault-avoidance (or intolerance) [ l I. 
A l l 
software defects are eliminated prior to operation. 
If 
m e defects remain, the operation is r e l i a b l e only as 
long as the defects are not involved 
i n progran 
execution. 
In most large and canplex software systems 
these fault-avoidance 
conditions 
have 
not 
been 
successfully attained, regardless of a very large 
investment of e f f o r t and resources, 
and 
software 
crashes 
have 
occurred 
during 
operation. 
"his 
observation leads to the conjecture t h a t for r e l i a b l e 
software operation, redundant software i n m e form is 
required t o detect, to isolate, or to recover fran 
effects of the thus f a r uneliminated software defects. 
Achievement of high r e l i a b i l i t y of operation through 
the use of redundant system elements is a fundaental 
principle i n fault-tolerance 
of hardware (physical) 
f a u l t s 141. 
"he use of redundant software to recover 
from software malfunction, 
however, 
requires special 
caution due to the idiosyncratic characteristics of 
software. 
I n contrast with hardware, i n which physical 
f a u l t s predominate, software defects a r e time-invariant 
defects. 
Errors are produced by using the sane inputs 
which trigger the same deficient elements of a progran. 
Therefore, executing duplicate copies of a program does 
not improve the r e l i a b i l i t y of operation with respect 
to software defects. 
Furthermore, while the main cause 
of 
hardware unreliability is a randan failure.that of 
software is its complexity. 
The canplexity of software 
leads t o several d i f f i c u l t i e s . F i r s t , it is d i f f i c u l t 
to construct error-free software. 
Second, software is 
unlikely t o perform canplete self-checking on its own 
outputs. 
Third, it is'difficult 
t o perform run-time 
diagnosis of software i n order to locate the source of 
a software error. 
These observations lead to the 
conclusion t h a t i f redundant software is used i n an 
attempt t o achieve software fault-tolerance, 
then it 
Reprinted from FTCSB 1978, pp. 3-9,0 IEEE 
Proceedings of FTCS-25, Volume 111 
0-8186-7150-5/96 $6.00 0 1996 IEEE 
should t r y to meet the following constraints: (1) It 
does not require complete self-checking; 
(2) it does 
not r e l y upon run-time software diagnosis; and (3) it 
m u s t contain 
independently 
developed 
alternative 
routines for the sane functions, 
Experience 
with 
fault-tolerance 
of 
hardware 
(physical) f a u l t s suggests t h a t functionally equivalent 
alternative routines may 
be employed 
to 
improve 
r e l i a b i l i t y 
of software operation. 
Recently, 
two 
d i s t i n c t approaches have been investigated which anploy 
alternate software routines a s a means to achieve 
software fault-tolerance. 
In the approach of recovery 
blocks 
[2, 33 these routines are organized i n a manner 
similar to the dynamic 
redundancy 
(standby sparing) 
technique i n hardware [41. 
The prime objective is to 
perform run-time 
software error detection and 
to 
implement 
error recovery by taking an alternate path 
of operation. 
A potential alternative to recovery blocks is to use 
software 
redundancy 
analogously 
t o 
the 
s t a t i c 
(replication and 
voting) 
redundancy 
approach 
i n 
hardware 
143. 
The prime objective here is t o mask the 
effects of software defects a t the boundaries of 
designated 
program 
modules. 
The f i r s t technical 
discussion of t h i s approach i n which one of the authors 
took part occurred 
i n February 
1966 a t the IEEE 
Workshop on the Organization of 
Reliable Automata 
i n 
Pacific Palisades, 
Ca. Several suggestions t h a t t h i s 
approach might be a viable method 
of software fault- 
tolerance 
were 
published 
a 
few 
years 
l a t e r 
[ l , 5, 6, 7, 81. In 
1975, 
an experimental research 
project entitled, "N-Version programing" was initiated 
a t UCLA to systematically investigate the f e a s i b i l i t y 
of t h i s approach [ l , 9, 103. 
2. 
Concepts of N-Version Programming 
N-version programing is defined a s the independent 
generation of 
N L 2 functionally equivalent prograns, 
called "versions", fran the same i n i t i a l specification 
[91. 
(This term is preferred to "distinct software,ft 
[81, 
since it bears 
no 
implication 
about 
the 
which 
is vague and d i f f i c u l t t o 
quantify or even qualify, among the 
N versions of a 
program. ) 
"Independent 
generation of programs" here 
means that the programing efforts a r e carried out by N 
individuals or groups t h a t do not interact with respect 
to the programing 
process. 
Wherever 
possible, 
different algorithms and 
programing languages 
or 
translators are used in each effort. 
The i n i t i a l specification is a formal specification 
i n a specification language. 
The goal of the i n i t i a l 
specification is to s t a t e the functional requirements 
canpletely and unanbiguously, while leaving the widest 
113 

possible choice of implementations to the N programing 
efforts. 
It also states a l l the special features that 
are needed in order to execute the set of N version i n 
a fault-tolerant 
manner. 
An 
i n i t i a l specification 
should.define: ( 1 ) the function to be implemented by an 
N-version 
software unit; 
(2) data f o n a t s for the 
special mechanisms: 
comparison vectors (,k-vectors") , 
comparison status indicators (ltcs-indicators"), 
and 
synchronization mechanisms; (3) the cross-check 
points 
k kc-points") 
for 
c-vector 
generation; 
(4) 
the 
canparison (matching or voting) algorithn; and (5) the 
response to the possible outcanes of matching or 
voting. 
We note t h a t "canparison" is used a s a general 
term, 
while "matching" 
refers to the N = 2 case, and 
"voting', 
to a majority decision with 
N 
2. 
The 
canparison algorithn explicitly s t a t e s the allowable 
range of discrepancy i n nunerical results, i f such a 
range exists. 
N 
versions of the 
program 
are 
independently 
generated with respect to the i n i t i a l specification. 
Though different 
i n their implmentation, 
t h e 
N 
versions are assmed to be functionally equivalent. 
Together, these N versions a r e said to form an N- 
version 
software unit. 
h r i n g the developnent of an 
N-version progran, the performance of each version must 
satisfy some 
acceptance criteria of its own before it 
can be integrated into the N-version software unit. 
An 
acceptance 
progran can be used to drive a single 
version for its acceptance testing. 
To 
drive an 
N- 
version software mit a supervisory progran called a 
driver, is needed. 
It is a modified 
acceptance 
program with additional capabilities to coordinate the 
execution of N versions and to vote or to match t h e i r 
correspondent 
results. 
The 
integrated set of an N- 
version software unit and its driver is said to be an 
N-version progran. 
Three types of 
special mechanisms are needed to 
execute an N-version software unit and to match or vote 
the correspopndent results generated by each version. 
These special mechanisms are: 
(1) comparison 
(c-) 
vectors, (2) comparison status (cs-) 
indicators, and 
(3) synchronization mechanisms. 
The points a t which 
c-vectors are generated and employed 
for matching or 
voting are called cross-check (cc-) p i n t s . 
a r e data structures representing a subset 
of 
a 
version's 
local 
program 
s t a t e which is 
interpretable by the driver. 
Meaningful interpretation 
of a c-vector, 
however, 
can only be achieved when a 
cc-point condition has been 
satisfied. 
A 
c-vector 
generated by a version a t a cc-point contains tw types 
of information. 
The canparison variables (c-variables) 
of a c-vector point to values of variables which are t o 
be matched with t h e i r counterparts from other versions. 
The 
status flags of a c-vector indicate whether or not 
some significant events have taken place during the 
generation of 
these c-variables. 
Exanples of such 
events are: end of file, exception conditions detected 
by the system, or conditions defined i n t h e i n i t i a l 
specification. When majority of versions produces the 
results that agree (i.e, 
f a l l within the allowable 
range of discrepancy), these results are treated 
a s 
acceptable results fran t h i s N-version software unit. 
Any version which generates results that d i f f e r frcm 
the acceptable results is designated a s a disagreeing 
version. 
Cs-indicators are used to indicate actions to be 
taken after matching or voting of correspondent c- 
vectors when a cc-point 
condition is satisfied. 
The 
actions to be taken a t the c c - p i n t s after the exchange 
of c-vectors 
depend on: 
(1) whether 
a l l versions 
deliver the c-vectors 
within specified time, and (2) 
whether the c-vectors 
agree or disagree. 
Possible 
outcanes are: (1) continuation, (2) termination of one 
or more versions, and (3) continuation after changes i n 
C-vectors 
the c-vectors of one or more versions on the basis of a 
majority decision. 
Synchronization mechanisms are used to synchronize 
the execution steps of an N-version software unit. 
Each version uses these mechanisms to signal to the 
driver that a c-vector is ready. 
The driver uses these 
mechanisms to control h e n a version 
should 
be 
activated. They are also used by the driver to prevent 
voting or matching before a l l correspondent c-vectors 
a r e ready. 
Originally, 
a version is i n an inactive 
state. When invoked by the driver, it enters into a 
waiting 
state. 
A t 
t h i s s t a t e it waits for a 
synchronization 
signal representing a request 
for 
service fran the driver. 
When t h i s signal is received, 
it transfers into a running state. If any terminating 
condition is signaled by the cs-indicators, then the 
execution of t h i s version is terminated and it goes 
back t o inactive state. 
Otherwise, it generates a c- 
vector upon the satisfaction of a cc-point 
condition, 
then it uses a synchronization signal to notify t h e 
driver that a c-vector is ready, 
and then returns to 
waiting state. 
The s t a t e transitions for a version a r e 
illustrated i n Figure 1. 
It should be noted that s t a t e 
transitions due t o system 
resource allocation and 
deallocation are not of d i r e c t concern to N-version 
programing and are not discussed here. 
INVOKED 
( INACTIVE ) 
INVOKED 
SERVICE REQUIRED-, 
CROSS-CHECK POINT 
CONDITION 
SATISFIED \ 
CROSS-CHECK POINT 
CONDITION 
SATISFIED \ 
TERMINATING CONDITION 
RUNNING 
Figure 1 State Transitions of a version 
A limitation of the N-version approach results fran 
the f a c t that a l l N versions of the program originate 
fran the same 
i n i t i a l 
specification, 
which 
is 
effectively 
t h e "hard core" 
of t h i s method. 
Its 
correctness, completeness, and unambiguity have to be 
assured prior to the N-version programing effort. It 
is our conjecture t h a t either formal 
correctness 
proofs, 
or 
exhaustive 
validations 
of 
i n i t i a l 
specifications when they a r e stated in compact, 
formal 
specification languages 
1111 are much more likely to 
succeed within acceptable cost bounds than proofs or 
validations 
of 
the detailed implementations t h a t 
originate 
fran 
such 
specifications. 
Once 
t h e 
specifications have been 
accepted 
a s correct, the 
proofs or validations of the programs can be replaced 
by the run-time software fault-tolerance provisions. 
The second major observation concerning 
N-version 
programing is that its success a s a method for run- 
time tolerance of software faults depends on whether 
the residual software faults i n each version 
a r e 
distinguishable. We 
define distinguishable software 
faults a s f a u l t s that w i l l cause a disagreenent between 
c-vectors 
a t the specified cc-points 
during 
the 
execution of the N-version 
program that was generated 
fran the i n i t i a l specification. 
fistinguishability is 
affected by the choice of c-vectors and cc-points, a s 
well a s by the nature of the faults thmselves. 
It is 
a fundamental conjecture of the N-version approach t h a t 
the independence of programing efforts w i l l greatly 
reduce 
the probability of identical software defects 
114 

occuring i n two or more versions. 
Together with a 
reasonable choice of c-vectors and c c - p i n t s t h i s is 
expected to turn 
N-version 
programming 
into 
an 
effective method t o achieve tolerance of software 
faults. 
The effectiveness of the e n t i r e approach 
depends on the validity of t h i s conjecture, therefore 
it is 
c r i t i c a l l y important 
t o keep the 
i n i t i a l 
specification 
free of any flaws t h a t would bias the 
independent programers toward 
introducing the same 
software defects. 
The research e f f o r t a t UCLA addresses two 
thus f a r 
unanswered 
questions: 
(1) Which constraints (e.g., 
need 
for formal 
specifications, suitable types of 
problems, 
nature of algorithms, 
timing constraints, 
i-tc.) 
have t o be 
satisfied 
to 
make 
N-version 
programing feasible a t a l l regardless of the cost? 
( 2 ) How does the cost-effectiveness of the N-version 
programing approach compare to the t w o alternatives: 
non-redmdant ("fault-intolerant") programing [l], and 
the "recovery block" [ 2 , 31 approach? 
The scarcity of 
previous results and an absence of formal theories on 
C-version 
programing has led 
us 
to 
choose 
an 
experimental 
approach 
i n t h i s investigation. 
?he 
approach has been 
to 
choose 
m e conveniently 
accessible 
programing 
problems, 
t o 
assess the 
applicability of N-version 
programing, 
and 
then to 
proceed to generate a set of programs. 
Cnce generated, 
the prcgrans are executed 
i n a simulated multiple- 
hardware system, 
and 
the resulting observations are 
applied to refine the methodology 
and to build 
up 
theoretical concepts of N-version programing. 
A more 
detailed discussion of the research approach and 
g w l s 
can be found 
i n 191, 
and 
a detailed discussion of 
experimental results i n [lo]. 
3. A Comparison of Approaches 
In canparison to N-version programing the recovery 
block approach has one apparent advantage. 
In sane 
situations, a mftware system evolves by replacement of 
m e of its modules with newly developed ones. 
The 
replaced modules can 
be 
used 
as 
supplmentary 
alternates t o the new modules. 
'Ihe production cost is 
lower i n t h i s case. 
However, 
there are a l s o 
certain 
disadvantages 
associated with the recovery block approach. 
Fir-st, 
the system s t a t e before entry into a recovery block 
must 
be saved 
until sane reasonable r e s u l t s are 
obtained fran the block. 
Considerable storage overhead 
may 
then 
be 
involved 
for nested 
recovery block 
structures. Second, special precautions are needed to 
coordinate parallel processes within a nested recovery 
block structure. 
Ctherwise the interdependencies anong 
these processes may 
require that a long chain of 
process effects should be undone a f t e r a 
process 
has 
failed 
[ZI. 
Third, some 
intermediate output frcxn a 
recovery block may not be reversible in a real-time 
environment. 
Therefore, 
no recovery action can be 
performed 
before the incorrect output causes 
its 
daaage. 
Fourth, special system support is necessary to 
alleviate the above weaknesses. 
This limits 
the 
generality 
of applications of the recovery block 
technique. 
that i n most cases only qlreasor~ableness" rather than 
"correctness" may 
be checked for by acceptance tests. 
The lack o f established 
procedures to estimate the 
effectiveness of acceptance tests leaves it hard to 
determine i f it is sufficient t o use a given acceptance 
test for a very c r i t i c a l application. 
In view o f the above d i f f i c u l t i e s , 
the N-version 
programing 
approach o f f e r s some advantages over the 
recovery blocks. 
In t h i s approach, 
self-checking 
is 
not 
required. 
Some 
redundant 
software can be 
eliminated; t h i s seems a t t r a c t i v e fran the coverage 
p i n t of view [12]. 
It a l s o o f f e r s the possibility o f 
imnediately masking sane software f a u l t s so that there 
is no delay i n operation. 
In certain applications, N-version programing also 
makes better use of existing hardware fault-tolerance 
resources. 
For 
instance, 
there are recent 
system 
designs for aerospace applications t h a t use redundant 
hardware a t the system level to a t t a i n fault-tolerance. 
The SIFT design [ 133, the Symnetric Multiprocessor [ 141 
and the central computer complex i n the Space Shuttle 
[151 are some exanples. 
In these systems, copies of 
identical 
programs are executed 
i n three o r more 
identical 
processor-memory 
units, and 
voting of the 
results allows detection and masking of 
hardware 
faults. 
Since f u l l system 
r e l i a b i l i t y requires the 
reliable operation of both hardware and software, these 
designs are vulnerable to software deficiencies. 
The 
adoption of N-version 
p r o g r m i n g may 
allow 
such 
systems t o tolerate both hardware and software faults 
without delays caused by the acceptance testing used i n 
the recovery block approach. 
4. 
Implementation of N-Version Programing 
For 
the reason of convenience , 
the 
following 
discussion 
w i l l assme t h a t N-3. 
An extension to N > 3 
is quite straightfoward. 
4.1 
Special Mechanisms 
Implementation 
of special mechanisms (c-vectors, 
cs-indicators, and synchronization mechanisms), 
i n a 
3-version 
progran is illustrated by Figures 2, 3, and 
4. 
The schemata 
shown i n these figures have been 
written 
with the PL/I compiler i n mind. 
It should be 
noted that as a result of emphasis on readability, 
the 
length of some identifiers or labels may not be allowed 
i n m e implementations. 
VERSIONi : PROCEDURE OPTIONS (TASK) ; 
}.EXTERNAL' 
DCL 1 C-VECTORi 
T { status 
flags 
DCL (DiSAGREEi , GOODBYE) 
DCL (SERVICEi , COMPLETEi) EVENT 
DCL FINIS 
BIT(I) 
I N I T ( ' O ' B ) ; 
other declarations; 
DO WHILE (TFINIS); 
WAIT (SERVICE1 ) ; 
COMPLETION (SERVICEi) = 'O'B; 
IF 1GOODBYE & TDISAGREEi 
comparison variables 
EIT(1 )'EXTERNAL; 
EXTERNAL; 
THEN CALL PRODUCE; 
ELSE FINIS = '1'B; 
COMPLETION (COMPLETEi) = '1'B; 
Finally, we also note that the effectiveness of the 
acceptance test is often quite d i f f i c u l t t o measure. 
In many cases, the procedure used to verify r e s u l t s 
fran the execution of a program can be 
as canplex 
as 
PRODUCE : PROCEDURE ; 
the program itself. For exanple, it is easy to check 
produce C-VECTORi ; 
the consistency of the nunber 
of elements i n a set 
END PRODUCE; 
before and a f t e r execution of a sorting routine. 
It. is 
more d i f f i c u l t to verify t h a t a l l of the data items a r e 
indeed 
sorted as specified. 
It is even more d i f f i c u l t 
Figure 2 
A Schema f o r the i-th Version 
t o verify t h a t the elments of the set before and a f t e r 
the sorting are the same. 
Therefore, it is obvi.ous 
END; 
END VERSIONi 
of Code 
115 

ACCEPTANCE: 
PROCEDURE OPTIONS (MAIN); 
DCL VERSIONi 
ENTRY; 
DCL 1 C VECTORi 
EXTERNAL, 
GOODBYE 
B I T ( 1 ) 
EXTERNAL ; 
DCL SERVICEi 
EVENT 
EXTERNAL, 
COMPLETEi 
EVENT 
EXTERNAL; 
other declarations ; 
COMPLETION (SERVICEi) = ' 1 ' B ; 
COMPLETION (COMPLETEi) = ' O ' B ; 
CALL VERSIONi TASK EVENT ( F I N I S i ) ; 
DO WHILE (need more service); 
WAIT (COMPLF?Ei )i 
COMPLETION (COMPLETEi) = ' O ' B ; 
process C VECTORi; 
IF-~need gore service THEN GOODBYE = ' 1 ' B ; 
COMPLETIGN ( S r R V I C E i ) = '1 'B; 
END; 
WAIT ( F I N I S i ) ; 
END ACCEPTANCE ; 
F i g u r e 3 
A Schema for an Acceptance Program 
DRIVER: 
PROCEDURE OPTIONS (MAIN) ; 
DCL (VERSION1 , VERSIONZ, VERSION3) ENTRY; 
declare (C VECTOR1 , C VECTORZ, 
C VECTOR3); 
DCL (DISAGFEEl , DISAGEEEZ, DISAGEEE3, GOODBYE) 
B I T ( 1 ) EXTERANL; 
DCL (SERVICEI, 
COMPLETE1 , 
SERVICEZ, COMPLETEZ, 
SERVICE3, COMPLETE3) EVENT EXTERNAL; 
other declarations; 
i n i t i a l i z e (SERVICEi. COMPLETE11 as i n ACCEPTANCE: 
CALL VERSIOi1 TASK EVENT ( F I N I S l ) ; 
CALL VERSIONZ TASK EVENT ( F I N I S Z ) ; 
CALL VERSION3 TASK EVENT ( F I N I S 3 ) ; 
DO WHILE (need more service): 
WAIT (COMPLETE1 ,-COMPLETE2, 
COMPLETE3) ; 
process (C VECTOR1 , C VECTORZ, C VECTOR3) ; 
I F lDISAGRrE1 THEN CORPLETIONICOflPLETEl ) = ' O ' B : 
I F .DISAGREE2 
THEN COMPLETI3N (COMPLETEZ) = 0' B f 
I F lDISAGREE3 THEN COMPLETION(COMPLETE3)='O'B; 
I F ineed-more-service 
THEN GOODBYE='l ' B ; 
COMPLETION(SERVICE1 ) = I 1 '6; 
COMPLETION( SERVICEZ)=' 1 ' B ; 
COMPLETION (SERVI CE 3) = ' 1 ' B ; 
END ; 
WAIT ( F I N I S 1 , F I N I S Z , F I N I S 3 ) ; 
END DRIVER; 
F i g u r e 4 
A Schema f o r a Driver 
When Figures 2, 3, and 4 are applieo "i" muld be 
replaced 
by 
1 , 2, or 3. 
VERSIONi is the i-th version 
of a 
3-version 
software unit, 
ACCEPTANCE is 
the 
acceptance progran with respect to VERSIONi and DRIVER 
represents a driver which exercises 
a 
+version 
software unit. 
C-VECTORi represents a c-vector to be 
produced 
by the i-th 
version. 
The 
cs-indicator 
DISAGREEi 
shows 
whether 
or not C-VECTORi 
agrees with 
the correspondent acceptable results. 
Another cs- 
indicator, 
GOODBYE, represents wbether or not a normal 
terminating 
condition 
is 
satisfied. 
The 
synchronization 
primitive, SERVICEi, is used to signal 
a request fran the driver for the service of the i-th 
version. 
Another synchronization primitive, CCMPLETEi, 
is used by the i-th version t o signal the 
that 
C-VECTORi is ready. 
driver 
From Figures 2, 3, and 4, it is evident t h a t the 
implementation of special mechanisms for N-version 
programing is relatively simple. 
This is illustrated 
by the exanple i n Appendix 1. 
4.2 
Inexact Votinz 
For nunerical computations, twu types of deviations 
may appear i n the results. 
The first type is an 
"expected" 
deviation due to the inexact 
hardware 
representation or the data sensitivity of a particular 
algoritfnn. 
The second type 
is 
an 
Ymexpected" 
deviation 
due 
t o 
either 
inadequate 
design or 
implementation of an algorithm, or a malfunction of 
hardware. 
Either type of deviation may cause results 
obtained fran different 
nunerical 
algorithms 
to 
disagree with each other. me standard voting process 
which requires t h a t 
the majority of correspondent 
r e s u l t s 
should 
have exactly t h e same values to 
determine an acceptable result is not applicable here. 
Different voting processes need to be devised to handle 
voting with non-identical 
results. 
These 
voting 
processes will be called "inexact voting". 
In general, adaptive and non-adaptive voting are two 
alternatives which may be applied to perform inexact 
voting. 
Assune t h a t R1, R2, and R3 
are correspondent 
results used to determine the voted result, R. 
Then i n 
the approach of adaptive voting, a s suggested i n [161, 
where (1) W1, 
W2, 
W3, 
a r e weights of 
R1, 
R2, 
R3 
respectively; 
(2) W1, W2, W3 a r e positive values; and 
(3) Wl+W2+W3=1. 
These weights may be dynamically 
calculated based on the values of R1, R2, and R3. 
The 
major intent is to 
favor acceptable results and to 
minimize 
the effect of a disagreeing result. 
In other 
w r d s , R is constructed to be a continuous function of 
R1, 
R2, 
and R3, t h a t w i l l s n w t h out the effect of a 
disagreeing result. 
To 
cmpute 
the 
weights 
of 
correspondent results, 
several schemes are available. 
The performance of a 
scheme is influenced by its 
"tolerance" 
parameter, which is a measure of the 
allowable noise level and could be optimally determined 
fran the magnitudes of expected 
results and noisy 
results. 
R = Wl*Rl + W2rR2 + W3aR3, 
The adaptive voting approach may suffer 
from the 
following disadvantages: 
(1) 
The optimal tolerance 
parameter is d i f f i c u l t t o 
determine 
unless 
t h e 
characteristics of the expected values and noisy values 
a r e knom well i n advance. 
( 2 ) The remaining effect of 
noise may not be acceptable i n m e cases. 
(3) If the 
voted result w i l l be used a s input for next cycle of 
canputation then the accunulation of residual effects 
of 
noise may cause a serious problem. 
(4) 
If 
implemented 
i n software, the adaptive voter may be 
quite slow. 
As a contrast, the non-adaptive voting approach uses 
an allowable discrepancy range and differences of pairs 
of correspondent results in determining R. 
Assume t h a t 
6 is the allowable discrepancy range, and D i j is the 
absolute value of the difference between 
R i and 
R j . 
Then an acceptable R may be reached by adopting one of 
the following tm strategies: (1) if maximun (D12, D23, 
D31) 
6 or 
(2) if minimimun (D12, D23, D31) <_ 
6. 
The first strategy 
requires D12, D23, 
D3l 
be known 
before 
R can be determined. 
In the second strategy, 
however, 
if 
D12 L 6 
R 
can be determined without 
knowing D23 and C Y . 
The non-adaptive 
voting approach is not without 
flaws. 
F i r s t , the value of 6 is very d i f f i c u l t to 
determine dynamically for each instance of voting. 
Second, 
the strategy which uses the principle of 
maximun (D12, D23, D32) L 6 is too rigid since an 
erroneous r e s u l t may easily cause a D i j which is larger 
than 
S. 
Acceptable results may not be reached 
even 
when 
two of 
t h e three correspondent results a r e 
reasonably close. 
Third, the strategy which 
uses the 
principle of minimun (D12, D23, D31) 
6 may encounter 
116 

situations where each version may 
have 
different 
effects on the outcane of voting. 
These situations are 
illustrated better with the following exanples. 
AsSUlle 
t h a t the allowable discrepancy range is 0.9 and ( i ) 
expected 
RI = 117.0, 
(ii) expected 
R2 = 116.5, 
and 
(iii) expected R3 = 115.8. 
In t h i s case, (i) i f Only 
Rl or A3 is erroneous, an acceptable 
R 
can still be 
generated, 
(ii) but 
i f R2 
is erroneous then no 
acceptable R can be generated. 
'herefore, there is no inexact voting approach which 
can be 
applied 
satisfactorily to a l l cases. 
The 
success of an 
approach usually 
depends 
on 
the 
designer's 
knowledge about (1) the data sensitivity of 
each algorithm, 
(2) the limitations 
of 
hardware 
representations, 
and 
(3) the allowable ranges of 
discrepancies for each instance of voting. 
5. 
Feasibility Studies of N-version Programming 
A t an early stage of the investigation of N-version 
prograrming, 
it 
was 
decided 
to conduct a few 
experiments to gain m e insight into the f e a s i b i l i t y 
of t h i s technique. 
Three objectives were set for the 
experiments. 
They were: (1) to study the generality 
and 
the ease of the implementation of N-version 
programing; (2) to gain qualitative and 
quantitative 
data on effectiveness of 3-version programing; and (3) 
to observe and identify problems or d i f f i c u l t i e s i n 
using 3-version programing. 
Three c r i t e r i a were used to select target problems 
for feasibility studies. F i r s t , a target problem needs 
to be relatively complex 50 that there is reasonably 
good 
possibility t h a t residual software defects w i l l 
occur i n its implementing programs. 
Second, 
the 
progran 
implementing a target problem 
should be of 
manageable size to f a c i l i t a t e the 
instrunentation 
efforts. 
Third, 
since programing is an expensive 
activity, it is very desirable t h a t a target problem 
should allow convenient generation of multiple versions 
of a progrzn. 
5.1 
The 3-version Y E S Frogran Experiment 
MESS 
Qini-Text 
Editing Sygtem) 
was 
a 
program 
assignnent 
for the graduate seminar course E2262, 
offered a t UCLA in the Spring quarter of 
1976. 
A 
preliminary report on 
Y S S is contained in [91. 
The 
specification of M E S S and 2 detailed description of the 
results can be found 
in [lo!. 
From the experience and 
the results of the HESS 
experiment the following conclusions were reached: (1) 
The 
methodology 
used 
to 
implement 
N-version 
programing (see Sections 2 and 4 ) is relatively simple 
and can be generalized to other similar applications. 
(2) The 
results attained 
fran executing +version 
programs are encouraging. 
The 
effectiveness 
of 
3-version 
programing 
seems 
to 
warrant 
further 
investigation. 
(3) 
The 3-version 
redundancy 
was 
succesfully 
applied 
a t subroutine 
(module) 
level, 
rather than a t canplete program level. 
This show t h a t 
selective 
application 
of 
N-version 
redundancy t o 
certain c r i t i c a l parts o f longer 
programs 
can be a 
practical alternative. 
5.2 
RATE, 
standing 
for 
Region 
Approximation 
and 
Temperature Estimation, 
is a 
program for computing 
dynamic changes of temperatures a t discrete points i n a 
particular region of a plain. 
The temperature changes 
are governed by the followi?g equation: 
The 3-version R4TE FV0gt-F Experiment 
where the coefficients A, B, C, D, E, and 
F are some 
constants, 
The problem specification for RATE (given i n [lo]) 
s t a t e s the requirements for a stand-alone RATE program 
lhis specification is written to make a 
RATE 
program 
easily instrunentable for the p u r p s e of conducting 
experiments on 3-version programing. 
There are four types of output data structures 
described i n the problem specification for RATE. 
The 
MESSAGE 
type of data informs the 
driver 
about 
execution termination conditions or the time a t which 
r e s u l t s are produced. 
The FAClDR 
type 
of 
data 
represents the s i z e and 
the units of the specified 
region. 
The GRID type of data represents a 
point 
i n 
the concerned region and its previous and Current 
temperatures. 
?he 
CUTPUT-REWEST 
type 
of 
data 
indicates the p i n t s and the times for which outputs 
are requested. 
Each of these types of data can be 
treated 
as a c-vector 
t h a t represents r e s u l t s to be 
voted upon. 
The problen specification for RATE 
also gives an 
algorithm specification for: (1) terminating conditions 
for program execution; ( 2 ) cc-points a t which r e s u l t s 
should be 
produced; 
and 
(3) 
an 
algorithm 
that 
implements a nunerical 
approximation for solving the 
partial differential 
equation 
shown 
above. 
Three 
a l g o r i t h s , 
(ALCI, 
ALC2, 
Affi3) were 
selected that 
implemented three different nunerical methods to solve 
the partial differential equation. 
While an individual 
RATE 
specification can employ only one of 
these 
a l g o r i t h s . 
the existence of three different choices 
provides a higher probability of avoiding related 
programing 
errors 
i n 
the N-version 
programing 
experiment. 
The problem of RATE 
was 
given a s a programing 
assignnent for the greduate seminar 
course, E2262, 
offered a t UCLA i n the Spring quarter of 
1977. 
The 
students were asked to form teams of two people t o 
solve the RATE problem. 
There were three students who 
preferred 
to w r k alone and 
their requests were 
granted. 
Totally, there were 
18 teams thus formed. 
Two of these teams failed t o turn in t h e i r programs. 
That left 16 programs available for t h i s investigation. 
The 
RATE 
specification was 
distributed to a l l 18 
programing 
teuns. 
Algorithms 
1, 
2, 
and 
3 
were 
specified i n s i x cases. 
Each of the RATE programs was 
written i n Pl/I(F), and executed on the IBM 
360/91. 
Each 
program 
consisted 
of 
more than 600 
P l / I 
statements. 
The period allowed for the developnent of 
the R4TE programs was four weeks. 
The R4TE programs were collected and tested 
against 
s i x text cases. 
Based on the results of these tests, 
the best four 
programs were 
selected 
for 
further 
experiments. 
Besides, 
there were 
three programs 
developed by the authors. 
Hence, we 
had 
7 programs 
available for subsequent studies on the f e a s i b i l i t y o f 
3-version programing. 
Three of the selected programs 
implemented 
ALG1. 
Two 
each of the remaining four programs implemented 
ALC2 and ALC3 respectively. 
The 
seven 
programs were 
instrunented, grouped into 12 combinations, and tested 
with 32 test cases. 
Totally, 
there were 384 
cases 
tested. 
Among them: 
( 1 ) 290 cases contained 
( 2 ) 71 cases contained 
one bad version, 
(3) 18 cases contained 
two bad versions, and 
(4) 
5 cases contained 
three bad versions. 
no bad version, 
Naturally, the 290 cases o f three good 
versions 
generated 
acceptable 
results, 
and 
the 
18 cases 
containing two bad versions and the 5 cases containing 
three bad versions generated unacceptable results. For 
the 71 cases containing a single bad version, 59 
cases 
117 

generated acceptable results and 
12 cases generated 
unacceptable results. 
These 
12 cases contained 
a 
version which malfunctioned 
i n a 
way t o cause the 
system to abort the execution of the involved +version 
unit. 
Based on these results, 
we 
have observed 
t W 
d i f f i c u l t i e s which require special 
attention i n N- 
version 
programing: 
(1) In m
e
 situations, 
one 
version of code developed an 
error that caused the 
operating system of the IBM 
360/91 
canputer 
t o take 
over execution, 
An exanple is the improper handling of 
conversion errors by a version. 
A s a r e s u l t , both the 
involved version and its associated 3-version program 
were aborted by the operating system. 
Even though the 
other 
tm 
versions were 
executing properly, 
the 
3-version program could not proceed further past t h i s 
point to generate correct results. 
(2) The logic being 
implemented by one version of the code may be correct, 
incorrect, or it may be altogether missing. 
For cases 
in which missing logic is the cause of incorrect 
software operation, error symptoms fran faulty versions 
tend to be the same. 
There is a possibility t h a t 
faulty but identical results (due to missing logic) may 
outvote correct results. 
6. 
Conclusions 
The results obtained f r m the MESS 
and 
the RATE 
experiments are of mixed 
nature. 
There are several 
encouraging 
points: 
(1 ) 
The 
methodology 
f o r 
implementing N-version programming is relatively simple 
and can be generalized to other similar applications; 
(2) In 
m e cases, 
+version 
p r o g r m i n g has been 
effective in preventing 
failure 
due 
t o 
defects 
localized i n one version of code; and (3) tJ-version 
programing can be a practical 
approach 
i f it is 
selectively applied at subroutine level. 
On the other 
hand, there are sane negative points: 
(1) 
I n the 
enviroment 
of 
sane 
operating 
systems, 
certain 
implementation defects of a version may 
cause its 
associated +version progran to be aborted by the O.S.; 
and 
(2) I f missing 
program 
functions 
are 
the 
predminant 
software 
defects, 
then 
N-version 
programing may not be an effective approach. 
I n addition t o the experimental results, we 
have 
.identified 
Sane 
situations 
i n 
which 
N-version 
programing appears to 
be not effective or is not 
applicable. 
The most significant limitations are 
discussed below. 
(1) In a real-time environment a system failure may 
be 
caused 
by 
performance 
limitations rather 
than 
functional 
problems. 
TWO typical exmples are timing 
constraint violations and 
resource contentions. 
A 
likely source 
for these problems is systen overload. 
N-version programing may produce 
adverse effects i n 
these situations. 
(2) In certain other circunstances, there exists no 
unique path t o the solution of a problem. 
Step-by-step 
matching or voting of correspondent results cannot be 
used 
a s a criterion of correctness. 
Therefore, N- 
version programing is not applicable for situations i n 
which d i s t i n c t multiple solutions (or intermediate 
solutions) exist. 
(3) In still other cases a long sequence of outputs 
may 
not lend itself t o be specified in a specific 
order. 
In these cases, the outputs from the component 
versions cannot be readily compared. 
(4) 
In m e situations the sequence of outputs from 
a version is context-dependent. 
Any error that pushes 
the rest of output o f f its proper 
position makes the 
subsequent comparison of r e s u l t s meaningless. 
(5) 
I n the event 
that an 
allowable range of 
discrepancy cannot be easily determined, the problem of 
inexact voting is d i f f i c u l t t o handle. 
Acceptable 
r e s u l t s are d i f f i c u l t to reach i n t h i s case. 
Although the above conclusions have a significant 
nunber of negative points, it should be noted that only 
a very small portion of 
the field of 
N-version 
programing 
has been 
touched. 
Some negative results 
might be due t o inexperience of programmers, inadequate 
selection 
of 
problems, 
or 
improper 
control of 
environment for conducting these studies. 
Furthermore, 
there are several variations of N-version programing. 
This approach might be more effective when it is 
applied to the specification or design of a program 
1171. 
It is also possible t h a t N-version 
programming 
can 
aid progran 
testing more effectively than it can 
perform run-time software defect masking. 
Therefore, 
it is believed 
that a t the present 
stage of the 
investigation 
N-version 
programing 
remains 
an 
interesting 
and 
potentially effective approach t o 
software fault-tolerance. 
7. 
Acknowledgment 
This research was supported by 
the U.S. 
National 
Science Fomdation, 
Grant 
No. MCS 72-03633 A@. 
The 
authors wish 
to 
acknowledge 
the 
generous 
and 
enthusiastic advice and cooperation received from Prof. 
Daniel 
M. 
Berry and 
the proaramscontributed by the 
students of h i s Software Engineering 
classes i n 1976 
and 
i n 1977. 
Valuable advice and criticism was 
received fran Professors 
J.A. 
Goguen, 
J r . 
and 
D.F. 
Martin of UCLA, and fran tw referees o f t h i s paper. 
8. 
References 
[ 13 
A. 
Avizienis, 
"Fault-Tolerance 
and 
Fault- 
Intolerance: 
Complementary 
Approaches 
t o Reliable 
Computing," Proc. 
1975 I n t . Conf. 
Reliable Software, 
458-454. 
[21 
B. Randell, 
"System 
Structure 
for 
Software 
Fault-Tolerance," 
IEEE Trans. 
Software Fngr., 
Vol. 
SE-1, June 1975, 220-232. 
[21 
B. Randell, 
"System 
Structure 
for 
Software 
Fault-Tolerance," 
IEEE Trans. 
Software Fngr., 
Vol. 
SE-1, June 1975, 220-232. 
[31 
H. Hecht, "Fault-Tolerant Software for Real-Time 
Applications," 
ACM 
Computing Surveys, Vol. 
8, Dec. 
1976, 391-407. 
[41 
A. 
Avizienis, 
"Fault-Tolerant 
Computing: 
Progress, 
Problems 
and 
Prospects 
Information 
Processing 77 (Proc. IFIP Congress 19771, 405-420. 
[51 
X.R. 
Elmendorf, 
"Fault-Tolerant 
Programming ," 
Proc. 
1972 I n t . 
Symp. Fault-Tolerant Computing, June 
1972, 79-83. 
161 
H. Kopetz, 
"Software 
Redundancy 
i n Real 
Time 
Systems," Proc. IFIP Congress 1974, 182-186. 
[71 
E. 
Girard 
and 
J.C. 
Rault, 
"A 
Programming 
Technnique 
for Software Reliability," Proc. 1973 IEEE 
Symp. on Computer Software Reliability, 44-50. 
[81 
M.A. 
Fischler, et. a l . , 
"Distinct 
Software: 
An 
Approach to Reliable Computing,', Proc. 2nd USA-Japan 
Computer Conference, Tokyo, Japan, 1975, 1-7. 
191 
A. Avizienis and L. Chen, "Ckl the Implementation 
of N-version 
Programming for Software Fault-Tolerance 
b r i n g Execution," Proceedings of COMPSAC 
77, 
( F i r s t 
IEEE-CS International Computer Software and Application 
Conference), Nov. 1977, 149-155 
118 

[lo] L. Chen, "Improving Software 
Reliability by 
N- 
version 
UCLA 
Computer Science Dept. 
.Technical 
Remrt, 
University of 
California 
Los 
Angeles, 1978. 
[111 B.H. 
Liskov and 
V. 
Berzins. 
"AI 
ADDraiSal of 
Progran specific a t ions, 1, 
Computation st r &ut- es Craup 
Memo 141-1, MIT Laboratory for Ccinputer Science, April 
1977. 
1123 W.C. 
Bouricius, et. 
a l . , "Reliability 
Modeling 
Techniques for Self-Repairing Computer Systems,1t m. 
ACM 1969 Annual Conf.,295-309. 
C131 
J.H. Wensley e t . al., "The Design, Analysis, 
and 
Verification of the S I F T Fault-Tolerant System," PE. 
2nd 
I n t . 
Conf. 
Software 
Engineering, 
Oct. 
1976, 
[141 
A.L. 
Ho@cins, Jr., 
and 
T.B. 
Smith 111, "?he 
Architectural Elements of a Svmnetric Fault-Tolerant 
aa-269. 
Multiprocessor," IEEE T r a n s . 
C$nputers, Vol. C-24, May 
19-75 , 43&505. 
[ 151 J.R. Sklaroff, "Redundancy Management Technique 
for Space Shuttle Canputers,lt IBM J. of Res. and Dev., 
Ti61 R.B. 
Broen. "New Voters for Redundant 
Systems," 
Vol. 20, Jan. 1976, 20-25. 
- - - 
Trans. 
M E : Journal of Dynanic Systems, Measurement, 
and Control, March 1975. 41-45. 
[l7] A.B. 
Long, 
C.V. 
Rammoorthy, 
e t . 
a l . , 
"A 
Methodology for kvelopnent and Validation of Critical 
Software for Nuclear Power Plants," Proc. 
CCMPSAC 
'77 
(IEEE-CS Int. Conputer Software & Applications Conf.), 
620-626. 
Authors 
Liminz Chen was born i n Taiwan. 
He received 
the ILS. 
('69) i n Psychology fran the National Taiwan University 
and the Y.A. 
and X.S. 
degrees i n Psychology 
and 
in 
Compter 
Science 
fran UCLA. 
Since 1974 he has been a 
Postgraduate Research 
Engineer 
associated 
with the 
Fault-Tolerant 
Computing project a t UCLA, where he is 
canpleting t h e Ph.C. 
dissertation i n Computer 
Science. 
Since Yay 
1977, he is associated with the Xerox Co. 
working on software developnent methodology, diagnostic 
programing, and huna? engineering. 
A 1 i r d a s Avizienis was born i n Kaunas, 
Lithuania. 
He 
re:eived 
the 
E.S. 
('54), 
M.S. ('55) and Ph.D. 
('60) 
degrees i n Electrical Engineering from 
t h e University 
of Illinois. 
In 1960 ne initiated research on fault- 
tolerant canputing 
and 
l a t e r directed 
the 
JPL-STAR 
computer project 
a t the Jet Propulsion Laboratory, 
where he is now an Academic Hember of Technical 
Staff. 
Since 
1962 ne has been a faculty member a t UCLA, where 
he is now 
a 
Professor i n the 
Computer 
Science 
Department. 
He is : Fellow of the IEEE and the author 
of over 50 publications on 
computer arithmetic and 
fault tolerance. 
He 
was 
the f i r s t chairman of the 
IEEE-CS Technical Comnittee on Faul t-Tolerant Computing 
and the Chairman of FTCS-1 i n 1971. 
Appendix 
Assume that a +version 
software 
u n i t has heen 
identified 
t o implement 
a function which can be 
activated repeatedly t o convert an array of 
10 ASCII 
coded 
d i g i t s 
into 
a 
binary 
nunber. 
Possible 
implementation of 3 vcrsions of a program 
for 
t h i s 
function are shown 
i n Figures 5, 
6 , and 7. 
It. is 
evident 
that 
these 
implementations 
are 
simple 
derivations of that i n Figure 2. 
CONVERSION1 : PROCEDURE OPTIONS (TASK) ; 
DCL NUMBERl 
BINARY 
FIXED(31) EXTERNAL; 
DCL (SERVICE1 , COMPLETEl) EVENT 
EXTERNAL; 
DCL (DISAGREE1 , GOODBYE) 
B I T ( 1 ) 
EXTERNAL; 
DCL D I G I T S ( 1 0 ) 
BINARY 
F I X E D ( 6 ) 
EXTERNAL; 
DCL F I N I S 
B I T ( 1 ) 
I N I T ( ' O ' B ) ; 
. . 
DO WHILE (>FINIS); 
WAIT (SERVICE1 ) ; 
COMPLETION (SERVICE1) = ' O ' B ; 
NUMBERl = 0: 
I F lGOODBYE.& 1DISAGREE1 
THEN DO I = 1 TO 10; 
NUMBERl = NUMBER1 *1 D+ 
D I G I TS ( I - 60 ; 
END; 
ELSE F I N I S = ' 1 ' B ; 
COMPLETION (COMPLETE1 ) = '1 ' B ; 
END; 
END CONVERSION7 ; 
Figure 5 
CONVERSION2: 
PROCEDURE OPTIONS (TASK) ; 
OCL NUMBER 2 
BINARY 
F I X E D ( 3 1 ) EXTERNAL; 
OCL (DISAGREEZ. 
GOODBYE) 
B I T ( 1 ) 
EXTERNAL; 
DCL (SERVICE2, .COMPLETE2) EVENT 
DCL ( D I G I T S ( 1 0 ) EINARY 
F I X E D ( 6 ) 
EXTERNAL; 
OCL F I N I S 
B I T ( 1 ) 
I N I T ( ' O ' B ) ; 
DO WHILE ( 7 F I N I S ) ; 
EXTERNAL ; 
WAIT (SERVICE2) ; 
COMPLETION (SERVICEL) = 'O'B; 
NUMBER2 = 0; 
I F TGOODBYE & lDISAGREE2 
THEN DO I = 1 TO 10; 
NUMBER2 = NUMBER2 + 
END; 
( D I G I T S (I 
)-60)*1 O**( 1 0 - 1 ) ; 
ELSE F I N I S = ' 1 ' B ; 
COMPLEION (COMPLETE2) = '1 'B; 
END; 
END CONVERSIONZ; 
Figure 6 
CONVERSIONJ: 
PROCEDURE OPTIONS (MAIN) ; 
DCL NUMBER3 
BINARY 
FIXED(31) EXTERNAL; 
DCL (DISAGREE3. 
GOODBYE) 
B I T ( 1 ) 
EXTERNAL; 
DCL C SERVICE^,   COMPLETE^) EVENT 
EXTERNAL; 
DCL D I G I T S ( 1 0 ) 
BINARY 
FIXED(6) 
EXTERNAL; 
OCL F I N I S 
B I T ( 1 ) 
I N I T ( ' 0 ' B ) ; 
DO WHILE (,FINIS); 
WAIT (SERVICE3); 
COMPLETION (SERVICE3) :: 'O'B; 
NUMBER3 = 0; 
I F TGOODBYE & l D I S A G R E E 3 
THEN DO I = 1 TO 10; 
NUMBER3 = NUMBER3*1 O+ 
END ; 
MOD(DIGXTS(I), 
60) ; 
ELSE F I N I S = ' 1 ' 6 ; 
COMPLETION(COMPLETE3) 
2: 
'1 'B; 
END; 
END CONVERSIONS; 
Figure 7 
119 

