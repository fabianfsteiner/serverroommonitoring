<?php
try {
   include "connect.php";
   $stmt = $dbh->prepare("select count(*) from sensor;");
    $stmt->execute();
    $count = $stmt->fetchColumn();
    $stmt->closeCursor();
	$query = 'select * from web limit '.$count;
	$stmt = $dbh->prepare($query);
	$stmt->execute();
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
			$color = 'panel-primary';
			if(doubleval($row['temp']) > 22.0){
				$color = 'panel-green';
			}
			if(doubleval($row['temp']) > 26.0){
				$color = 'panel-yellow';
			}
			if(doubleval($row['temp']) > 30.0){
				$color = 'panel-red';
			}
			$ausgaben[intval($row['sensorID'])] = '<div class="col-lg-3 col-md-6">
                    <div class="panel '.$color.'">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-12 text-right">
									<div class="huge">'.$row['sensorName'].'</div>
                                    <div id = "s'.(intval($row["sensorID"]) -1).'" data-temp="'.$row["temp"].'">'.$row['temp'].' °C / '.$row['feucht'].' %</div>
                                </div>
                            </div>
                        </div>
                        <div class="panel-footer">
                            <span class="pull-left">Date: </span>
                            <span class="pull-right">'.$row['zeit'].'</span>
							<div class="clearfix"></div>
                        </div>
                    </div>
                </div>';
   }
	ksort($ausgaben);
	foreach ($ausgaben as $key=>$value) {
		print $value;
	}
   $dbh = null;
} catch (PDOException $e) {
   print "Error!: " . $e->getMessage() . "<br/>";
   die();
}
?>