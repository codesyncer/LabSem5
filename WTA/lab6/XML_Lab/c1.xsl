<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
    <html>
    <head>
        <title>Concerts</title>
    </head>
    <body>
    <table width="100%" border="1">
        <THEAD>
                <TR>
                    <TD width="33%"><B>Name</B></TD>
                    <TD width="33%"><B>Genre</B></TD>
                    <TD width="34%"><B>Venue</B></TD>
                </TR>
        </THEAD>
        <TBODY>
                <xsl:for-each select="root/concert_ad">
                    <xsl:if test="genre = 'Pop'">
                    <TR bgcolor="green"> 
                        <TD width="33%"><xsl:value-of select="name" /></TD>   
                        <TD width="33%"><xsl:value-of select="genre" /></TD>
                        <TD width="34%"><xsl:value-of select="place" /></TD>
                    </TR>
                    </xsl:if>
                    <xsl:if test="genre = 'Classical'">
                    <TR bgcolor="yellow"> 
                        <TD width="33%"><xsl:value-of select="name" /></TD>   
                        <TD width="33%"><xsl:value-of select="genre" /></TD>
                        <TD width="34%"><xsl:value-of select="place" /></TD>
                    </TR>
                    </xsl:if>
                    <xsl:if test="genre = 'Instrumental'">
                    <TR bgcolor="blue"> 
                        <TD width="33%"><xsl:value-of select="name" /></TD>   
                        <TD width="33%"><xsl:value-of select="genre" /></TD>
                        <TD width="34%"><xsl:value-of select="place" /></TD>
                    </TR>
                    </xsl:if>
                </xsl:for-each>
        </TBODY>
    </table>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>