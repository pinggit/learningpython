#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim:set cc=80:

if 0:
    # test OOB {{{1}}}
    class Student(object):
        __slots__ = ('name', 'age', 'score', '__privatename', '__grade')

        def __init__(self, name, score):
            self.name = name
            self.score = score
            self.__privatename = name

        def print_score(self):
            print '%s\'s score is %s' % (self.name, self.score)

        # use __grade to test controlling method to a member
        @property
        def grade(self):
            return self.__grade

        @grade.setter
        def grade(self, grade):
            self.__grade = grade

    jeremy = Student('jeremy', 92)

    print "jeremy's name is %s" % jeremy.name
    jeremy.print_score()
    print "jeremy's private name is %s" % jeremy._Student__privatename
    # print "private name is %s" % jeremy.__privatename

    class Student_in_america(Student):

        def print_score(self):
            print '%s\'name is %s' % (self.name, self.score * 20)

    xixi = Student_in_america('xixi', 4.7)
    print "xixi's name is %s" % xixi.name
    xixi.print_score()

    '''
    # test duotai {{{2}}}
    print "is jeremy a student?"
    isinstance(jeremy,Student)
    print "is jeremy an america student?"
    print isinstance(jeremy,Student_in_america)
    print "is xixi a student?"
    print isinstance(xixi,Student)
    print "is xixi an america student?"
    print isinstance(xixi,Student_in_america)
    '''

    '''
    # test dir, len
    print "dir of Student looks:-------------------------"
    print dir('Student')
    print len('Student')
    print "dir of Student_in_america looks:-----------------------"
    print dir('Student_in_america')
    '''

    # jeremy.set_grade(4)
    # print jeremy.get_grade()

    # test decoration {{{2}}}
    jeremy.grade = 4
    print jeremy.grade

    # test for loop for object {{{2}}}
    class Fib(object):

        def __init__(self):
            self.a, self.b = 0, 1   # 初始化两个计数器 a， b

        def __iter__(self):
            return self             # 实例本身就是迭代对象，故返回自己

        def next(self):
            self.a, self.b = self.b, self.a + self.b    # 计算下一个值
            if self.a > 3:          # 退出循环的条件
                raise StopIteration()
            return self.a           # 返回下一个值

    # pdb.set_trace()
    for n in Fib():
        print n

    # test jason {{{1}}}
if 0:
    import json
    d = dict(name='Bob', age=20, score=88)
    print "original dict looks %s" % d
    j = json.dumps(d)
    print "jsondump looks %s" % j
    d1 = json.loads(j)
    print "jsonloads looks %s" % d1

    # test jason {{{2}}}
    class Student(object):

        def __init__(self, name, age, score):
            self.name = name
            self.age = age
            self.score = score

    s = Student('Bob', 20, 88)
    # print(json.dumps(s))

    def student2dict(std):
        return {
            'name': std.name,
            'age': std.age,
            'score': std.score
        }

    print "json dump looks %s" % json.dumps(s, default=student2dict)

    # multi-tasking {{{1}}}

    # multi-processing:
    #    multiprocessing -> Process, Pool, Queue
    # multi-threading:
    #    threading ->

    # multiprocessing {{{2}}}
if 0:

    '''
    import os
    print 'Process (%s) start...' % os.getpid()
    pid = os.fork()
    if pid==0:
        print 'I am child process (%s) and my parent is %s.' % \
                (os.getpid(), os.getppid())
    else:
        print 'I (%s) just created a child process (%s).' % \
                (os.getpid(), pid)

    '''

    # multiprocessing.Process {{{3}}}
    print "---------------multiprocessing.Process----------------------"
    from multiprocessing import Process, Pool, Queue
    import time
    import os
    import random

    # 子进程要执行的代码
    def run_proc(name):
        print 'Run child process %s (%s)...' % (name, os.getpid())
        print 'child process %s sleep 1s now' % name
        time.sleep(1)

    if __name__ == '__main__':
        print 'Parent process %s.' % os.getpid()
        p = Process(target=run_proc, args=('test',))
        print 'will start a child process...'
        p.start()
        p.join()
        print 'parent Process end.'

    # multiprocessing.Pool {{{3}}}
    print "----------------multiprocessing.Pool---------------------"

    def long_time_task(name):
        print 'Run task %s (%s)...' % (name, os.getpid())
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print 'Task %s runs %0.2f seconds.' % (name, (end - start))

    if __name__ == '__main__':
        print 'Parent process %s.' % os.getpid()
        p = Pool()
        for i in range(10):
            p.apply_async(long_time_task, args=(i,))
        print 'Waiting for all subprocesses done...'
        p.close()
        p.join()

    # multiprocessing.Queue {{{3}}}

    print "----------------multiprocessing.Queue---------------------"

    # 写数据进程执行的代码:
    def write(q):
        for value in ['A', 'B', 'C']:
            print 'Put %s to queue...' % value
            q.put(value)
            time.sleep(random.random())

    # 读数据进程执行的代码:
    def read(q):
        while True:
            value = q.get(True)
            print 'Get %s from queue.' % value

    if __name__ == '__main__':
        # 父进程创建 Queue，并传给各个子进程：
        q = Queue()
        pw = Process(target=write, args=(q,))
        pr = Process(target=read, args=(q,))
        # 启动子进程 pw，写入:
        pw.start()
        # 启动子进程 pr，读取:
        pr.start()
        # 等待 pw 结束:
        pw.join()
        # pr 进程里是死循环，无法等待其结束，只能强行终止:
        pr.terminate()

    # multithreading {{{2}}}

