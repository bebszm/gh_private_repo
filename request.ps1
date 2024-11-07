$TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"
$FILE="file.zip"                  # Your file name    
$VERSION="latest"                 # Release TAG                      
$GITHUB="https://api.github.com"
$releaseUrl = "$GITHUB/repos/<ORG_ID>/<REPO_NAME>/releases"
$response = gh_curl $releaseUrl
$response | Format-List 

Function gh_curl {
    param (
        [string]$url
    )
    $headers = @{
        "Authorization" = "token $TOKEN"
        "Accept" = "application/vnd.github.v3.raw"
    }
    return Invoke-RestMethod -Uri $url -Headers $headers
}

if ($response -is [System.Collections.IEnumerable]) {
    $asset_id = $response | ForEach-Object {
        if ($VERSION -eq "latest") {
            $_.assets | Where-Object { $_.name -eq $FILE } | Select-Object -First 1 -ExpandProperty id
        } else {
            $_ | Where-Object { $_.tag_name -eq $VERSION } | Select-Object -ExpandProperty assets | Where-Object { $_.name -eq $FILE } | Select-Object -First 1 -ExpandProperty id
        }
    }
} else {
    $asset_id = $response.assets | Where-Object { $_.name -eq $FILE } | Select-Object -First 1 -ExpandProperty id
}


$downloadUrl = "$GITHUB/repos/<ORG_ID>/<REPO_NAME>/releases/assets/$asset_id"
Invoke-WebRequest -Uri $downloadUrl -OutFile "C:\your\location\here\file.zip" -Headers @{ "Authorization" = "token $TOKEN"; "Accept" = "application/octet-stream" }
