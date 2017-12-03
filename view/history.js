var historyCount = 30; 

function setHistory() {  
    $('#acomp').hide();
    var keyWord = $("#inputtable").val();
      var keyWords = $.cookie('keyWord');  
      if (keyWords) {  
          if(keyWord) {  
              var keys = keyWords.split(",");  
              for (var i = keys.length - 1; i >= 0; i--) {  
                  if (keys[i] == keyWord) {  
                      keys.splice(i, 1);  
                  }  
              }  
              keys.push(keyWord);  
              if (keys.length >= historyCount) {  
                  var count = keys.length - historyCount + 1; 
                  keys.splice(0, count);  
              }  
              $.cookie('keyWord', keys.join(','), {expires: 365, path: '/'});  
          }  
      } else {  
          $.cookie('keyWord', keyWord, {expires: 365, path: '/'});  
      }  
}  

function  delHistory() {  
  $.cookie("keyWord",null,{path:"/",expires: -1});
  $("#acomp").hide();
}  

function  getHistory(){  
    var keyWords = $.cookie('keyWord');  
    if (keyWords) { 
        $("#acomp").show();
        $("#inputtable").on('keyup', function (e) {
            if (e.keyCode == 13) {
                $("#acomp").hide();
            }
        });
        var keys =  keyWords.split(",");  
        var length = keys.length;  
        if (length > 0) {  
            $("#suggs").empty();  
            var htmlString = ''; 
            if (!$("#inputtable").val()){
                for (var i = length - 1; (i >= 0) && (i >= length - 6); i--) {  
                    htmlString += '<li class = "entries his" role="presentation" onclick="clickSuggs(this)">' + keys[i] + "</li>";  
                }  
            } else {
                var i = length - 1;
                var n = 0; 
                while (i >= 0 && n < 3) {
                    if (keys[i].startsWith($("#inputtable").val())) {
                        var thiskey = keys[i].replace($("#inputtable").val(), '<b>'+$("#inputtable").val()+'</b>')
                        htmlString += '<li class = "entries his" role="presentation" onclick="clickSuggs(this)">' + thiskey + "</li>";  
                        n++;
                    }
                    i--;
                }
            }
            htmlString += '<li class = "entries clearhis" role="presentation" onclick="delHistory()">Clear History</li>';
            $("#suggs").html(htmlString);
        };
    } ;
}  

window.autoComp = function() {
    var hasValue = document.getElementById('inputtable').value;
    if (!!hasValue) {
        document.getElementById('acomp').style.display = 'block';
    } else {
        document.getElementById('acomp').style.display = 'none';
    };
};

window.clickSuggs = function(ent) {
    document.getElementById('acomp').style.display = 'none';
    document.getElementById('inputtable').value = ent.innerText;
    $('.sform').submit();
};

window.autoCompOut = function() {
      document.getElementById('acomp').style.display = 'none';
};

window.addEventListener('click', function(e){  
    if (document.getElementById('searchbutton').contains(e.target)) {
        $("#acomp").hide();
        $(".sform").submit();
    } else {
        if (!document.getElementById('inputtable').contains(e.target))
            if (!document.getElementById('acomp').contains(e.target))
                $("#acomp").hide();
    }
  });

$("#inputtable").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $("#acomp").hide();
    }
});