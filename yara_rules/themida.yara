rule Themida_Protected
{
    strings:
        $a = "This program is protected with Themida"
        $b = ".themida"
    condition:
        any of them
}