if 0:

    print "---------------multithreading----------------------"
    # 启动一个线程就是把一个函数传入并创建 Thread 实例，然后调用 start()开始执行：

    import threading

    # 新线程执行的代码:
    def loop():
        print 'thread %s is running...' % threading.current_thread().name
        n = 0
        while n < 5:
            n = n + 1
            print '%s:thread %s >>> %s' % \
                (time.time(), threading.current_thread().name, n)
        time.sleep(1)
        print 'thread %s ended.' % threading.current_thread().name

    print 'thread %s is running...' % threading.current_thread().name
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print 'thread %s ended.' % threading.current_thread().name

    '''
    thread MainThread is running...
    thread LoopThread is running...
    1478741107.56:thread LoopThread >>> 1
    1478741107.56:thread LoopThread >>> 2
    1478741107.56:thread LoopThread >>> 3
    1478741107.56:thread LoopThread >>> 4
    1478741107.56:thread LoopThread >>> 5
    thread LoopThread ended.
    thread MainThread ended.
    '''

    # use global var without lock: wrong{{{3}}}
    '''
    problem of multi-threading:
        global var are shared by all threads
        and in multi-thread environment, things may get wrong
    '''

    from multiprocessing import Process, Pool, Queue
    import threading
    import time
    import os
    import random

    balance = 0

    def change_it(n):
        # 先存后取，结果应该为 0:
        global balance
        balance = balance + n
        balance = balance - n

    def run_thread(n):
        for i in range(100000):
            change_it(n)

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print balance

    '''
    ping@ubuntu47-3:~/Dropbox/python$ python test.py
    40
    ping@ubuntu47-3:~/Dropbox/python$ python test.py
    107
    ping@ubuntu47-3:~/Dropbox/python$ python test.py
    84
    ping@ubuntu47-3:~/Dropbox/python$ python test.py
    34
    '''

    # use global var withlock {{{3}}}
    '''
    one solution is to use thead lock

    '''
    from multiprocessing import Process, Pool, Queue
    import time
    import os
    import random
    import threading

    balance = 0

    lock = threading.Lock()

    def change_it(n):
        # 先存后取，结果应该为 0:
        global balance
        balance = balance + n
        balance = balance - n

    def run_thread(n):
        for i in range(100000):
            # 先要获取锁:
            lock.acquire()
            try:
                # 放心地改吧:
                change_it(n)
            finally:
                # 改完了一定要释放锁:
                lock.release()

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print balance

    # multi-core support {{{3}}}
    '''
    python threads' multi-core support

    '''
    import threading
    import multiprocessing

    def loop():
        x = 0
        while True:
            x = x ^ 1

    for i in range(multiprocessing.cpu_count()):
        t = threading.Thread(target=loop)
        t.start()

    # use local var with threading.local {{{3}}}
    '''
    thread1:
        process_thread:
            args:               Alice, name:Thread-A
            pass: Alice -> name
                process_student(name)
    thread2:
        process_thread:
            args:               Bob, name:Thread-B
            pass: Bob -> name
                process_student(name)

    '''
    import threading
    # 创建全局 ThreadLocal 对象:
    local_school = threading.local()

    def process_student():
        print 'Hello, %s (in %s)' % \
            (local_school.student, threading.current_thread().name)

    def process_thread(name):
        # 绑定 ThreadLocal 的 student:
        local_school.student = name
        process_student()

    t1 = threading.Thread(target=process_thread,
                          args=('Alice',), name='Thread-A')
    t2 = threading.Thread(target=process_thread,
                          args=('Bob',), name='Thread-B')

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    '''
    distributed computing:
    it looks for me, that server just dispatch a number (n in this case)
    client to get this number from the queue, and then do the task
    then client return the result (also a number) to server,
    then server display it.
    need to understand: how to use this in practical?
    '''
    role = 'server'
    # role = 'client'
    if role == 'server':
        # taskmanager.py {{{4}}}
        import random
        import time
        import Queue

        from multiprocessing.managers import BaseManager

        # 发送任务的队列:
        task_queue = Queue.Queue()

        # 接收结果的队列:
        result_queue = Queue.Queue()

        # 从 BaseManager 继承的 QueueManager:
        class QueueManager(BaseManager):
            pass

        # 把两个 Queue 都注册到网络上, callable 参数关联了 Queue 对象:
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)

        # 绑定端口 5000, 设置验证码'abc':
        manager = QueueManager(address=('', 5000), authkey='abc')

        # 启动 Queue:
        manager.start()

        # 获得通过网络访问的 Queue 对象:
        task = manager.get_task_queue()
        result = manager.get_result_queue()

        # 放几个任务进去:
        for i in range(10):
            n = random.randint(0, 10000)
            print('Put task %d...' % n)
            task.put(n)

        # 从 result 队列读取结果:
        print('Try get results...')
        for i in range(10):
            r = result.get(timeout=100)
            print('Result: %s' % r)

        # 关闭:
        manager.shutdown()

    else:
        # taskworker.py {{{4}}}
        import time
        import sys
        import Queue
        from multiprocessing.managers import BaseManager

        # 创建类似的 QueueManager:
        class QueueManager(BaseManager):
            pass

        # 由于这个 QueueManager 只从网络上获取 Queue，所以注册时只提供名字:
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        # 连接到服务器，也就是运行 taskmanager.py 的机器:
        server_addr = '127.0.0.1'
        print('Connect to server %s...' % server_addr)

        # 端口和验证码注意保持与 taskmanager.py 设置的完全一致:
        m = QueueManager(address=(server_addr, 5000), authkey='abc')

        # 从网络连接:
        m.connect()

        # 获取 Queue 的对象:
        task = m.get_task_queue()
        result = m.get_result_queue()

        # 从 task 队列取任务,并把结果写入 result 队列:
        for i in range(10):
            try:
                n = task.get(timeout=1)
                print('run task %d * %d...' % (n, n))
                r = '%d * %d = %d' % (n, n, n*n)
                time.sleep(1)
                result.put(r)
            except Queue.Empty:
                print('task queue is empty.')

        # 处理结束:
        print('worker exit.')

    # pyez {{{1}}}
    # Device module {{{2}}}

if 0:
    # pprint print things in a prettier format
    from pprint import pprint
    from jnpr.junos import Device

    # if __name__ == '__main__':

    # connect to router {{{3}}}
    # create an instance of class Device
    myrouter = Device(host='172.19.161.129', user='labroot', passwd='lab123')

    # start netconf-over-ssh connection to router
    # this will return the same instance 'myrouter', represented as
    # "Device(myrouter)"
    myrouter.open()

    from IPython.Shell import IPShellEmbed
    IPShellEmbed([])()

    # #above 2 lines can be merged into one line
    # myrouter=Device(host='172.19.161.129',user='labroot',passwd='lab123').open()

    # close the netconf connection
    myrouter.close()
    # myrouter.facts dict {{{3}}}

if 0:
    # facts gathering is enabled by default, can be disabled to speed up:
    #    dev.open(gather_facts=False)
    # and later can still be enabled:
    # dev.facts_refresh()
    pprint(myrouter.facts)

    interface_lxml_element = myrouter.rpc.get_interface_information(terse=True)
    list_of_interfaces = interface_lxml_element.findall('physical-interface')
    print "list_of_interfaces looks %s:" % list_of_interfaces

    for interface in list_of_interfaces:
        # print "interface in the list looks: %s" % interface
        print "Interface: %s Status: %s " % (
                interface.findtext('name').strip(),
                interface.findtext('oper-status').strip()
        )

    # myrouter.cli: send a command
    print myrouter.cli("show interfaces terse fxp0")

    # myrouter.close()

    # yaml module {{{2}}}
if 0:
    import yaml
    ethport_yaml_file_path = \
        '/usr/local/lib/python2.7/dist-packages/jnpr/junos/op/ethport.yml'
    yaml_file = open(ethport_yaml_file_path, "r")
    data = yaml.load(yaml_file)
    print data
    for key in data:
        print "key: %s" % key
        print "value: %s" % data[key]

    # EthPortTable module {{{2}}}
