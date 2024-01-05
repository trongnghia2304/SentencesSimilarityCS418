foreach($i in ls -recurse -filter "*.txt") {
    $temp = Get-Content $i.fullname
    Out-File -filepath $i.fullname -inputobject $temp -encoding utf8 -force
}