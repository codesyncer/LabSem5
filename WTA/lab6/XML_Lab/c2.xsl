<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
    <html>
    <head>
        <title>Concerts</title>
    </head>
    <body>
    <table width="100%" border="0" cellpadding="5"  cellspacing="5"> 
        <THEAD>
                <TR>
                    <TD><B>Name</B></TD>
                    <TD><B>Place</B></TD>
                    <TD><B>Genre</B></TD>
                    <TD><B>Date</B></TD>
                    <TD><B>Performer</B></TD>
                    <TD><B>Ticket</B></TD>
                    <TD><B>Discount</B></TD>
                    <TD><B>Seller</B></TD>
                </TR>
        </THEAD>
        <TBODY>
                <xsl:for-each select="root/concert_ad">
                    <xsl:sort select="name"/>
                    <xsl:if test="ticket/price &lt; 100 and contains(place/address, 'Mangalore') and contains(datetime/date, '-04-')">
                        <xsl:if test="ticket/discount != 0">
                            <TR bgcolor="green"> 
                                <TD><xsl:value-of select="name" /></TD>   
                                <TD><xsl:value-of select="place" /></TD>
                                <TD><xsl:value-of select="genre" /></TD>
                                <TD><xsl:value-of select="datetime" /></TD>   
                                <TD><xsl:value-of select="performer" /></TD>
                                <TD><xsl:value-of select="ticket/price" /></TD>
                                <TD><xsl:value-of select="ticket/discount" /></TD>
                                <TD><xsl:value-of select="seller" /></TD>
                            </TR>
                            </xsl:if>
                            <xsl:if test="ticket/discount = 0">
                            <TR> 
                                <TD><xsl:value-of select="name" /></TD>   
                                <TD><xsl:value-of select="place" /></TD>
                                <TD><xsl:value-of select="genre" /></TD>
                                <TD><xsl:value-of select="datetime" /></TD>   
                                <TD><xsl:value-of select="performer" /></TD>
                                <TD><xsl:value-of select="ticket/price" /></TD>
                                <TD><xsl:value-of select="ticket/discount" /></TD>
                                <TD><xsl:value-of select="seller" /></TD>
                            </TR>
                            </xsl:if>
                        </xsl:if>
                </xsl:for-each>
        </TBODY>
    </table>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>