if 0:
    '''
    EthPortTable module
    '''
    from jnpr.junos import Device
    from jnpr.junos.op.ethport import EthPortTable
    from pprint import pprint

    myrouter = Device(host='172.19.161.129', user='labroot', passwd='lab123')
    myrouter.open()

    # create EthPortTable obj
    eth_interfaces = EthPortTable(myrouter)
    eth_interfaces.get()

    print "eth_interface.keys() looks:\n  ",
    pprint(eth_interfaces.keys())

    for interface in eth_interfaces:
        print "interface.keys() looks:\n  ",
        print interface.keys()
        print interface.name + "'s keys,name,admin,oper,macadd looks:"
        print "  " + interface.name, interface.admin,\
            interface.oper, interface.macaddr

    myrouter.close()

    # Config module {{{2}}}
if 0:
    from jnpr.junos import Device
    from jnpr.junos.utils.config import Config
    import time
    import os
    import sys
    from jnpr.junos.exception import *

    MAX_ATTEMPTS = 3
    WAIT_BEFORE_RECONNECT = 10

    # Assumes r0 already exists and is a connected device instance

    for attempt in range(MAX_ATTEMPTS):
        try:
            myrouter = Device(host='172.19.161.129', user='labroot',
                              passwd='lab123')
            myrouter.open()
            cfg = Config(myrouter)

            print "connection opened"

            # load override abc.conf {{{3}}}
            # this won't work, for some reason, has to use either absolute path,
            # or change the dir first
            config_file = "~/download_folder/backup.botanix.161101.jtac.conf"

            # this works
            config_file = \
                "/home/ping/download_folder/backup.botanix.161101.jtac.conf"
            cfg.load(path=config_file, format="text", merge=True)

            # #this works
            # os.chdir('/home/ping/download_folder')
            # cfg.load(path="backup.botanix.161101.jtac.conf",overwrite=True)

            print "config loaded"

            # commit confirm {{{3}}}
            cfg.commit(confirm=2)
            time.sleep(10)

            print "commit confirm 2"

            # commit {{{3}}}
            cfg.commit()

            print "commited"

            # edit exclusive {{{3}}}
            cfg.lock()

            # rollback 2 {{{3}}}
            cfg.rollback(rb_id=2)

            print "rollback 2"
            # commit {{{3}}}
            cfg.commit()

            print "commited"

            # unlock {{{3}}}
            cfg.unlock()

            # config one statement {{{3}}}
            cfg.load("set system host-name mytest_python",
                     format="set", merge=True)
            print cfg.diff()
            cfg.rollback(0)

            myrouter.close

        except ConnectAuthError:
            print "Authentication error!"
            myrouter.close()
            sys.exit()
        except ConnectTimeoutError:
            print "Timeout error!"
            myrouter.close()
            sys.exit()
        except ConfigLoadError:
            print "Couldn't unlock the config db!"
            myrouter.close()
            sys.exit()
        except Exception as error:
            if isinstance(error, RpcTimeoutError):
                print "Rpc Timeout while loading the config!"
                myrouter.close()

            # elif type(error) is CommitError:
            else:
                print "Encountered an expected exception"
                print error
                sys.exit()

# route table {{{2}}}
if 0:

    from jnpr.junos.op.routes import RouteTable

    route_table = RouteTable(myrouter)

    route_table.get('192.168.1.0/24')

    route_table.get('12.123.73.43/32')

    route_table.get()

    route_table.get('192.168.4.0/24', table='inet.0', protocol='static')

    route_table.get(protocol='isis')

    for key in route_table:
        print key.name + ' Nexthop: ' + key.nexthop + ' Via: ' + \
              key.via + ' Protocol: ' + key.protocol


# a working example {{{2}}}

