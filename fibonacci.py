
startNumber = 1
endNumber = 50

def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

print (fib, range(startNumber, endNumber))
