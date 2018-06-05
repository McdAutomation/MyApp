var clock;

var year = 2018;
var mon = 2;
var day = 16;
var hr = 7;
var min = 50;
// Set some date in the past.


function displayClock(){
			$(document).ready(function() {
            var currentDate = new Date();
            var pastDate  = new Date(year, mon, day , hr, min);
			var diff = currentDate.getTime() / 1000 - pastDate.getTime() / 1000;

				// Instantiate a coutdown FlipClock
				clock = $('.clock').FlipClock(diff, {
					clockFace: 'MinuteCounter',
		        	countdown: true,
		        	autoStart: true,
				});
			});
		}