if 0:

    #!/usr/bin/env python
    """Use interface descriptions to track the topology reported by LLDP.
    This includes the following steps:
    1) Gather LLDP neighbor information.
    2) Gather interface descriptions.
    3) Parse LLDP neighbor information previously stored in the descriptions.
    4) Compare LLDP neighbor info to previous LLDP info from the descriptions.
    5) Print LLDP Up / Change / Down events.
    6) Store the updated LLDP neighbor info in the interface descriptions.
    Interface descriptions are in the format:
    [user-configured description ]LLDP: <remote system> <remote port>[(DOWN)]
    The '(DOWN)' string indicates an LLDP neighbor which was previously
    present, but is now not present.
    """

    import sys
    import getpass
    import jxmlease
    from jnpr.junos import Device
    from jnpr.junos.utils.config import Config
    import jnpr.junos.exception

    TEMPLATE_PATH = 'interface_descriptions_template.xml'

    # Create a jxmlease parser with desired defaults.
    parser = jxmlease.EtreeParser()
    class DoneWithDevice(Exception): pass

    def main():         # {{{3}}}

        """The main loop.
        Prompt for a username and password.
        Loop over each device specified on the command line.
        Perform the following steps on each device:
        1) Get LLDP information from the current device state.
        2) Get interface descriptions from the device configuration.
        3) Compare the LLDP information against the previous snapshot of LLDP
        information stored in the interface descriptions. Print changes.
        4) Build a configuration snippet with new interface descriptions.
        5) Commit the configuration changes.
        Return an integer suitable for passing to sys.exit().
        """

        if len(sys.argv) == 1:
            print("\nUsage: %s device1 [device2 [...]]\n\n" % sys.argv[0])
            return 1
        rc = 0

        # Get username and password as user input.
        user = raw_input('Device Username: ')
        password = getpass.getpass('Device Password: ')

        for hostname in sys.argv[1:]:
            try:
                print("Connecting to %s..." % hostname)
                dev = Device(host=hostname,
                             user=user,
                             password=password,
                             normalize=True
                             )
                dev.open()

                # retrieving LLDP info {{{4}}}
                print("Getting LLDP information from %s..." % hostname)
                lldp_info = get_lldp_neighbors(device=dev)

                if lldp_info == None:
                    print(" Error retrieving LLDP info on " +\
                            hostname +\
                            ". Make sure LLDP is enabled."
                    )
                    rc = 1
                    raise DoneWithDevice

                # retrieving int desc info {{{4}}}
                print("Getting interface descriptions from %s..." % hostname)
                desc_info = get_description_info_for_interfaces(device=dev)

                if desc_info == None:
                    print(" Error retrieving interface descriptions on %s." %
                            hostname)
                    rc = 1
                    raise DoneWithDevice

                # check lldp change {{{4}}}
                desc_changes = check_lldp_changes(lldp_info, desc_info)
                if not desc_changes:
                    print(" No LLDP changes to configure on %s." % hostname)
                    raise DoneWithDevice

                # load merge temp config {{{4}}}
                if load_merge_template_config(
                        device=dev,
                        template_path=TEMPLATE_PATH,
                        template_vars={'descriptions': desc_changes}
                ):
                    print("Successfully committed configuration changes on %s."
                          % hostname)
                else:
                    print(" Error committing description changes on %s." %
                          hostname)
                    rc = 1
                    raise DoneWithDevice

            except jnpr.junos.exception.ConnectError as err:
                print(" Error connecting: " + repr(err))
                rc = 1

            except DoneWithDevice:
                pass

            finally:
                print(" Closing connection to %s." % hostname)
                try:
                    dev.close()
                except:
                    pass

        return rc


    def get_lldp_neighbors(device): # {{{3}}}

        """
        Get current LLDP neighbor information.
        Return a two-level dictionary with the LLDP neighbor information.
        The first-level key is the local port (aka interface) name.
        The second-level keys are 'system' for the remote system name
        and 'port' for the remote port ID. On error, return None.
        For example:
        {'ge-0/0/1': {'system': 'r1', 'port', 'ge-0/0/10'}}
        """

        lldp_info = {}

        try:
            resp = device.rpc.get_lldp_neighbors_information()

        except (jnpr.junos.exception.RpcError,
                jnpr.junos.exception.ConnectError) as err:

            print " " + repr(err)
            return None

        for nbr in resp.findall('lldp-neighbor-information'):
            local_port = nbr.findtext('lldp-local-port-id')
            remote_system = nbr.findtext('lldp-remote-system-name')
            remote_port = nbr.findtext('lldp-remote-port-id')

            if local_port and (remote_system or remote_port):
                lldp_info[local_port] = {
                        'system': remote_system,
                        'port': remote_port
                }

        return lldp_info


    def get_description_info_for_interfaces(device):  # {{{3}}}


        """
        Get current interface description for each interface.
        Parse the description into the user-configured description, remote system,
        and remote port components.
        Return a two-level dictionary. The first-level key is the local port (aka
        interface) name. The second-level keys are 'user_desc' for the
        user-configured description, 'system' for the remote system name, 'port'
        for the remote port, and 'down', which is a Boolean indicating if LLDP was
        previously down. On error, return None.  For example: {'ge-0/0/1':
        {'user_desc': 'test description', 'system': 'r1', 'port': 'ge-0/0/10',
        'down': True}}
        """

        desc_info = {}

        try:

            resp = parser(device.rpc.get_interface_information(descriptions=True))

        except (jnpr.junos.exception.RpcError,
                jnpr.junos.exception.ConnectError) as err:

            print " " + repr(err)
            return None

        try:

            pi = resp['interface-information']['physical-interface'].jdict()

        except KeyError:

            return desc_info

        for (local_port, port_info) in pi.items():

            try:

                (udesc, _, ldesc) = port_info['description'].partition('LLDP: ')
                udesc = udesc.rstrip()
                (remote_system, _, remote_port) = ldesc.partition(' ')
                (remote_port, down_string, _) = remote_port.partition('(DOWN)')
                desc_info[local_port] = {
                    'user_desc': udesc,
                    'system': remote_system,
                    'port': remote_port,
                    'down': True if down_string else False
                }
            except (KeyError, TypeError):
                pass
            return desc_info


    def check_lldp_changes(lldp_info, desc_info):   # {{{3}}}

        """
        Compare current LLDP info with previous snapshot from descriptions.
        Given the dictionaries produced by get_lldp_neighbors() and
        get_description_info_for_interfaces(), print LLDP up, change, and down
        messages.
        Return a dictionary containing information for the new descriptions
        to configure.
        """
        desc_changes = {}
        # Iterate through the current LLDP neighbor state. Compare this
        # to the saved state as retrieved from the interface descriptions.
        for local_port in lldp_info:
            lldp_system = lldp_info[local_port]['system']
            lldp_port = lldp_info[local_port]['port']
            has_lldp_desc = desc_info.has_key(local_port)

            desc_system = desc_port = False

            if has_lldp_desc:
                desc_system = desc_info[local_port]['system']
                desc_port = desc_info[local_port]['port']
                down = desc_info[local_port]['down']
            if not desc_system or not desc_port:
                has_lldp_desc = False
            if not has_lldp_desc:
                print(" %s LLDP Up. Now: %s %s" \
                        % \
                    (local_port,lldp_system,lldp_port)
                    )
            elif down:
                print(" %s LLDP Up. Was: %s %s Now: %s %s" %
                (local_port,desc_system,desc_port,lldp_system,lldp_port))
            elif lldp_system != desc_system or lldp_port != desc_port:
                print(" %s LLDP Change. Was: %s %s Now: %s %s" %
                (local_port,desc_system,desc_port,lldp_system,lldp_port))
            else:
                # No change. LLDP was not down. Same system and port.
                continue
            desc_changes[local_port] = "LLDP: %s %s" % (lldp_system,lldp_port)

        # Iterate through the saved state as retrieved from the interface
        # descriptions. Look for any neighbors that are present in the
        # saved state, but are not present in the current LLDP neighbor
        # state.
        for local_port in desc_info:
            desc_system = desc_info[local_port]['system']
            desc_port = desc_info[local_port]['port']
            down = desc_info[local_port]['down']
            if (desc_system and desc_port and not down
                and not lldp_info.has_key(local_port)):

                print(" %s LLDP Down. Was: %s %s" %
                    (local_port,desc_system,desc_port))
                desc_changes[local_port] = "LLDP: %s %s(DOWN)" % \
                    (desc_system, desc_port)

        # Iterate through the list of interface descriptions we are going
        # to change. Prepend the user description, if any.
        for local_port in desc_changes:
            try:
                udesc = desc_info[local_port]['user_desc']
            except KeyError:
                continue
            if udesc:
                desc_changes[local_port] = udesc + " " + desc_changes[local_port]

        return desc_changes

    def load_merge_template_config(device, template_path, template_vars): # {{{3}}}

        """
        Load templated config with "configure private" and "load merge".
        Given a template_path and template_vars, do:
            configure private,
            load merge of the templated config,
            commit,
            and check the results.
        Return True if the config was committed successfully, False otherwise.
        """

        class LoadNotOKError(Exception):
            pass

        device.bind(cu=Config)
        rc = False

        try:

            try:
                # configure private
                resp = device.rpc.open_configuration(private=True)
            except jnpr.junos.exception.RpcError as err:
                if not (err.rpc_error['severity'] == 'warning' and
                        'uncommitted changes will be discarded on exit' in
                        err.rpc_error['message']):
                    raise
            resp = device.cu.load(
                    template_path=template_path,
                    template_vars=template_vars,
                    merge=True
            )
            if resp.find("ok") is None:
                raise LoadNotOKError
            device.cu.commit(comment="made by %s" % sys.argv[0])

        except (jnpr.junos.exception.RpcError,
                jnpr.junos.exception.ConnectError,
                LoadNotOKError) as err:
            print " " + repr(err)

        except:
            print " Unknown error occurred loading or committing configuration."

        else:
            rc = True

        try:

            device.rpc.close_configuration()

        except jnpr.junos.exception.RpcError as err:

            print " " + repr(err)

        rc = False
        return rc

    if __name__ == "__main__":
        sys.exit(main())

