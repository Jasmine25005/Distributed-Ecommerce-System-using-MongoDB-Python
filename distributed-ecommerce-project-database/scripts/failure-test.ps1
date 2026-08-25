$ErrorActionPreference = "Continue"

Write-Host "========================================"
Write-Host "   ROLE 5 - FAILURE HANDLING TEST"
Write-Host "========================================"

Write-Host ""
Write-Host "STEP 1: Current Replica Set Status"

mongosh --port 27101 --eval "rs.status().members.forEach(function(m){print(m.name + ' -> ' + m.stateStr)})"

Write-Host ""
Write-Host "STEP 2: Simulating Egypt Primary Failure"
Write-Host "Stopping port 27101..."

$conn = Get-NetTCPConnection -LocalPort 27101 -State Listen -ErrorAction SilentlyContinue

if ($conn) {

    $processId = $conn.OwningProcess | Select-Object -First 1

    Write-Host "Stopping process $processId..."

    Stop-Process -Id $processId -Force

    Write-Host "Egypt Primary (27101) stopped successfully."

} else {

    Write-Host "No process found on port 27101."

}

Write-Host ""
Write-Host "Waiting for replica-set election..."
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "STEP 3: Checking New Primary"

mongosh --port 27111 --eval "printjson(db.hello())"

Write-Host ""
Write-Host "STEP 4: Replica Set Status"

mongosh --port 27111 --eval "rs.status().members.forEach(function(m){print(m.name + ' -> ' + m.stateStr)})"

Write-Host ""
Write-Host "========================================"
Write-Host "Failure handling test completed."
Write-Host "========================================"