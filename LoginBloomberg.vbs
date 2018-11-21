'''
''' This script schedules to log into Bloomberg
''' Apr 2017

Dim oWs, strPass
strPass = ".abcapr17"
set oWs = WScript.CreateObject("WScript.Shell")

If  oWs.AppActivate("1-BLOOMBERG") Then
         oWs.AppActivate "1-BLOOMBERG"
         WScript.Sleep 500
         oWs.SendKeys "{esc}"
         oWs.SendKeys "{esc}"
         oWs.SendKeys "{esc}"
         WScript.Sleep 1000
         oWs.SendKeys "login~"
         WScript.Sleep 3000
         oWS.SendKeys "HXUOBGMS{right}"
         WScript.Sleep 2000
         'Wscript.echo  strPass 
         oWs.SendKeys strPass
         oWs.SendKeys "{ENTER}"
End If

set oWs = Nothing
WScript.Quit