#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

; incomes
^#y::
    Loop, 12
    {
        Send, ^{Tab}
        Sleep, 100
        Send, {Tab}
        Sleep, 100
        Loop, 9
        {
            Random, rand, 0, 100
            if (rand < 10)
            {
                Send, {Right}
                Sleep, 100
            }
        }
        Send, {Enter}
    }
return

; contributions
^#x::
    Loop, 12
    {
        Send, ^{Tab}
        Sleep, 100
        Send, {Tab}
        Sleep, 100
        Send, {Right}
        Sleep, 100
        Random, rand, 0, 10
        if (rand < 3)
        {
            Send, {Left}
            Sleep, 100
        }
        Send, {Right}
        Sleep, 100
        Random, rand, 0, 10
        if (rand < 3)
        {
            Send, {Left}
            Sleep, 100
        }
        Send, {Right}
        Sleep, 100
        Send, {Right}
        Sleep, 100
        Random, rand, 0, 10
        if (rand < 1)
        {
            Send, {Left}
            Sleep, 100
        }
        Send, {Enter}
    }
return

; feedback
^#c::
    Loop, 12
    {
        Send, ^{Tab}
        Sleep, 100
        Send, {Tab}
        Sleep, 100
        Send, {Enter}
        Sleep, 100
    }
return

; post
^#p::
    Loop, 12
    {
        Send, ^{Tab}
        Sleep, 100
        Loop, 8
        {
            Send, {Tab}
            Sleep, 100
            Send, {Down}
            Sleep, 100
        }
        Send, {Enter}
        Sleep, 100
    }
return
