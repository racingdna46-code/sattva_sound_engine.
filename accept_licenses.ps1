$env:JAVA_HOME = 'C:\Users\Lenovo\AppData\Local\BeeWare\briefcase\Cache\tools\java17'
1..30 | ForEach-Object { "y" } | & 'C:\Users\Lenovo\AppData\Local\BeeWare\briefcase\Cache\tools\android_sdk\cmdline-tools\19.0\bin\sdkmanager.bat' --licenses
