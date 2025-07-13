rule Themida_Protected
{
    strings:
        $a = "This program is protected with Themida"
        $b = ".themida"
        $c = "VMProtect"
        $d = ".vmp"
    condition:
        any of them
}
