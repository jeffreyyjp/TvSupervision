<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">
    <xsl:template match="/">
        <html>
            <head>
                <title>Camera Test Report</title>
                <link rel="stylesheet" type="text/css" href="../style.css"/>
            </head>
            <body>
                <div>
                    <h1>开关机图像对比详细报告</h1>
                    <table>
                        <caption>
                            摄像头名称：
                            <xsl:value-of select="body/Details/@cameraName"/>
                        </caption>
                        <tr>
                            <th>开机轮次</th>
                            <th>拍摄次数</th>
                            <th>时间</th>
                            <th>结果</th>
                            <th>误差值</th>
                            <th>图像</th>
                            <th>标准图</th>
                        </tr>
                        <xsl:for-each select="body/Details/Detail">
                            <tr>
                                <td>
                                    <xsl:value-of
                                            select="@currSupervisionTime"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@snapTime"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@currentTime"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@result"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@diffPercent"/>
                                </td>
                                <td>
                                    <xsl:variable name="curr_img_address">
                                        <xsl:value-of select="@imgSrc"/>
                                    </xsl:variable>
                                    <a href="{$curr_img_address}">
                                        <img src="{$curr_img_address}"
                                             alt="实时图"
                                             width="56"
                                             height="42"/>
                                    </a>
                                </td>
                                <td>
                                    <a href="standard.jpg">
                                        <img src="standard.jpg"
                                             alt="标准图"
                                             width="56"
                                             height="42"/>
                                    </a>
                                </td>
                            </tr>
                        </xsl:for-each>
                    </table>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
