cd c:\Task\webcheck
call c:\Task\webcheck\updateChineseVersion.bat
c:\Task\webcheck\typc_chn.py
timeout /t 10 >nul
chcp 65001
IF EXIST "c:\Task\webcheck\TYPC_Chn_info.txt" (
c:\Task\LineNotify\LineNotify_general.exe "0xQH1k7AuD1CERF9Hy12XNv8MnTOE8V6MwitbfdJHe9" "c:\Task\webcheck\TYPC_Chn_info.txt"
) ELSE (
ECHO "沒執行linenotify"
)
rem c:\LineNotify\LineNotify_general.exe "lj7BBFFqnWuoezANZEd5jD3NJu9dZkJFua3Cn4wIz2q" "c:\webcheck\TYPC_Chn_info.txt"
rem timeout /t 100 >nul
