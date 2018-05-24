rule baseline_01
{
    meta:
        description = "behavior of baseline_01"
        date = "2018-05-17"
    strings:
        $a = "eval" nocase
    condition:
        $a
}