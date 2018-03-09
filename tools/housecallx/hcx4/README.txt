README of HouseCallX

This tool is provided to perform xscan on the specified paths.

There are two methods to specify the paths to scan.
For example, if you want to scan "C:\Windows" and "D:\My Documents", you can:
(A) Specify the paths as the command arguments:
HouseCallX C:\Windows "D:\My Doucments"

(B) Provide a config file ScanPaths.conf in the same path of HouseCallX.exe, and its content is as follows:
C:\Windows
D:\My Doucments

If you pass paths as the command argument and the config file also exists,
this tool will scan the paths from the command argument first and then those from the config file.

Environment variables such as %TEMP% are supported.
