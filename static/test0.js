
<html>
	<head>
		<link rel="stylesheet" href="../compiled/flipclock.css">

		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>

		<script src="../compiled/flipclock.js"></script>	
	</head>
	<body>
		<div class="clock" style="margin:2em;"></div>
		
		<script type="text/javascript">
			var clock;

			$(document).ready(function() {

				// Grab the current date
				var currentDate = new Date();

				// Set some date in the past. In this case, it's always been since Jan 1
				var pastDate  = new Date(currentDate.getFullYear(), 0, 1);

				// Calculate the difference in seconds between the future and current date
				var diff = currentDate.getTime() / 1000 - pastDate.getTime() / 1000;

				// Instantiate a coutdown FlipClock
				clock = $('.clock').FlipClock(diff, {
					clockFace: 'DailyCounter'
				});
			});
		</script>
		
	</body>
</html>