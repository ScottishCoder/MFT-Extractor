# ADD YOUR VOLUME LABEL. KEEP THE :
$MFTStartCluster=(fsutil fsinfo ntfsinfo VOLUMELABELHERE:) | select-string “ : “ | Select-String -Pattern 'Mft Valid Data Length' -SimpleMatch
write-host $MFTStartCluster
# Removes the labels up to the :
$MFTStartClusterData = $MFTStartCluster -replace ".*:"
write-host $MFTStartClusterData

$MFTSize = $MFTStartClusterData.Trim()

write-host $MFTSize
mkdir 'c:\scriptlog'
Add-Content 'C:\scriptlog\MFTSize.txt' $MFTSize
