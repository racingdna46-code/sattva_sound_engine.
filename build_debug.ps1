$env:JAVA_HOME = 'C:\Users\Lenovo\anaconda3\envs\briefcase\briefcase\Cache\tools\java17'
if (-not (Test-Path $env:JAVA_HOME)) {
    $env:JAVA_HOME = 'C:\Users\Lenovo\AppData\Local\BeeWare\briefcase\Cache\tools\java17'
}
$env:ANDROID_SDK_ROOT = 'C:\Users\Lenovo\AppData\Local\BeeWare\briefcase\Cache\tools\android_sdk'
$env:Path = "C:\Users\Lenovo\anaconda3;$env:Path"
cd build\sattva_sound\android\gradle
.\gradlew.bat assembleDebug --stacktrace > build_log.txt 2>&1
