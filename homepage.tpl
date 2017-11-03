<html>
    <style>
    	/*style of search box*/
        input[type=text] {
        width: 650px;
        padding: 15px 20px;
    	margin: 8px 0;
    	display: inline-block;
    	border: 1px solid #ccc;
    	border-radius: 4px;
    	box-sizing: border-box;
    	font-size: 15px;

		}

		/*style of search box when clikced on*/
		input[type=text]:focus {
    		border: 2px solid #a1abba;
    		border-radius: 4px;
    		box-shadow: 10px 10px 30px #a1abba;
		}

		/*style of search box when mouse is on top*/
		input[type=text]:hover {
    		border: 2px solid #4286f4;
    		border-radius: 4px;
    		box-shadow: 10px 10px 30px #a1abba;
		}

		/*style of submit button*/
		input[type=submit] {
			width: 100px;
		    background-color: #4CAF50;
		    color: white;
		    padding: 15px 15px;
		    margin: 8px 0;
		    border: none;
		    border-radius: 4px;
		    cursor: pointer;
		    font-size: 18px;
		    font-weight: bold;
		}

		/*style of submit button when mouse is on top*/
		input[type=submit]:hover {
    		background-color: #45a049;
		}

		.searchbar {
			position: absolute;
			top:300px;
			left:350px;
			/*margin-top: 15%;*/
			/*position: fixed;*/
		}
		
		.bottomart {
			bottom: 0;
			position: absolute;
		}

		.profilepic {
			border-radius: 50%;
			overflow: hidden;
		}

		.recentKW {
			position: absolute;
			top:482px;
			left:350px;
			width:650px;
			background-color: #e5ede2;
			font-size: large;
		}

		tr:nth-child(even){background-color: #d3dbd1}

		th, td {
        text-align: center;
        padding: 5px;
    	}

		table {
			width: 650px;
		}

		#panel {
			width: 100%;
    		padding: 50px 0;
    		text-align: center;
    		background-color: lightblue;
    		margin-top: 20px;
		}

		#logo {
			position: relative;
			left: 50px;
			width: 600;
		}
	</style>



  	<head>
      	<title>Stinky Fish</title>
  	</head>

  	<body>
  		<!-- top bar -->
		<div class = "topbar" align = right>	
			<!-- user have not sign into a google account -->
			%if ss_user is None:
			<a href = '/login' title = "Sign in">
				<!-- display sign in button that will link to sign in page -->
				<img src = "/static/image/sign_in.png" width = 80>
			</a>
			%end
			<!-- user log in to google account -->
			%if ss_user is not None:	
				<img src = {{ss['picture']}} width = 45 class = "profilepic">
				<a href='/logout' title = "sign out">
					<img src = "/static/image/sign_out.png" width = 80>
				</a>
			%end
		</div>

  		<!-- search bar and logo -->
  		<div class = "searchbar">
	  		<!-- logo image -->
	  		<img id = "logo" src = "/static/image/test_logo.png">
	  		<br>
	  		<!-- input filed for search -->
		    <form method="get" action="/">
		        <input type='text' name='keywords'>
		    	<input type='submit' value='Search'>
		    </form>
		</div>

		<!-- 10 recent search keyword for google user-->
		<div class = "recentKW">
		%if ss_user is not None:
			<h3 align="center">Recent 10 Keywords</h2>
			<table align = center>
			% for word in ss[ss_user].recent:
				<tr><td>{{word}}</td></tr>
			%end
			</table>
		%end
		</div>
  	</body>
</html>
