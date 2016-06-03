<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>中草药问答系统</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.12.0.min.js"></script>
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![enif]-->
    <style>
        body{
            color: #fff;
            background-color: #333;
        }
        div{
            margin-bottom: 20px;
        }
        .btn{
            position: absolute;
            bottom 10px;
            right: 15px;
        }
    </style>

    <script>
        function ask()
        {
            if (!document.getElementById("in1").value){
                alert('请输入问题！');
                return ;
            }
            $.ajax({
                type:'GET',
                url:"/answer/" + document.getElementById("in1").value,
                success: function(data){
                    $('#in2').val(data['answer']);
                },
                error: function(exception){
                    alert('Exception:'+exception);
                }
            });
        }
        $(document).keypress(function(e){
            if (e.which == 13){
                $("#save_post").click();
        }
        });
    </script>

  </head>

  <body>
    <div class="row col-md-6 col-md-offset-3">
        <h1 class="cover-heading">中草药问答系统</h1>
    </div>
    <div class="row col-md-6 col-md-offset-3">
        <form role="form">
          <div class="form-group">
            <label for="inputdefault">问题</label>
                <input class="form-control" id="in1" type="text">
            </div>
        </form>
        <button class="btn btn-primary" type="button" onclick="ask()">查询</button>
    </div>

    <div class="row col-md-6 col-md-offset-3">
        <form role="form">
          <div class="form-group">
            <label for="inputdefault">答案</label>
            <textarea class="form-control" id="in2" type="text" rows="20"></textarea>
          </div>
        </form>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>

  </body>
</html>