# upgrade sw {{{2}}}

if 0:

    import os, sys, logging
    from jnpr.junos import Device
    from jnpr.junos.utils.sw import SW
    from jnpr.junos.exception import *

    host = 'dc1a.example.com'
    package = '/var/tmp/junos-install/jinstall-13.3R1.8-domestic-signed.tgz'
    remote_path = '/var/tmp'
    validate = True
    logfile = '/var/log/junos-pyez/install.log'

    def do_log(msg, level='info'):
        getattr(logging, level)(msg)

    def update_progress(dev, report):
        # log the progress of the installing process
        do_log(report)

    def main():

        # initialize logging
        logging.basicConfig(filename=logfile, level=logging.INFO,
                            format='%(asctime)s:%(name)s: %(message)s')
        logging.getLogger().name = host
        sys.stdout.write('Information logged in {0}\n'.format(logfile))

        # verify package exists
        if (os.path.isfile(package)):
            found = True
        else:
            msg = 'Software package does not exist: {0}. '.format(package)
            sys.exit(msg + '\nExiting program')

        dev = Device(host=host)
        try:
            dev.open()
        except Exception as err:
            sys.stderr.write('Cannot connect to device: {0}\n'.format(err))
            return

        # Increase the default RPC timeout to accommodate install operations
        dev.timeout = 300

        # Create an instance of SW
        sw = SW(dev)

        try:
            do_log('Starting the software upgrade process: {0}'.format(package))
            ok = sw.install(package=package, remote_path=remote_path,
                            progress=update_progress, validate=validate)
        except Exception as err:
            msg = 'Unable to install software, {0}'.format(err)
            do_log(msg, level='error')
        else:
            if ok is True:
                do_log('Software installation complete. Rebooting')
                rsp = sw.reboot()
                do_log('Upgrade pending reboot cycle, please be patient.')
                do_log(rsp)

        # End the NETCONF session and close the connection
        dev.close()

    if __name__ == "__main__":
        main()

# issu {{{2}}}

if 0:

    from jnpr.junos import Device
    from pprint import pprint
    from jnpr.junos.utils.sw import SW

    with Device(host=xxxx, user=xxxx, password=xxx) as dev:
        pprint(dev.facts)
        sw = SW(dev)
        try:
            ok = sw.install(package='/var/home/regress/junos-srx5000-12.1X47-D43-domestic.tgz', issu=True,
                    no_copy=True, progress=True)
            print 'Install Status %s' % ok
            if ok is not True:
                print "sw.install returned False"
        except Exception as ex:
            print "ERROR: %s" % ex.message


# web {{{1}}}

# crawl {{{2}}}

if 0:

    # work flow {{{3}}}
    # class:
    #    Crawler
    #        get_page
    #        go
    #    Retriever
    #        get_file
    #        download
    #        parse_links

    # main:
    #    robot=Crawler.go
    #    robot.go
    #        get_page
    #            r=Retriever
    #                get_file
    #                download
    #                parse_links

    #            r.download
    #            r.parse_links
    #                #add links to q
    # !/usr/bin/env python

    import cStringIO
    import formatter
    import htmllib
    import httplib
    import os
    import sys
    import urllib
    import urlparse

    class Retriever(object):        # {{{3}}}

        # the only attributes that instances can have are self.url and
        # self.file.
        __slots__ = ('url', 'file')

        def __init__(self, url):
            self.url, self.file = self.get_file(url)

        def get_file(self, url, default='index.html'):  # {{{4}}}
            'Create usable local filename from URL'
            parsed = urlparse.urlparse(url)

            # find host: www.null.com
            host = parsed.netloc.split('@')[-1].split(':')[0]

            # set file full path:
            # www.null.com+/home/index.html
            filepath = '%s%s' % (host, parsed.path)

            # if filepath no '.html', meaning only www.null.com/a/b/c
            # assume index.html
            if not os.path.splitext(parsed.path)[1]:
                filepath = os.path.join(filepath, default)

            # set dir name: 'www.null.com/home'
            linkdir = os.path.dirname(filepath)

            # on confliction of this folder name, erase and create the folder
            if not os.path.isdir(linkdir):
                if os.path.exists(linkdir):
                    os.unlink(linkdir)
                os.makedirs(linkdir)

            return url, filepath

        def download(self):     # {{{4}}}
            'Download URL to specific named file'
            try:
                retval = urllib.urlretrieve(self.url, self.file)
            except (IOError, httplib.InvalidURL) as e:
                retval = (('*** ERROR: bad URL "%s": %s' % (self.url, e)),)
            return retval

        def parse_links(self):  # {{{4}}}
            'Parse out the links found in downloaded HTML file'

            f = open(self.file, 'r')
            data = f.read()
            f.close()
            parser = htmllib.HTMLParser(
                        formatter.AbstractFormatter(
                            formatter.DumbWriter(
                                cStringIO.StringIO()
                            )
                        )
                    )
            parser.feed(data)
            parser.close()

            # return list of url
            return parser.anchorlist

    class Crawler(object):  # {{{3}}}

        count = 0

        def __init__(self, url):    # {{{4}}}
            self.q = [url]
            self.seen = set()

            # retrieve domain name
            parsed = urlparse.urlparse(url)
            host = parsed.netloc.split('@')[-1].split(':')[0]
            self.dom = '.'.join(host.split('.')[-2:])

        def get_page(self, url, media=False):   # {{{4}}}
            'Download page & parse links, add to queue if nec'
            r = Retriever(url)

            # download the url
            fname = r.download()[0]

            if fname[0] == '*':
                print fname, '... skipping parse'
                return

            Crawler.count += 1

            print '\n(', Crawler.count, ')'
            print 'URL:', url
            print 'FILE:', fname
            self.seen.add(url)

            ftype = os.path.splitext(fname)[1]
            if ftype not in ('.htm', '.html'):
                return

            for link in r.parse_links():
                if link.startswith('mailto:'):
                    print '... discarded, mailto link'
                    continue

                if not media:
                    ftype = os.path.splitext(link)[1]
                    if ftype in ('.mp3', '.mp4', '.m4v', '.wav'):
                        print '... discarded, media file'
                        continue

                if not link.startswith('http://'):
                    link = urlparse.urljoin(url, link)

                print '*', link,

                if link not in self.seen:
                    if self.dom not in link:
                        print '... discarded, not in domain'
                    else:
                        if link not in self.q:
                            self.q.append(link)
                            print '... new, added to Q'
                        else:
                            print '... discarded, already in Q'
                else:
                    print '... discarded, already processed'

        def go(self, media=False):
            'Process next page in queue (if any)'
            while self.q:
                url = self.q.pop()
                self.get_page(url, media)

    def main():     # {{{3}}}

        # get url
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            try:
                url = raw_input('Enter starting URL: ')
            except (KeyboardInterrupt, EOFError):
                url = ''
        if not url:
            return
        if not url.startswith('http://') and \
           not url.startswith('ftp://'):
            url = 'http://%s/' % url
        #
        robot = Crawler(url)
        robot.go()

    if __name__ == '__main__':
        main()


