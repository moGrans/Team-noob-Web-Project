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

		div {
			margin-top: 15%;
			/*position: fixed;*/
		}
	</style>



  	<head>
      	<title>Stinky Fish</title>
  	</head>
  	
  	<body>
  		<div align = center>
	  		<!-- logo image -->
	  		<img src = "/static/test_logo.png" width = 600> 
	  		<br>
	  		<!-- input filed for search -->
		    <form method="get" action="/">
		        <input type='text' name='keywords'>          
		    	<input type='submit' value='Search'>
		    </form>
		</div>
  	</body>
</html>
