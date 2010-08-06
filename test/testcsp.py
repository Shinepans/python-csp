from csp.csp import *
from csp.guards import Timer
#set_debug(True)

@process
def foo(n):
    time.sleep(random.random()*2)
    print('foo() got argument {0}'.format(n))
    return


@process
def send(cout):
    """
    readset =
    writeset = cout
    """
    for i in range(5):
        print('send() is sending {0}'.format(i))
        cout.write(i)
    return


@process
def recv(cin):
    """
    readset = cin
    writeset =
    """
    for i in range(5):
        data = cin.read()
        print('recv() has received {0}'.format(str(data)))
    return


@process
def send100(cout):
    """
    readset =
    writeset = cout
    """
    for i in range(100):
        print('send100() is sending {0}'.format(i))
        cout.write(i)
    return


@process
def recv100(cin):
    """
    readset = cin
    writeset =
    """
    for i in range(100):
        data = cin.read()
        print('recv100() has received {0}'.format(str(data)))
    return



@process
def sendAlt(cout, num):
    """
    readset =
    writeset = cout
    """
    t = Timer()
    t.sleep(1)
    cout.write(num)
    return


@process
def testAlt0():
    alt = Alt(Skip(), Skip(), Skip())
    for i in range(3):
        print('*** TestAlt0 selecting...')
        val = alt.select()
        print('* Got this from Alt:' + str(val))
    return


@process
def testAlt1(cin):
    """
    readset = cin
    writeset =
    """
    alt = Alt(cin)
    numeric = 0 
    while numeric < 1:
        print('*** TestAlt1 selecting...')
        val = alt.select()
        if isinstance(val, int): numeric += 1 
        print('* Got this from Alt:' + str(val))
    return


@process
def testAlt2(cin1, cin2, cin3):
    """
    readset = cin1, cin2, cin3
    writeset =
    """
    alt = Alt(Skip(), cin1, cin2, cin3)
    numeric = 0 
    while numeric < 3:
        print('*** TestAlt2 selecting...')
        val = alt.select()
        if isinstance(val, int): numeric +=1
        print('* Got this from Alt:' + str(val))
    return


@process
def testAlt3(cin1, cin2, cin3):
    """
    readset = cin1, cin2, cin3
    writeset =
    """
    # For obvious reasons, SKIP cannot go first 
    alt = Alt(cin1, cin2, cin3, Skip())
    numeric = 0
    while numeric < 3:
        print('*** TestAlt3 selecting...')        
        val = alt.pri_select()
        if isinstance(val, int): numeric +=1
        print('* Got this from Alt:' + str(val))
    return


@process
def testAlt4(cin1, cin2, cin3):
    """
    readset = cin1, cin2, cin3
    writeset =
    """
    alt = Alt(Skip(), cin1, cin2, cin3)
    numeric = 0
    while numeric < 3:
        print('*** TestAlt4 selecting...')        
        val = alt.fair_select()
        if isinstance(val, int): numeric +=1
        print('* Got this from Alt:' + str(val))
    return


@process
def testOr(cin1, cin2):
    """
    readset = cin1, cin2
    writeset =
    """
    print(cin1 | cin2)
    print(cin1 | cin2)
    return


@process
def testAltRRep(cin1, cin2, cin3):
    """
    readset = cin1, cin2, cin3
    writeset =
    """
    gen = Alt(cin1, cin2, cin3) * 3
    print(next(gen))
    print(next(gen))
    print(next(gen))
    return


@process
def testAltLRep(cin1, cin2, cin3):
    """
    readset = cin1, cin2, cin3
    writeset =
    """
    gen = 3 * Alt(cin1, cin2, cin3)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    return


########## Top level stuff

def _printHeader(name):
    random.seed(time.clock()) # Introduce a bit more randomness...    
    print('')
    print('****************************************************')
    print('* Testing {0}...'.format(name))
    print('****************************************************')
    print('')
    return




def testAlt():
    _printHeader('Alt')
    print('Alt with 3 SKIPs:')
    ta0 = testAlt0()
    ta0.start()
    print('')
    print('Alt with 1 channel read:')
    ch1 = Channel()
    Par(testAlt1(ch1), sendAlt(ch1, 100)).start()
    print('')
    print('Alt with 1 SKIP, 3 channel reads:')
    ch2, ch3, ch4 = Channel(), Channel(), Channel()
    Par(testAlt2(ch2, ch3, ch4),
		sendAlt(ch2, 100),
		sendAlt(ch3, 200),
		sendAlt(ch4, 300)).start()
    print('')
    print('Alt with priSelect on 1 SKIP, 3 channel reads:')
    ch5, ch6, ch7 = Channel(), Channel(), Channel()
    ta3 = Par(testAlt3(ch5, ch6, ch7),
              sendAlt(ch5, 100),
              sendAlt(ch6, 200),
              sendAlt(ch7, 300))
    ta3.start()
    print('')
    print('Alt with fairSelect on 1 SKIP, 3 channel reads:')
    ch8, ch9, ch10 = Channel(), Channel(), Channel()
    Par(testAlt4(ch8, ch9, ch10),
		sendAlt(ch8, 100),
		sendAlt(ch9, 200),
		sendAlt(ch10, 300)).start()
    return


def testChoice():
    _printHeader('Choice')
    print('Choice with |:')
    c1, c2 = Channel(), Channel()
    Par(sendAlt(c1, 100), sendAlt(c2, 200), testOr(c1, c2)).start()
    return


def testRep():
    _printHeader('Repetition')
    print('Repetition with Alt * int:')
    ch1, ch2, ch3 = Channel(), Channel(), Channel()
    Par(sendAlt(ch1, 100), sendAlt(ch2, 200), sendAlt(ch3, 300),
        testAltRRep(ch1, ch2, ch3)).start()
    print('')
    print('Repetition with Alt * int:')
    ch1, ch2, ch3 = Channel(), Channel(), Channel()
    Par(sendAlt(ch1, 100), sendAlt(ch2, 200), sendAlt(ch3, 300),
        testAltLRep(ch1, ch2, ch3)).start()
    return


        testAlt()
        testChoice()
        testRep()
    elif options.alt: testAlt()
    elif options.choice: testChoice()
    elif options.rep: testRep()