# parse_links.py {{{2}}}

if 0:

    from HTMLParser import HTMLParser
    from cStringIO import StringIO
    from urllib2 import urlopen
    from urlparse import urljoin

    from BeautifulSoup import BeautifulSoup, SoupStrainer
    from html5lib import parse, treebuilders

    URLS = (
        'http://python.org',
        'http://google.com',
    )

    def output(x):
        print '\n'.join(sorted(set(x)))

    def simpleBS(url, f):
        'simpleBS() - use BeautifulSoup to parse all tags to get anchors'
        output(
            urljoin(url, x['href'])
            for x in BeautifulSoup(f).findAll('a')
        )

    def fasterBS(url, f):
        'fasterBS() - use BeautifulSoup to parse only anchor tags'
        output(
            urljoin(url, x['href'])
            for x in BeautifulSoup(
                f,
                parseOnlyThese=SoupStrainer('a')
            )
        )

    def htmlparser(url, f):
        'htmlparser() - use HTMLParser to parse anchor tags'
        class AnchorParser(HTMLParser):

            # called every time a new tag is encountered in the file stream
            def handle_starttag(self, tag, attrs):

                if tag != 'a':
                    return
                if not hasattr(self, 'data'):
                    self.data = []
                for attr in attrs:
                    if attr[0] == 'href':
                        self.data.append(attr[1])

        parser = AnchorParser()
        parser.feed(f.read())
        output(urljoin(url, x) for x in parser.data)

    def html5libparse(url, f):
        'html5libparse() - use html5lib to parse anchor tags'
        output(
            urljoin(url, x.attributes['href'])
            for x in parse(f)
            if isinstance(x, treebuilders.simpletree.Element) and
            x.name == 'a'
        )

    def process(url, data):
        print '\n*** simple BS'
        simpleBS(url, data)
        data.seek(0)
        print '\n*** faster BS'
        fasterBS(url, data)
        data.seek(0)
        print '\n*** HTMLParser'
        htmlparser(url, data)
        data.seek(0)
        print '\n*** HTML5lib'
        html5libparse(url, data)

    def main():
        for url in URLS:
            f = urlopen(url)
            data = StringIO(f.read())
            f.close()
            process(url, data)

    if __name__ == '__main__':
        main()

# wsgi {{{2}}}

if 0:
    from pprint import pprint

    def application(environ, start_response):
        pprint(environ)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'ping')
        # return '<h1>Hello, web!</h1>'

    # server.py
    # 从 wsgiref 模块导入:
    from wsgiref.simple_server import make_server

    # 导入我们自己编写的 application 函数:
    # from hello import application

    # 创建一个服务器， IP 地址为空，端口是 8000，处理函数是 application:
    httpd = make_server('', 8000, application)

    print "Serving HTTP on port 8000..."

    # 开始监听 HTTP 请求:
    httpd.serve_forever()

# flask {{{3}}}

if 0:

    from flask import Flask
    from flask import request

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        return '<h1>Home</h1>'

    @app.route('/signin', methods=['GET'])
    def signin_form():
        return '''<form action="/signin" method="post">
        <p><input name="username"></p>
        <p><input name="password" type="password"></p>
        <p><button type="submit">Sign In</button></p>
        </form>'''

    @app.route('/signin', methods=['POST'])
    def signin():
        # 需要从 request 对象读取表单内容：
        if request.form['username'] == 'admin' and\
           request.form['password'] == 'password':
            return '<h3>Hello, dmin!</h3>'
        return '<h3>Bad username or password.</h3>'

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')

# getopt {{{1}}}

if 0:

    import sys
    import getopt

    def usage():
        print("Usage:%s [-a|-o|-c] [--help|--output] args...." % sys.argv[0])

    if "__main__" == __name__:

        try:
            opts, args = getopt.getopt(
                sys.argv[1:], "ao:c", ["help", "output="]
            )

            print("============ opts ==================")
            print(opts)

            print("============ args ==================")
            print(args)

            # check all param
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    usage()
                    sys.exit(1)
                elif opt in ("-t", "--test"):
                    print("for test option")
                else:
                    print("%s  ==> %s" % (opt, arg))

        except getopt.GetoptError as e:
            print("getopt error!")
            print e
            usage()
            sys.exit(1)

# twisted {{{1}}}

if 0:

    from twisted.internet import task
    from twisted.internet import reactor

    def runEverySecond():
        print "a second has passed"
        # print "a second has passed"

    l = task.LoopingCall(runEverySecond)
    l.start(1.0)  # call every second

    # l.stop() will stop the looping calls
    reactor.run()

# game {{{1}}}

