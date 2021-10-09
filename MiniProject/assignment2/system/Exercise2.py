text = input("Enter String: ")
def start(t, n):
    if n >= len(t):
        exit()
    if t[n] == 'a':
        char_a(t, n+1)
    else:
        start(t, n+1)
        
def char_a(t, n):
    if n >= len(t):
        exit()
    if t[n] == 'a':
        char_a(t, n+1)
    elif t[n] == 'b':
        char_b(t, n+1)
    else:
        start(t, n+1)
def char_b(t, n):
    if n >= len(t):
        exit()
    if t[n] == 'a':
        char_a(t, n+1)
    elif t[n] == 'c':
        char_c(t, n+1)
    else:
        start(t, n+1)
def char_c(t, n):
    if n >= len(t):
        exit()
    if t[n] == 'a':
        char_a(t, n+1)
    elif t[n] == 'd':
        char_d(t, n+1)
    else:
        start(t, n+1)
        
def char_d(t, n):
    print('abcd is contained in the string\n')
    if n >= len(t):
        exit()
    if t[n] == 'a':
        char_a(t, n+1)
    else:
        start(t, n+1)    
start(text, 0)