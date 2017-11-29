<html>
  <style>
    img {
      position: relative;
      left: 0px;
      top: 20px;
      margin-right: 0px;
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
      max-height: 80px;
    }

    input[type=text] {
      position: relative;
      top: 8px;
      min-width: 400px;
      /* width: 40%; */
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
        border-radius: 3px;
        border: 1px solid #ccc;
        box-shadow: 2px 2px 3px #a1abba;
    }

    /*style of search box when hover*/
    input[type=text]:hover {
        border-radius: 4px;
        border: 1px solid #ccc;
        box-shadow: 2px 2px 4px #a1abba;
    }

    /*style of submit button*/
    input[type=submit] {
      position: relative;
      top: 8px;
      min-width: 28px;
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
      position: relative;
      max-width: 600px;
      left: 0px;
      margin-left: 4px;
      margin-right: 4px;
    }
    
    h3 {
      display: block;
      font-size: 1.17em;
      -webkit-margin-before: 1em;
      -webkit-margin-after: 1em;
      -webkit-margin-start: 0px;
      -webkit-margin-end: 0px;
      font-weight: normal;
    }

    .mw {
      position: relative;
      /* max-width: 1197px; */
      top: 20px;
      margin-top: 80px;
      padding: 0 165px;
    }

    .rcnt {
      border: 0;
      margin: 0;
    }

    .g {
      margin-top: 0;
      margin-bottom: 26px;
      font-size: small;
      font-family: arial,sans-serif;
      line-height: 1.2;
      text-align: left;
    }

    .result {
      font-size: medium;
    }
    
    .r {
      margin: 0;
    }

    .r a {
      text-decoration: none;
    }
    
    .r a:hover {
      text-decoration: underline;
    }

    .r a:link {
      cursor: pointer;
      color: #1a0dab;
    }

    .r a:visited {
      color:#609;
    }

    cite {
      color: #006621;
      font-style: normal;
      font-size: 14px;
    }

    .spell_co {
      margin: .33em 0 17px;
      font-size: 18px;
    }

    .spell {
      color: #dd4b39;
      font-family: arial,sans-serif;
    }
    
    .spell a {
      text-decoration: none;
    }

    .spell a:hover {
      text-decoration: underline;
    }

    .spell a:link {
      cursor: pointer;
      color: #1a0dab;
    }

    .spell a:visited {
      color:#609;
    }

    .logo {
      position: absolute;
      float: left;
      left: 0;
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
    
    .signin {
      position:relative;
      left: 800px;
      top: 0;
    }

    .signin-button {
      min-width: 28px;
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

    .signin-button:hover {
        background-color: #45a049;
    }
    
    .searchbox {
      position: relative;
      left: 165px;
    }
  
  </style>

  <head>
      <title>Stinky Fish: search result</title>
  </head>
  <body>
    <!-- top right search bar -->
    <div class="sfbgx">
      <div id = "searchform">
        <!-- <table id = "searchhistory"> -->
        <div class = "logo">
          <a href = "/" title = "Go to homepage">
            <img src = "/static/image/test_logo.png" width = 160></a>
        </div>
        <div class = "searchbox">
          <form method="get" action="/">
              <input type='text' name='keywords'>
              <input type='submit' value='Search'>
          </form>
      </div>
    </div>
  </div>
    <!-- RESULT URL -->
    
    <div class = "mw">
      <!-- spell correction -->
      % if correction is True:
      <div class = "spell_co">
        <span class = "spell">
          Did you mean: <a href="/{{ss['corrected_string']}}">{{correctedKeywords}} </a>
        </span>
      </div>
      % end

      % if url is None:
      <div>
        <p> No result found. </p>
      </div>
      % end
      % if url is not None:
      <div class = "rcnt">
        %for (url, title) in url[5*(page-1):5*page]:
        <div class = "g">
          <div class = "result">
                <h3 class = "r">
                  <a href= {{url}}>
                     {{title}}
                  </a>
                </h3>
          </div>
          <div style="white-space:nowrap">
            <cite  class="ref">{{url}}</cite>
          </div>
        </div>
        %end
      </div>
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

  %end
  </body>
</html>
