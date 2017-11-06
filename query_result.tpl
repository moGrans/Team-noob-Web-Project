<html>
  <style>
    img {
      position: relative;
      left: 8px;
      top: 20px;
      margin-right: 8px;
    }

    .sfbgx {
      background-color: #fafafa;
      border-bottom: 1px solid #ebebeb;
      height: 80px;
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      min-width: 1100px;
    }

    input[type=text] {
      position: relative;
      top: 8px;
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
      top: 8px;
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

    div {
      margin: 0;
      padding: 0;
    }

    table {
        position: relative;
        left: 60;
        top: 10;
        border-collapse: collapse;
        width: 70%;
        font-family : "Myriad Web",Verdana,Helvetica,Arial,sans-serif;

    }

    th, td {
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even){background-color: #f2f2f2}

    th {
        background-color: #4CAF50;
        color: white;
    }

    h1 {
      font-family: "Segoe UI",Arial,sans-serif;
      font-weight: 100;
      font-size: 25;
    }

    #search_result_head {
      position: relative;
      left: 60px;
      top: 30px;
    }

    #searchform {
      float = left;
      margin-right: 10px;
    }

    .pagination a {
    color: black;
    float: left;
    padding: 8px 16px;
    text-decoration: none;
    transition: background-color .3s;
    position: relative;
    top:150px;
    }

    .pagination a.active {
        background-color: #4CAF50;
        color: white;
    }

    .pagination a:hover:not(.active) {background-color: #ddd;}
  </style>

  <head>
      <title>Stinky Fish: search result</title>
  </head>
  <body>
    <!-- top right search bar -->
    <div class="sfbgx"></div>
    <h1>
    <div id = "searchform" align = left>
      <table id = "searchhistory">
      <a href = "/" title = "Go to homepage">
        <img src = "/static/image/test_logo.png" width = 160></a>
      <form method="get" action="/">
          <input type='text' name='keywords'>
          <input type='submit' value='Search'>
      </form>

      <!-- google sign in/ sign out -->
      %if ss_user is None:
      <a href = '/login' title = "Sign in" style = "float:right">
        <!-- display sign in button that will link to sign in page -->
        <img src = "/static/image/sign_in.png" width = 80>
      </a>
      %end
      %if ss_user is not None:
        <a href='/logout' title = "sign out">
          <img src = "/static/image/sign_out.png" width = 80 style = "float:right">
        </a>
        <img src = {{ss['picture']}} width = 45 style = "float:right;border-radius: 50%;overflow: hidden;">
      %end
    </h1>

    <!-- RESULT URL -->
    <div class = "result">
      %for (url, doc_id, title, score) in url[5*(page-1):5*page]:
      <a hrf= {{url}}>
        <p> {{title}} </p>
      </a>
      <br>
      %end
    </div>

    <!-- page choice -->
    <div class="pagination" align="center">
      % if page is not 1:
        <a href="/{{ss['query_string']}}&page=1">&laquo;</a>
      % end
      <a class="active" href="#">{{page}}</a>
      % for npage in range(page+1,page+min(5,total_page - page)):
        <a href="/{{ss['query_string']}}&page={{npage}}">{{npage}}</a>
      % end
      % if page is not total_page:
        <a href="/{{ss['query_string']}}&page={{total_page}}">&raquo;</a>
      % end
    </div>


  </body>
</html>
