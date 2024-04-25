
[Rainmeter]
Update=1000

ContextTitle=Edit (un)Plugged Config
ContextAction=["#@#Variables.ini"]

[Variables]
@IncludeVariables=#@#Variables.ini
; set to 1 if detailed logs wanted
Debug=0

[Actions]
Measure=Script
ScriptFile=#@#Actions.lua
Disabled=1

[PluggedInStatus]
Measure=Plugin
Plugin=PowerPlugin
PowerState=ACLine
IfCondition=(#CURRENTSECTION#<=0)
IfTrueAction=[&Actions:deactivate_skins()]
IfFalseAction=[&Actions:activate_skins()]

[PluggedInTextStatus]
Measure=STRING
DynamicVariables=1
String=[PluggedInStatus]
Substitute="0":"On battery","1":"Plugged in"
