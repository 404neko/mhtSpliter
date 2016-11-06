@echo off
echo 请在MaxBlock.txt 中指定没个文件要包含的QQ 信息条数
pause
copy /y "%1" File.mht
Main.exe File.mht