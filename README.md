# proj3-ajax
Reimplement the RUSA ACP controle time calculator with flask and ajax

## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted.  Controls are points where 
a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must
arrive at the location.  

The algorithm for calculating controle times is described at http://www.rusa.org/octime_alg.html . The description is ambiguous, but the examples help.  Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator at http://www.rusa.org/octime_acp.html .  We can also use that calculator to clarify requirements.  

## AJAX and Flask reimplementation

The current RUSA controle time calculator is a Perl script that takes an HTML form and emits a text page. The reimplementation will fill in times as the input fields are filled.  Each time a distance is filled in, the corresponding open and close times should be filled in.   If no begin time has been provided, use 0:00 as the begin time. 


## Requirements.txt

Flask==0.10.1
Jinja2==2.8
MarkupSafe==0.23
Werkzeug==0.10.4
arrow==0.6.0
itsdangerous==0.24
python-dateutil==2.4.2
six==1.10.0

#Rules

The calculation of a control's opening time is based on the maximum speed. Calculation of a control's closing time is based on the minimum speed.

Calculates times based on input. Initial 0 closes 1 hour after opening.

Control location (km)	Minimum Speed (km/hr)	Maximum Speed (km/hr)
0 - 200	                15	                34
200 - 400		15			32
400 - 600		15			30
600 - 1000		11.428			28
1000 - 1300		13.333			26
