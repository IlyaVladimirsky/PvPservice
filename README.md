###Note about work done.
Logic of the sevice is moved in the separate `class MatchLogic`. Thus I missed server side code, 
where it is more configurating than programming, but now anyone can use this implementation
of the task easily with a server and library he prefers. So He can just call create_match_request
function in the POST method and await its result. This implementation requires to use asychronous
processing of the client requests on the server side. One comfortable solution is to use 
[aiohttp](http://aiohttp.readthedocs.io/en/stable/) library. I did not implement database class, 
but describe methods and structure of db. It also allows to choose one of the solutions
(i.e. [sqlite](https://docs.python.org/3.5/library/sqlite3.html) is the simplest).
I wrote unit tests to check whether the logic works fine.

I consider other implementation of a service, when all client requests are processed consecutive, but then
the client would send requests constantly waiting for a successful response or a timeout response. But
in a given condition I think preferable to use my solution, where all requests are processed simultaneously. 
I think the problem of my solution is when many clients will send requests.

###How to install.
**Warning**! Python version >= 3.5.2

1) Clone the repository:

`git clone https://github.com/IlyaVladimirsky/PvPservice.git`

2) Installation: 

`sudo python setup.py install`

###How to run tests.
You must be situated in the root directory to run the tests! 
Then enter 

`sudo python -m unittest -v tests.test_logic`
