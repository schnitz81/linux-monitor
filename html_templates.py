INDEX_HEAD = """
<!DOCTYPE html>
<html lang="en">
  <head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
	<title>linux-monitor</title>
	<link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
	  <center><img src="linuxmonitor-logo.jpg">
	  <br><br><br><br>
	  <table width="500">
"""

INDEX_CLIENT = """
<tr><td><a href="{}.html">{}</a></td><td>{}</td><td><img width="25" height="25" style="position:relative; top:2px;" src="led-{}.svg"></td></tr>
"""

INDEX_TAIL = """
	  </table>
	  </center>
  </body>
</html>
"""

CLIENT_HEAD = """
<!DOCTYPE html>
<html lang="en">
  <head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
	<title>linux-monitor</title>
	<link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
	<a href="index.html"><<<</a><br>
	<script type="text/javascript" src="enlarge.js"></script>
	<center><h2>{}</h2>
"""

CLIENT_BUTTON = """
    <button id="{}_button" onclick="hideshow_{}()"><img style="max-width:80px; max-height:80px;" src="{}.png"><h2>{}</h2></button>
"""

DATA_HEAD = """
			<div id="togglediv_{}" style="display:none;">
			<div class="flex-container">
"""

DATA_RECORD = """                    <div class="thumb"><img width="228" height="175" src="{}-{}-{}.png"  onclick="showImage('{}-{}-{}.png');"></div>"""

DATA_RECORD_DISK_NETWORK = """                    <div class="thumb"><img width="228" height="175" src="{}-{}-{}-{}.png"  onclick="showImage('{}-{}-{}-{}.png');"></div>"""

DATA_TAIL = """
				<br></div>
			</div>
			<script>
                function hideshow_{}() {{
                  var alltoggledivs = document.querySelectorAll("[id^='togglediv']");
                  var alldevicebuttons = document.querySelectorAll("[id$='_button']");
				  for (let z of alltoggledivs) {{ z.style.display = "none"; }}
                  var x = document.getElementById("togglediv_{}");
                  var b = document.getElementById("{}_button")
                  if (x.style.display === "none") {{
                    x.style.display = "block";
                    for (let a of alldevicebuttons) {{ a.style.border = "2px outset buttonborder"; }}
                    b.style.border = "4px solid #4CAF50";
                  }} else {{
                    x.style.display = "none";
                  }}
                }}
			</script>
"""

CLIENT_TAIL = """
      <div class="largeImgPanel"><img style="width:100%; max-width:1300px; max-height:1000px; display:block;" id="largeImg"></div>
    </center>
  </body>
</html>
"""
