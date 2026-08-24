$ErrorActionPreference = "Stop"

$MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin"
$BaseDir  = "C:\mongodb-ddb"

$mongod = Join-Path $MongoBin "mongod.exe"
$mongos = Join-Path $MongoBin "mongos.exe"

if (!(Test-Path $mongod)) { throw "mongod.exe not found at $mongod" }
if (!(Test-Path $mongos)) { throw "mongos.exe not found at $mongos" }

New-Item -ItemType Directory -Force -Path "$BaseDir\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$BaseDir\egypt"  | Out-Null
New-Item -ItemType Directory -Force -Path "$BaseDir\europe" | Out-Null
New-Item -ItemType Directory -Force -Path "$BaseDir\usa"    | Out-Null

Write-Host "Starting Config Server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$mongod' --configsvr --replSet cfgRS --port 27019 --dbpath '$BaseDir\config' --bind_ip localhost"

Start-Sleep -Seconds 2

Write-Host "Starting Egypt shard..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$mongod' --shardsvr --replSet rsEgypt --port 27101 --dbpath '$BaseDir\egypt' --bind_ip localhost"

Write-Host "Starting Europe shard..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$mongod' --shardsvr --replSet rsEurope --port 27102 --dbpath '$BaseDir\europe' --bind_ip localhost"

Write-Host "Starting USA shard..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$mongod' --shardsvr --replSet rsUSA --port 27103 --dbpath '$BaseDir\usa' --bind_ip localhost"

Start-Sleep -Seconds 4

Write-Host "Starting mongos router..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$mongos' --configdb cfgRS/localhost:27019 --port 27017 --bind_ip localhost"

Write-Host ""
Write-Host "Cluster processes started."
Write-Host "Router connection: mongodb://localhost:27017"
