#!/usr/bin/python
# -*- coding: UTF-8 -*- 

def generateDimens():
    str = "<dimen name=\"dp_%d\">%ddp</dimen>"
    sp  = "<dimen name=\"sp_%d\">%dsp</dimen>"
    with open("res/values/dimens.xml","w") as f:
            f.write("<resources xmlns:tools=\"http://schemas.android.com/tools\">")
            f.write("\n")
            f.write("    <!--create dp dimens from 1-100dp-->\n")
            for i in range(1,101):
                f.write('    ')
                f.write(str % (i,i))
                f.write("\n")   
            f.write("    <!--create dp dimens from 105-1080dp-->\n")
            for i in range(1,197):
                f.write('    ')
                f.write(str % (100+i*5,100+i*5))
                f.write("\n")
            f.write("\n\n")
            f.write("    <!--create sp dimens from 5-50sp-->\n")
            for j in range(5,51):
                f.write('    ')
                f.write(sp % (j,j))
                f.write("\n")
            f.write("</resources>")
            f.close


        
             

if __name__ == '__main__':
    generateDimens()
