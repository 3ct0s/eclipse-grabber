$pythonVersion = "3.8.9"
$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion.exe"
$pythonDownloadPath = "$(Get-Location)\python-$pythonVersion.exe"
$pythonInstallDir = "$(Get-Location)\python$pythonVersion"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

if (-not(Test-Path -Path $pythonDownloadPath -PathType Leaf)) {
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonDownloadPath
} else {
    Write-Host "$pythonDownloadPath already exists."
}

& $pythonDownloadPath /quiet InstallAllUsers=0 TargetDir=$pythonInstallDir | Out-Null
& "$pythonInstallDir\python.exe" -m venv venv
& "$(Get-Location)\venv\Scripts\python.exe" -m pip install pyinstaller==4.6
