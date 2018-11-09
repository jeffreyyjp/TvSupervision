<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">
    <xsl:template match="/">
        <html>
            <head>
                <title>Summary Test Report</title>
                <link rel="stylesheet" type="text/css" href="style.css"/>
            </head>
            <body>
                <div>
                    <h1>开关机图像对比测试报告</h1>
                    <h2>研发测试部--自动化测试室</h2>
                    <table>
                        <caption>
                            时间：
                            <xsl:value-of select="body/Details/@time"/>
                        </caption>
                        <tr>
                            <th>摄像头名称</th>
                            <th>通过次数</th>
                            <th>失败次数</th>
                            <th>总次数</th>
                            <th>详情</th>
                        </tr>
                        <xsl:for-each select="body/Details/Detail">
                            <tr>
                                <td>
                                    <xsl:value-of select="@cameraName"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@passTimes"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@failTimes"/>
                                </td>
                                <td>
                                    <xsl:value-of select="@totalTimes"/>
                                </td>
                                <td>
                                    <xsl:variable name="camera_report">
                                        <xsl:value-of select="@fileSrc"/>
                                    </xsl:variable>
                                    <a href="{$camera_report}" target="_blank">
                                        <xsl:value-of
                                                select="@fileSrc"/>
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
