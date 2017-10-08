<html>
  <style>
    img {
      position: relative;
      left: 8px;
      top: 12px;
      margin-right: 8px;
    }
    input[type=text] {
      position: relative;

      width: 40%;
      padding: 8px 8px;
      margin-left: 6px;
      margin-right: 6px;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      font-size: 15px;

    }

    /*style of search box when clikced on*/
    input[type=text]:focus {
        border: 1px solid #a1abba;
        border-radius: 3px;
        box-shadow: 4px 4px 12px #a1abba;
    }

    /*style of search box when hover*/
    input[type=text]:hover {
        border: 2px solid #4286f4;
        border-radius: 4px;
        box-shadow: 4px 4px 8px #a1abba;
    }

    /*style of submit button*/
    input[type=submit] {
      position: relative;

      width: 8%;
        background-color: #4CAF50;
        color: white;
        padding: 8px 8px;
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


  </style>

  <head>
      <title>Stinky Fish: search result</title>
  </head>
  <body>
    <!-- display previous searched string -->
    <h1>
    <div id = "searchform" align = left>
      <table>
      <a href = "http://127.0.0.1:8080" title = "Go to homepage">
        <img src = "/static/test_logo.png" width = 160></a>
      <form method="get" action="/">
          <input type='text' name='search_string'>
        <input type='submit' value='Search'>
      </form>
    </h1>
    </div>

    <p> Searched or "{{search_string}}" </P>
    <!-- display keywords frequency table -->
    <table id = keyword_freq_table>
    <tr><th> Keyword </th>
    	<th> Frequency </th></tr>

    %for word in top_20_list:
    	<tr><th>{{word}}</th>
    		<th>{{keyword_dict[word]}}</th></tr>
    %end

  </body>
</html>
