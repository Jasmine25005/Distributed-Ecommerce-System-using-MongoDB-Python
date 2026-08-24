$ErrorActionPreference = "SilentlyContinue"

function Stop-PortProcess {
    param([int]$Port)

    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        $pids = $conn.OwningProcess | Sort-Object -Unique
        foreach ($pid in $pids) {
            Write-Host "Stopping process $pid on port $Port..."
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "No listening process found on port $Port."
    }
}

Stop-PortProcess 27017
Stop-PortProcess 27019
Stop-PortProcess 27101
Stop-PortProcess 27102
Stop-PortProcess 27103

Write-Host "Cluster processes stopped."
