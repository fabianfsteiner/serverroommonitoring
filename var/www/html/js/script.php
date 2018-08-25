<script>
(function($)
	{
    $(document).ready(function()
    {
        $.ajaxSetup(
        {
            cache: false,
            beforeSend: function() {
                $('#content').hide();
                $('#loading').show();
            },
            complete: function() {
                $('#loading').hide();
                $('#content').show();
            },
            success: function() {
                $('#loading').hide();
                $('#content').show();
            }
        });
        var container = $("#div_summary");
		var cs076 = $("#Ser078");
		var maximum = cs076.outerWidth() / 2 || 300;
		 var data = [];

    function getRandomData() {

        if (data.length) {
            data = data.slice(1);
        }

        while (data.length < maximum) {
            var count = 1;
            var y = 0;
			while ($("#s"+count).length) {
				y += parseFloat($("#s"+count).attr("data-temp"));
				count++;
			}
			y = y / (count - 1);
            data.push(y);
        }

        // zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data.length; ++i) {
            res.push([i, data[i]])
        }

        return res;
    }

    //

    series = [{
        data: getRandomData(),
        lines: {
            fill: true
        }
    }];

    //

    var plot = $.plot(cs076, series, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 15,
            max: 40
        },
        legend: {
            show: true
        }
			});
        var refreshId = setInterval(function()
        {	
			<?php
			try {
			$opt  = array
				(
				  PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
				);
				$dbh = new PDO('mysql:host=localhost;dbname=serverraum_temperaturueberwachung', 'webuser', 'La4R2uyME78hAfn9I1pH', $opt);
				$query = 'select ip, name from messsystem;';
				$stmt = $dbh->prepare($query);
				$stmt->execute();
				while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
					$string = str_replace(' ', '', $row["name"]);
					echo '
					var '.$string.' = $("#'.$string.'");
					'.$string.'.load("http://'.$row["ip"].'/pages/currentvalues.php");';
				}
				$dbh = null; 
				} catch (PDOException $e) {
				   print "Error!: " . $e->getMessage() . "<br/>";
				   die();
				}?>
			series[0].data = getRandomData();
			plot.setData(series);
			plot.draw();
        }, 5000);
});
})(jQuery);
</script>