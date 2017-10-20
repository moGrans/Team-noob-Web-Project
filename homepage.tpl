<html>
    <style>
    	/*style of search box*/
        input[type=text] {
        width: 40%;
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
			width: 8%;
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
			margin-top: 15%;
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
			<a href = '/logout' title = "Log out">	
				<img src = {{ss['picture']}} width = 50 class = "profilepic">
			</a>
			%end
		</div>

  		<!-- search bar and logo -->
  		<div class = "searchbar" align = center>
	  		<!-- logo image -->
	  		<img src = "/static/image/test_logo.png" width = 600>
	  		<br>
	  		<!-- input filed for search -->
		    <form method="get" action="/">
		        <input type='text' name='keywords'>
		    	<input type='submit' value='Search'>
		    </form>
		</div>

		<!-- wave design -->
		<div class = "bottomart" align = center>
			<img src = "/static/image/wave_1.png" width = 100%>
		</div>




  	</body>
</html>
