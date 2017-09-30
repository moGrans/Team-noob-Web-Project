<html>
  <head>
      <title>Stinky Fish: search result</title>
  </head>
  <body>
    <!-- display previous searched string -->

    <p> Searched for "{{search_string}}" </P>

    <!-- display keywords frequency table -->
    <table id = keyword_freq_table>
    <tr><th> Keyword </th>
    	<th> Frequency </th></tr>

    %for word, count in top_20_dict.items():
    	<tr><th>{{word}}</th>
    		<th>{{count}}</th></tr>
    %end

  </body>
</html>