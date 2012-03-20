<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>

  <xsl:attribute-set name="headline-style">
    <xsl:attribute name="font-size">14px</xsl:attribute>
    <xsl:attribute name="margin-top">15px</xsl:attribute>
    <xsl:attribute name="margin-bottom">5px</xsl:attribute>    
  </xsl:attribute-set>
  
  <xsl:attribute-set name="paragraph-style">
    <xsl:attribute name="font-size">10px</xsl:attribute>
    <xsl:attribute name="margin-top">10px</xsl:attribute>
  </xsl:attribute-set>
  
  <xsl:template match="html">
    <fo:block-container>
      <xsl:apply-templates select="body"/>
    </fo:block-container>
  </xsl:template>

  <xsl:template match="body">
    <xsl:apply-templates/>
  </xsl:template>
  
  <xsl:template match="p">
      <fo:block xsl:use-attribute-sets="paragraph-style">
          <xsl:apply-templates />
      </fo:block>
  </xsl:template>
  
  <!-- HEADLINES -->
  <xsl:template match="h1|h2|h3|h4|h5|h6">
    <fo:block xsl:use-attribute-sets="headline-style">
      <xsl:apply-templates />
    </fo:block>
  </xsl:template>  

  <!-- UNORDERED LIST -->
  <xsl:template match="ul">
    <fo:list-block start-indent="-3mm" xsl:use-attribute-sets="paragraph-style">
      <xsl:for-each select="child::*">
        <fo:list-item>
          <fo:list-item-label end-indent="label-end()">
            <fo:block font-weight="bold">
              <fo:character character="&#x2022;"/>
            </fo:block>
          </fo:list-item-label>
          <fo:list-item-body start-indent="0">
            <fo:block>
              <xsl:apply-templates />
            </fo:block>
          </fo:list-item-body>
        </fo:list-item>
      </xsl:for-each>
    </fo:list-block>
  </xsl:template>
  
  <!-- ORDERED LIST -->
  <xsl:template match="ul">
    <fo:list-block start-indent="-3mm" xsl:use-attribute-sets="paragraph-style">
      <xsl:for-each select="child::*">
        <fo:list-item>
          <fo:list-item-label end-indent="label-end()">
            <fo:block font-weight="bold">
              <fo:character character="&#x2022;"/>
            </fo:block>
          </fo:list-item-label>
          <fo:list-item-body start-indent="0">
            <fo:block>
              <xsl:apply-templates />
            </fo:block>
          </fo:list-item-body>
        </fo:list-item>
      </xsl:for-each>
    </fo:list-block>
  </xsl:template>
  

</xsl:stylesheet>