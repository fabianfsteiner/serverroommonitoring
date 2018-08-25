<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8"/>

	<xsl:template match="/">
		<xsl:apply-templates select = "//sensor">
			<xsl:sort select="@name" order = "ascending"/>
		</xsl:apply-templates>
	</xsl:template>


	<xsl:template match="//sensor">
		<div class="col-lg-3 col-md-6">
		<xsl:choose>
			<xsl:when test="smoke &lt;= 10">
				<div class="panel panel-green">
					<div class="panel-heading">
						<div class="row">
							<div class="col-xs-12 text-right">
								<div class="huge"><xsl:value-of select="@name" /></div>
								<xsl:element name="div">
									<xsl:attribute name="id">r<xsl:value-of select="id"/></xsl:attribute>
									<xsl:attribute name="data-smoke"><xsl:value-of select="smoke"/></xsl:attribute>
									<xsl:value-of select="smoke"/>
								</xsl:element>
							</div>
						</div>
					</div>
					<div class="panel-footer">
						<span class="pull-left">Date: </span>
						<span class="pull-right"><xsl:value-of select="zeit" /></span>
						<div class="clearfix"></div>
					</div>
				</div>
			</xsl:when>
			<xsl:otherwise>
				<div class="panel panel-red">
					<div class="panel-heading">
						<div class="row">
							<div class="col-xs-12 text-right">
								<div class="huge"><xsl:value-of select="@name" /></div>
								<xsl:element name="div">
									<xsl:attribute name="id">r<xsl:value-of select="id"/></xsl:attribute>
									<xsl:attribute name="data-smoke"><xsl:value-of select="smoke"/></xsl:attribute>
									<xsl:value-of select="smoke"/> 
								</xsl:element>
							</div>
						</div>
					</div>
					<div class="panel-footer">
						<span class="pull-left">Date: </span>
						<span class="pull-right"><xsl:value-of select="zeit" /></span>
						<div class="clearfix"></div>
					</div>
				</div>
			</xsl:otherwise>
		</xsl:choose>
		</div>
	</xsl:template>
</xsl:stylesheet>