if 0:

    # Tic Tac Toe
    # This is the solution for the Milestone Project! A two player game made
    # within a Jupyter Notebook. Feel free to download the notebook to
    # understand how it works!
    # First some imports we'll need to use for displaying output and set the
    # global variables

    # Specifically for the iPython Notebook environment for clearing output.
    from IPython.display import clear_output

    # Global variables
    board = [' '] * 10
    game_state = True
    announce = ''

    # Next make a function that will reset the board, in this case we'll store
    # values as a list.

    # Note: Game will ignore the 0 index
    def reset_board():  # {{{2}}}
        global board , game_state
        board = [' '] * 10
        game_state = True

    # Now create a function to display the board, I'll use the num pad as the
    # board reference. Note: Should probably just make board and player classes
    # later....

    def display_board():    # {{{2}}}
        ''' This function prints out the board so the numpad can be used as a
        reference '''
        # Clear current cell output
        clear_output()
        # Print board
        print "  "+board[7]+" |"+board[8]+" | "+board[9]+" "
        print "------------"
        print "  "+board[4]+" |"+board[5]+" | "+board[6]+" "
        print "------------"
        print "  "+board[1]+" |"+board[2]+" | "+board[3]+" "

    # Define a function to check for a win by comparing inputs in the board
    # list.  Note: Maybe should just have a list of winning combos and cycle
    # through them?

    def win_check(board, player):   # {{{2}}}
        ''' Check Horizontals,Verticals, and Diagonals for a win '''
        if (board[7] == board[8] == board[9] == player) or \
           (board[4] == board[5] == board[6] == player) or \
           (board[1] == board[2] == board[3] == player) or \
           (board[7] == board[4] == board[1] == player) or \
           (board[8] == board[5] == board[2] == player) or \
           (board[9] == board[6] == board[3] == player) or \
           (board[1] == board[5] == board[9] == player) or \
           (board[3] == board[5] == board[7] == player):
            return True
        else:
            return False

    # Define function to check if the board is already full in case of a tie.
    # (This is straightforward with our board stored as a list) Just remember
    # index 0 is always empty.

    def full_board_check(board):    # {{{2}}}
        ''' Function to check if any remaining blanks are in the board '''
        if " " in board[1:]:
            return False
        else:
            return True

    # Now define a function to get player input and do various checks on it.

    def ask_player(mark):   # {{{2}}}
        ''' Asks player where to place X or O mark, checks validity '''
        global board
        req = "Choose where to place your '" + mark + "': "
        while True:
            try:
                choice = int(raw_input(req))
            except ValueError:
                print("Sorry, please input a number between 1-9.")
                continue
            if board[choice] == " ":
                board[choice] = mark
                break
            else:
                print "That space isn't empty!"
                continue

    # Now have a function that takes in the player's choice (via the ask_player
    # function) then returns the game_state.

    def player_choice(mark):    # {{{2}}}
        global board, game_state, announce
        # Set game blank game announcement
        announce = ''
        # Get Player Input
        mark = str(mark)
        # Validate input
        ask_player(mark)
        # Check for player win
        if win_check(board, mark):
            clear_output()
            display_board()
            announce = mark + " wins! Congratulations"
            game_state = False

        # Show board
        clear_output()
        display_board()
        # Check for a tie
        if full_board_check(board):
            announce = "Tie!"
            game_state = False

        return game_state, announce

    # Finally put it all together in a function to play the game.

    def play_game():    # {{{2}}}
        reset_board()
        global announce

        # Set marks
        X = 'X'
        O = 'O'
        while True:
            # Show board
            clear_output()
            display_board()

            # Player X turn
            game_state, announce = player_choice(X)
            print announce
            if game_state is False:
                break

            # Player O turn
            game_state, announce = player_choice(O)
            print announce
            if game_state is False:
                break

        # Ask player for a rematch
        rematch = raw_input('Would you like to play again? y/n')
        if rematch == 'y':
            play_game()
        else:
            print "Thanks for playing!"

    # Let's play!

    if __name__ == "__main__":
        play_game()

    #   O |X |
    # ------------
    #   X |X | O
    # ------------
    #   O |X |
    # X wins! Congratulations
    # Would you like to play again? y/nn
    # Thanks for playing!


# re {{{1}}}

if 0:

    # In [3]: run test.py testre.txt local2:80 /tmp

    # test data file: restre.txt
    # NameVirtualHost 127.0.0.1:80
    # <VirtualHost localhost:80>
    #     DocumentRoot /var/www/
    #     <Directory />
    #     Options FollowSymLinks
    #     AllowOverride None
    #     </Directory>
    #     ErrorLog /var/log/apache2/error.log
    #     LogLevel warn
    #     CustomLog /var/log/apache2/access.log combined
    #     ServerSignature On
    # </VirtualHost>
    # <VirtualHost local2:80>
    #     DocumentRoot /var/www2/
    #     <Directory />
    #     Options FollowSymLinks
    #     AllowOverride None
    #     </Directory>
    #     ErrorLog /var/log/apache2/error2.log
    #     LogLevel warn
    #     CustomLog /var/log/apache2/access2.log combined
    #     ServerSignature On
    # </VirtualHost>

    from cStringIO import StringIO
    import re
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

    vhost_start = re.compile(r'<VirtualHost\s+(.*?)>')
    vhost_end = re.compile(r'</VirtualHost')
    docroot_re = re.compile(r'(DocumentRoot\s+)(\S+)')

    def replace_docroot(conf_string, vhost, new_docroot):
        '''yield new lines of an httpd.conf file where docroot lines matching
        the specified vhost are replaced with the new_docroot
        '''

        conf_file = StringIO(conf_string)
        in_vhost = False
        curr_vhost = None

        for line in conf_file:

            # for each line check if it contains block start flag?
            # (<VirtualHost...>)
            vhost_start_match = vhost_start.search(line)
            # if yes, get the vhost name from the first word in the matched
            # part, that is first word #after "VirtualHost ", in this line
            # below, it should be "local2:80"
            #
            #   <VirtualHost local2:80>
            #
            # then we are sure we are now "in" the block that we are looking
            # for
            if vhost_start_match:
                curr_vhost = vhost_start_match.groups()[0]
                in_vhost = True

            # if we are in the block, and the vhost is what we are looking for
            # start to search the docroot "DocumentRoot"
            if in_vhost and (curr_vhost == vhost):
                docroot_match = docroot_re.search(line)

                # once found, replace first match group with new_docroot
                if docroot_match:
                    #                                  \0         \1    ?
                    #                           ________________  ___
                    # docroot_re = re.compile(r'(DocumentRoot\s+)(\S+)')
                    sub_line = docroot_re.sub(r'\1%s' % new_docroot, line)
                    # then replace old line with new line, for yield (generator)
                    line = sub_line

            # check if the line is the end of block, if yes, then we are
            # stepping out of the block
            vhost_end_match = vhost_end.search(line)
            if vhost_end_match:
                in_vhost = False

            yield line

    if __name__ == '__main__':
        import sys

        # test.py testre.txt local2:80 /tmp
        #         ---------- --------- ----

        # name of the file to be processed
        conf_file = sys.argv[1]

        # name of the VirtualHost section to be located
        # <VirtualHost local2:80>
        #              ---------
        vhost = sys.argv[2]

        # name of the new DocumentRoot value to be applied
        # DocumentRoot /var/www/
        #              ---------
        docroot = sys.argv[3]

        conf_string = open(conf_file).read()
        for line in replace_docroot(conf_string, vhost, docroot):
            print line,

# unit test {{{1}}}

# module -> function to be tested {{{2}}}

