<!DOCTYPE html>
<html lang="de">

	<?php include "header.php";?>
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">Notifications</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            Critical
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
								<?php
									try {
										$opt  = array
										(
										  PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
										);
										$dbh = new PDO('mysql:host=localhost;dbname=messages', 'webuser', 't5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg', $opt);
										$query = 'select * from message where typ=1 order by zeit desc;';
										$stmt = $dbh->prepare($query);
										$stmt->execute();
										while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
											echo '<a href="#" class="list-group-item" data-toggle="popover" title="'.$row["betreff"].'"
											data-placement="right" data-trigger="hover" data-content="'.$row["text"].'">';
											echo '<i class="fa fa-bolt fa-fw"></i>';
											echo $row["betreff"].'
													<span class="pull-right text-muted small"><em>'.$row["zeit"].'</em>
													</span>
												</a>
											';
										}
										$dbh = null; 
										} catch (PDOException $e) {
										   print "Error!: " . $e->getMessage() . "<br/>";
										   die();
										}
								?>
                        </div>
                        <!-- .panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
				<div class="col-lg-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            Non Critical
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
								<?php
									try {
										$opt  = array
										(
										  PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
										);
										$dbh = new PDO('mysql:host=localhost;dbname=messages', 'webuser', 't5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg', $opt);
										$query = 'select * from message where typ!=1 order by zeit desc;';
										$stmt = $dbh->prepare($query);
										$stmt->execute();
										while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
											echo '<a href="#" class="list-group-item" data-toggle="popover" title="'.$row["betreff"].'"
											data-placement="left" data-trigger="hover" data-content="'.$row["text"].'">';
											if ($row["typ"] == 2){
												echo '<i class="fa fa-envelope fa-fw"></i>';
											}
											if ($row["typ"] == 3){
												echo '<i class="fa fa-comment fa-fw"></i>';
											}
											echo $row["betreff"].'
													<span class="pull-right text-muted small"><em>'.$row["zeit"].'</em>
													</span>
												</a>
											';
										}
										$dbh = null; 
										} catch (PDOException $e) {
										   print "Error!: " . $e->getMessage() . "<br/>";
										   die();
										}
								?>
                        </div>
                        <!-- .panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-6 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

    <!-- jQuery -->
    <script src="../vendor/jquery/jquery.min.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="../vendor/bootstrap/js/bootstrap.min.js"></script>

    <!-- Metis Menu Plugin JavaScript -->
    <script src="../vendor/metisMenu/metisMenu.min.js"></script>

    <!-- Custom Theme JavaScript -->
    <script src="../dist/js/sb-admin-2.js"></script>

    <!-- Page-Level Demo Scripts - Notifications - Use for reference -->
    <script>
    // tooltip demo
    $('.tooltip-demo').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body"
    })
    // popover demo
    $("[data-toggle=popover]")
        .popover()
    </script>

</body>

</html>
