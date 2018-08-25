<?php
header('Access-Control-Allow-Origin: *');

// Load the XML source

foreach(glob('../xml/actual*') as $file) {
	$filename = '../xml/'. substr($file,13, -4).'.xml';
	if (file_exists($filename)) {
	$xml = new DOMDocument( "1.0", "ISO-8859-1" );
	$xml->load($filename);

	$xsl = new DOMDocument;
	$xsl->load($file);

	// Configure the transformer
	$proc = new XSLTProcessor;
	$proc->importStyleSheet($xsl); // attach the xsl rules

	echo $proc->transformToXML($xml);
	}

}
?> 