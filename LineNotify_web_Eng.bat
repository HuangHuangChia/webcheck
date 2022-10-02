cd c:\webcheck
c:\webcheck\typc_eng.py
timeout /t 10 >nul
chcp 65001
IF EXIST "c:\webcheck\TYPC_Eng_info.txt" (
c:\LineNotify\LineNotify_general.exe "0xQH1k7AuD1CERF9Hy12XNv8MnTOE8V6MwitbfdJHe9" "c:\webcheck\Typc_Eng_info.txt"
) ELSE (
ECHO "沒執行linenotify"
)
rem c:\LineNotify\LineNotify_general.exe "lj7BBFFqnWuoezANZEd5jD3NJu9dZkJFua3Cn4wIz2q" "c:\webcheck\TYPC_Chn_info.txt"
rem timeout /t 100 >nul