<div class="list-group">
	<?php
		try {
			$opt  = array
			(
			  PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
			);
			$dbh = new PDO('mysql:host=localhost;dbname=messages', 'webuser', 'La4R2uyME78hAfn9I1pH', $opt);
			$query = 'select * from message order by zeit desc limit 10;';
			$stmt = $dbh->prepare($query);
			$stmt->execute();
			while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
				echo '<a href="#" class="list-group-item" data-toggle="popover" title="'.$row["betreff"].'"
				data-placement="left" data-trigger="hover" data-content="'.$row["text"].'">';
				if ($row["typ"] == 1){
					echo '<i class="fa fa-bolt fa-fw"></i>';
				}
				if ($row["typ"] == 2){
					echo '<i class="fa fa-envelope fa-fw"></i>';
				}
				if ($row["typ"] == 3){
					echo '<i class="fa fa-comment fa-fw"></i>';
				}
				echo $row["betreff"].'<span class="pull-right text-muted small"><em>'.$row["zeit"].'</em></span></a>';
			}
			$dbh = null; 
			} catch (PDOException $e) {
			   print "Error!: " . $e->getMessage() . "<br/>";
			   die();
			}
	?>
</div>