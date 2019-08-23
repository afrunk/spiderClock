# 导出文件
'''
 导出要求：
    - 没有价格就不导出
    - 导出时美元符号删掉
    - 库存分几种情况进行数字替换
    - 导出时 批发量小于一个数字才导出
    - 第6点需要确认
    - 价格需要自定义乘多少倍 然后省略到角
    - 自定义水印
    - 分类导出
        - 自定义导出具体的数量
        - 自定义导出的类目
        - 可以添加添加一个宝贝类目

    文件夹放图片 csv文件放置各个属性

<IMG src="https://img.alicdn.com/imgextra/i2/1685786492/TB2Pu_9c7SWBuNjSszdXXbeSpXa_!!1685786492.jpg">
<TABLE borderColor=#000000 cellSpacing=0 cellPadding=3 width=730 align=left border=1>
<TBODY>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Manufacturer Part Number</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>ZXLD1374QEV1</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Manufacturer</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>Diodes Incorporated</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Categories</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>evaluation-boards-led-drivers</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Description</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>EVAL BOARD LED MV INT SWITCH</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Part Status</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>Active</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Series</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>-</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Minimum Quantity</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>1</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Outputs and Type</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>1.5A</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Voltage - Output</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>1, Non-Isolated</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Features</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>-</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Voltage - Input</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>Dimmable</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Supplied Contents</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>8V ~ 48V</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>Utilized IC / Part</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>Board(s)</TD></TR>
<TR>
<TD bgColor=#f8f8f8 vAlign=middle align=right>产品供应商</TD>
<TD bgColor=#f8f8f8 vAlign=middle align=left>美客数码配件</TD></TR>
<TR>
<TD colSpan=2 align=center><IMG src="https://img.alicdn.com/imgextra/i1/1685786492/TB2xY.VcHSYBuNjSspfXXcZCpXa_!!1685786492.jpg"></TD></TR></TBODY></TABLE>

'''