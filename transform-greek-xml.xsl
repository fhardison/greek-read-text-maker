<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.01" indent="yes"/>
<xsl:output doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
<xsl:output doctype-public="-//W3C//DTD HTML 4.01//EN"/>

	<xsl:template match="/">
		<xsl:apply-templates />
	</xsl:template>
	
	<xsl:template match="text">
		<div class="text">
			<xsl:apply-templates />
		</div>
	</xsl:template>
	
	<xsl:template match="p">
		<p>
			<xsl:apply-templates />
		</p>
	</xsl:template>

	<xsl:template match="w">
		<a class="footnote">
			<xsl:value-of select="form" />
			<span>
				<xsl:apply-templates />
			</span>
		</a>
	</xsl:template>
	<xsl:template match="info">
		
			<xsl:apply-templates  />
		
	</xsl:template>
	<xsl:template match="l">
		<xsl:value-of select="text()" /><br />
	</xsl:template> 
</xsl:stylesheet>
