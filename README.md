# -Machine-Learning-1081-0316-Project-svm-HW4
<br />
rules base -> ml_play_template.py <br />
level 1 pass rate 100%  <br />
level 2 pass rate 100%  <br />
level 3 pass rate 100%  <br />
level 4 pass rate 95%  <br />
<br />
algorithm:  <br />
while(alive){  <br />
&nbsp;&nbsp;if ball is dowing{  <br />
&nbsp;&nbsp;&nbsp;&nbsp;calculate the next x of ball  <br />
&nbsp;&nbsp;&nbsp;&nbsp;if ball will hit the brick and going down{  <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;calculate the  next x after the ball bounces}  <br />
&nbsp;&nbsp;}else{  <br />
&nbsp;&nbsp;#ball is upping  <br />
&nbsp;&nbsp;&nbsp;&nbsp;if ball will hit the brick and going down{  <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;calculate the  next x after the ball bounces }
 <br />&nbsp;&nbsp;}
  <br />
 &nbsp;&nbsp;move the platform to the next x   <br />
}
<br />
<br />

SVR training data: <br />
&nbsp;&nbsp;Level 1 log file * 1 <br />
&nbsp;&nbsp;Level 3 log file * 1 <br />
&nbsp;&nbsp;Level 4 log file * 4 <br />
&nbsp;&nbsp;total frames -> 14501 <br />
&nbsp;&nbsp;R^2 -> 0.6752995058622785 <br />
