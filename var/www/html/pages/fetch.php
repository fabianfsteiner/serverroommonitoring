<?php
	include "connect.php";
	$d1 = array();
	$d2 = array();
	$stmt = $dbh->prepare("SELECT COUNT(*) FROM sensor");
    $stmt->execute();
    $count = $stmt->fetchColumn();
    $stmt->closeCursor();
	$query = 'select * from web limit '.$count;
	$stmt = $dbh->prepare($query);
	$stmt->execute();
    while ($result = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$feucht_arr[intval($result["sensorID"])] = doubleval(result["feucht"]);
		$temp_arr[intval($result["sensorID"])] = doubleval(result["temp"]);
		if(count($temp_arr) == $count){
			$temp = 0.0;
			$feucht = 0.0;
			foreach ($temp_arr as $key=>$value) {
				$temp = $temp+$value;
			}
			foreach ($feucht_arr as $key=>$value) {
				$feucht = $feucht+ $value;
			}
			array_push($d1, array($result['zeit'], $feucht / count($feucht_arr)));
			array_push($d2, array($result['zeit'], $temp / count($temp_arr)));
		}
	}

	$allreferrals = array($d1, $d2);
	echo json_encode(($allreferrals), JSON_NUMERIC_CHECK);

?>