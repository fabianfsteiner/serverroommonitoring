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
					echo '<div class="row"><div class="col-lg-12">
							<h1 class="page-header">'.$row["name"].'</h1>
						</div></div>';
					$string = str_replace(' ', '', $row["name"]);
					echo '<div id="'.$string.'">';
					echo '
					<script>
					var lo'.$string.' = $("#'.$string.'");
					lo'.$string.'.load("http://'.$row["ip"].'/pages/currentvalues.php");
					</script>';
					echo '</div>';
				}
				$dbh = null; 
				} catch (PDOException $e) {
				   print "Error!: " . $e->getMessage() . "<br/>";
				   die();
				}
?>