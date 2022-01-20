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

If ($args[0] -eq "-s"){
    Write-Host "Beginning silent Python $pythonVersion Installation"
    & $pythonDownloadPath /quiet InstallAllUsers=0 TargetDir=$pythonInstallDir | Out-Null
} else {
    & $pythonDownloadPath InstallAllUsers=0 TargetDir=$pythonInstallDir | Out-Null
}

& "$pythonInstallDir\python.exe" -m venv venv
# TODO: add dependencies.
# & "$(Get-Location)\venv\Scripts\python.exe" -m pip install