if 0:

    """
    USAGE:
    apache_log_parser_split.py some_log_file
    This script takes one command line argument: the name of a log file
    to parse. It then parses the log file and generates a report which
    associates remote hosts with number of bytes transferred to them.
    """
    import sys
    import re

    # dictify_logline is the function to be tested

    # regex with these features:
    # VERBOSE, comments, named group
    log_line_re = re.compile(r'''
        (?P<remote_host>\S+)  #IP ADDRESS
        \s+                   # whitespace
        \S+                   # remote logname
        \s+                   # whitespace
        \S+                   # remote user
        \s+                   # whitespace
        \[[^\[\]]+\]          # time
        \s+                   # whitespace
        "[^"]+"               # first line of request
        \s+                   # whitespace
        (?P<status>\d+)       # status
        \s+                   # whitespace
        (?P<bytes_sent>-|\d+) # bytes_sent
        \s*                   # whitespace
        ''', re.VERBOSE)

    # version1: Example 3-24. Apache logfile parser—split on white space
    def dictify_logline(line):
        '''return a dictionary of the pertinent pieces of an apache combined
        log file Currently, the only fields we are interested in are remote
        host and bytes sent, but we are putting status in there just for
        good measure.
        '''
        split_line = line.split()
        return {'remote_host': split_line[0],
                'status': split_line[8],
                'bytes_sent': split_line[9],
        }

    # version2: Example 3-26. Apache logfile parser—regex
    def dictify_logline(line):
        '''return a dictionary of the pertinent pieces of an apache combined log
        file Currently, the only fields we are interested in are remote host and
        bytes sent, but we are putting status in there just for good measure.
        '''
        m = log_line_re.match(line)
        if m:
            groupdict = m.groupdict()
            if groupdict['bytes_sent'] == '-':
                groupdict['bytes_sent'] = '0'
            return groupdict
        else:
            return {'remote_host': None,
                    'status': None,
                    'bytes_sent': "0",
            }

    def generate_log_report(logfile):
        '''return a dictionary of format remote_host=>[list of bytes sent]
        This function takes a file object, iterates through all the lines in
        the file, and generates a report of the number of bytes transferred
        to each remote host for each hit on the webserver.
        '''
        report_dict = {}
        for line in logfile:
            line_dict = dictify_logline(line)
            print line_dict
            try:
                bytes_sent = int(line_dict['bytes_sent'])
            except ValueError:

                # totally disregard anything we don't understand
                continue
        report_dict.setdefault(line_dict['remote_host'], []).append(bytes_sent)
        return report_dict

    if __name__ == "__main__":
        if not len(sys.argv) > 1:
            print __doc__
            sys.exit(1)
        infile_name = sys.argv[1]
        try:
            infile = open(infile_name, 'r')
        except IOError:
            print "You must specify a valid file to parse"
            print __doc__
            sys.exit(1)
        log_report = generate_log_report(infile)
        print log_report
        infile.close()

# unit test code {{{2}}}
if 0:

    # unit test code
    # save below code in another file, say utest.py, and run :
    # ./utest.py
    # test result:
    # In [64]: run  /tmp/temp.py
    # ...F
    # ======================================================================
    # FAIL: testMalformed (__main__.TestApacheLogParser)
    # ----------------------------------------------------------------------
    # Traceback (most recent call last):
    #       File "/tmp/temp.py", line 68, in testMalformed
    #           'bytes_sent': '2326'})
    #           AssertionError: {'status': 'space.html', 'bytes_sent': 'HTTP/1.0"', 'remote_host': '127.0.0.1'} != {'status': '200', 'bytes_sent': '2326', 'remote_host': '127.0.0.1'}
    #           - {'bytes_sent': 'HTTP/1.0"', 'remote_host': '127.0.0.1',
    #              'status': 'space.html'}
    #           ?                 ^^^^^^^^^                                          ^^^^^^^^^^

    #           + {'bytes_sent': '2326', 'remote_host': '127.0.0.1', 'status': '200'}
    #           ?                 ^^^^                                          ^^^


    #           ----------------------------------------------------------------------
    #           Ran 4 tests in 0.012s

    #           FAILED (failures=1)
    #           An exception has occurred, use %tb to see the full traceback.

    #           SystemExit: True

    import imp
    import unittest
    test = imp.load_source('test', '/home/pings/python/test.py')
    from test import dictify_logline

    class TestApacheLogParser(unittest.TestCase):

        def setUp(self):
            pass

        def testCombinedExample(self):

            # test the combined example from apache.org
            combined_log_entry = \
                '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] ' \
                '"GET /apache_pb.gif HTTP/1.0" 200 2326 ' \
                "http://www.example.com/start.html" \
                "Mozilla/4.08 [en] (Win98; I;Nav)"

            self.assertEqual(
                dictify_logline(combined_log_entry),
                {
                    'remote_host': '127.0.0.1',
                    'status': '200',
                    'bytes_sent': '2326'
                }
            )

        def testCommonExample(self):
            # test the common example from apache.org
            common_log_entry = \
                '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] ' \
                '"GET /apache_pb.gif HTTP/1.0" 200 2326'
            self.assertEqual(
                dictify_logline(common_log_entry),
                {
                    'remote_host': '127.0.0.1',
                    'status': '200',
                    'bytes_sent': '2326'
                }
            )

        def testExtraWhitespace(self):
            # test for extra whitespace between fields
            common_log_entry = \
                '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '\
                '"GET /apache_pb.gif HTTP/1.0" 200 2326'
            self.assertEqual(
                dictify_logline(common_log_entry),
                {
                    'remote_host': '127.0.0.1', 'status': '200',
                    'bytes_sent': '2326'
                }
            )

        def testMalformed(self):
            # test for extra whitespace between fields
            common_log_entry = \
                '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '\
                '"GET /some/url/with white space.html HTTP/1.0" 200 2326'
            self.assertEqual(
                dictify_logline(common_log_entry),
                {'remote_host': '127.0.0.1', 'status': '200',
                 'bytes_sent': '2326'})

    if __name__ == '__main__':
        unittest.main()

# pdf {{{1}}}

## simplest {{{2}}}

if 0:

    from reportlab.pdfgen import canvas

    def hello():
        c = canvas.Canvas("helloworld.pdf")
        c.drawString(100, 100, "Hello World")
        c.showPage()
        c.save()

    hello()

## medium {{{2}}}

if 1:

    import subprocess
    import datetime
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    def disk_report():
        p = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE)
        return p.stdout.readlines()

    def create_pdf(input, output="disk_report.pdf"):
        now = datetime.datetime.today()
        date = now.strftime("%h %d %Y %H:%M:%S")
        c = canvas.Canvas(output)
        textobject = c.beginText()
        textobject.setTextOrigin(inch, 11*inch)
        textobject.textLines('''Disk Capacity Report: %s''' % date)

        for line in input:
            textobject.textLine(line.strip())
            c.drawText(textobject)
            c.showPage()
            c.save()

    report = disk_report()
    create_pdf(report)
