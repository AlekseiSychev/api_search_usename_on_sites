R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow


def start_search(uname, dns, ulist, tout):
    found = []
    set_uname = uname
    set_timeout = []
    set_dns = []
    if uname == None and ulist == None:
        print(f'{R}[-] {C}Please provide {Y}one {C}of the following : \n\t{C}* {Y}username [-u]\n\t{C}* {Y}comma separated usernames [-l]\n\t{C}* {Y}file containing list of usernames [-f]{W}')
        exit()

    if uname != None:
        mode = 'single'
        if len(uname) > 0:
            if uname.isspace():
                print(f'{R}[-] {C}Username Missing!{W}')
                exit()
            else:
                pass
        else:
            print(f'{R}[-] {C}Username Missing!{W}')
            exit()

    elif ulist != None:
        mode = 'list'
        tmp = ulist
        if '%' not in tmp:
            print(f'{R}[-] {C}Invalid Format!{W}')
            exit()
        else:
            ulist = tmp.split('%')
    else:
        pass

    print(f'{G}[+] {C}Importing Modules...{W}')

    import socket
    import asyncio
    import aiohttp
    import tldextract
    from json import loads
    from datetime import datetime
    from requests import get, exceptions
    from sys import platform
    
    if platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    codes = [200, 301, 302, 403, 405, 410, 418, 500]

    async def clout(url):
        url = str(url)
        found.append(url)
        ext = tldextract.extract(url)
        dom = str(ext.domain)
        suf = str(ext.suffix)
        orig = f'{dom}.{suf}'
        cl_dom = f'{Y}{dom}.{suf}{C}'
        url = url.replace(orig, cl_dom)
        print(f'{G}[+] {C}{url}{W}')

    async def query(session, url, test, data, uname):
        try:
            if test == 'method':
                await test_method(session, url)
            elif test == 'string':
                await test_string(session, url, data)
            elif test == 'redirect':
                await test_redirect(session, url)
            elif test == 'api':
                data = data.format(uname)
                await test_api(session, url, data)
            elif test == 'alt':
                data = data.format(uname)
                await test_alt(session, url, data)
            else:
                response = await session.head(url, allow_redirects=True)
                if response.status in codes:
                    if test == None:
                        await clout(response.url)
                    elif test == 'url':
                        await test_url(response.url)
                    elif test == 'subdomain':
                        await test_sub(url, response.url)
                    else:
                        pass
                elif response.status == 404 and test == 'method':
                    await test_method(session, url)
                elif response.status != 404:
                    print(f'{R}[-] {Y}[{url}] {W}[{response.status}]')
                else:
                    pass
                
        except asyncio.exceptions.TimeoutError:
            print(f'{Y}[!] Timeout :{C} {url}{W}')
        except Exception as exc:
            print(f'{Y}[!] Exception [query] [{url}] :{W} {str(exc)}')

    async def test_method(session, url):
        try:
            response = await session.get(url, allow_redirects=True)
            if response.status != 404:
                await clout(response.url)
            else:
                pass
        except asyncio.exceptions.TimeoutError:
            print(f'{Y}[!] Timeout :{C} {url}{W}')
        except Exception as exc:
            print(f'{Y}[!] Exception [test_method] [{url}] :{W} {exc}')
            return

    async def test_url(url):
        url = str(url)
        proto = url.split('://')[0]
        ext = tldextract.extract(url)
        subd = ext.subdomain
        if subd != '':
            base_url = proto + '://' + subd  + '.' + ext.registered_domain
        else:
            base_url = proto + '://' + ext.registered_domain

        if url.endswith('/') == False and base_url.endswith('/') == True:
            if url + '/' != base_url:
                await clout(url)
            else:
                pass
        elif url.endswith('/') == True and base_url.endswith('/') == False:
            if url != base_url + '/':
                await clout(url)
            else:
                pass
        elif url != base_url:
            await clout(url)
        else:
            pass

    async def test_sub(url, resp_url):
        if url == str(resp_url):
            await clout(url)
        else:
            pass

    async def test_string(session, url, data):
        try:
            response = await session.get(url)
            if response.status == 404:
                pass
            elif response.status not in codes:
                print(f'{R}[-] {Y}[{url}] {W}[{response.status}]')
            else:
                resp_body = await response.text()
                if data in resp_body:
                    pass
                else:
                    await clout(response.url)
        except asyncio.exceptions.TimeoutError:
            print(f'{Y}[!] Timeout :{C} {url}{W}')
            return
        except Exception as exc:
            print(f'{Y}[!] Exception [test_string] [{url}] :{W} {exc}')
            return

    async def test_api(session, url, endpoint):
        try:
            response = await session.get(endpoint)
            if response.status != 404:
                resp_body = loads(await response.text())
                if len(resp_body) != 0:
                    tmp_vars = ['results', 'users', 'username']
                    for var in tmp_vars:
                        try:
                            if resp_body.get(var) != None:
                                if len(resp_body[var]) != 0:
                                    await clout(url)
                                    return
                                else:
                                    pass
                            else:
                                pass
                        except:
                            pass
                else:
                    pass
            else:
                pass
        except Exception as exc:
            print(f'{Y}[!] Exception [test_api] [{url}] :{W} {exc}')
            return

    async def test_alt(session, url, alt_url):
        try:
            response = await session.get(alt_url, allow_redirects=False)
            if response.status != 200:
                pass
            else:
                await clout(url)
        except Exception as exc:
            print(f'{Y}[!] Exception [test_alt] [{url}] :{W} {str(exc)}')
            return

    async def test_redirect(session, url):
        try:
            response = await session.head(url, allow_redirects=False)
        except asyncio.exceptions.TimeoutError:
            print(f'{Y}[!] Timeout :{C} {url}{W}')
            return
        except Exception as exc:
            print(f'{Y}[!] Exception [test_redirect] [{url}] :{W} {str(exc)}')
            return
        try:
            location = response.headers['Location']
            if url != location:
                pass
            else:
                await clout(url)
        except KeyError:
            await clout(url)

    async def main(uname):
        tasks = []
        print(f'\n{G}[+] {C}Target :{W} {uname}\n')

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:88.0) Gecko/20100101 Firefox/88.0'
        }
        try:
            resolver = aiohttp.AsyncResolver(nameservers=dns)
            set_dns.append(dns[0])

        except ValueError:
            resolver = aiohttp.AsyncResolver(nameservers=['1.1.1.1'])
            set_dns.append('1.1.1.1')
            print(f'{R}[-] {C}DNS ValueError! Set default dns [1.1.1.1].{W}')

        if tout > 5*60:
            timeout = aiohttp.ClientTimeout(total=20)
            print(f'{R}[-] {C}TIMEOUT ValueError! Set default timeout 20 sec.{W}')
            set_timeout.append(20)
        else:
            timeout = aiohttp.ClientTimeout(total=tout)
            set_timeout.append(tout)

        conn = aiohttp.TCPConnector(
            limit=0,
            family=socket.AF_INET,
            ssl=False,
            resolver=resolver
        )
        print(f'{Y}[!] Finding Profiles...{W}\n')
        async with aiohttp.ClientSession(connector=conn, headers=headers, timeout=timeout) as session:
            for block in urls_json:
                curr_url = block['url'].format(uname)
                test = block['test']
                data = block['data']
                task = asyncio.create_task(query(session, curr_url, test, data, uname))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def netcheck():
        print(f'\n{G}[+] {C}Checking Connectivity...{W}')
        try:
            rqst = get('https://github.com/', timeout=5)
            if rqst.status_code == 200:
                pass
            else:
                print(f'{Y}[!] {C}Status : {W}{rqst.status_code}')
        except exceptions.ConnectionError:
            print(f'{R}[-] {C}Connection Error! Exiting.{W}')
            exit()

    def launch(uname):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main(uname))
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
        

    try:
        netcheck()

        print(f'{Y}[!] Loading URLs...{W}')
        with open('url_store.json', 'r', encoding='utf-8') as url_store:
            raw_data = url_store.read()
            urls_json = loads(raw_data)
        print(f'{G}[+] {W}{len(urls_json)} {C}URLs Loaded!{W}')

        print(f'{G}[+] {C}Timeout     : {W}{tout} secs')
        print(f'{G}[+] {C}DNS Servers : {W}{dns}')

        start_time = datetime.now()
        
        if mode == 'single':
            launch(uname)
        elif mode == 'list':
            for uname in ulist:
                ulist[ulist.index(uname)] = uname.strip()
                launch(uname)
        else:
            pass

        end_time = datetime.now()
        delta = end_time - start_time
        
        if mode == 'single':
            print(f'\n{G}[+] {C}Lookup for {Y}{uname} {C}completed in {W}{delta}')
            print(f'\n{G}[+] {Y}{len(found)} {C}Possible Profiles Found for {Y}{uname}{W}')
        elif mode == 'list' or mode == 'file':
            print(f'\n{G}[+] {C}Lookup for {Y}{ulist} {C}completed in {W}{delta}')
            print(f'\n{G}[+] {Y}{len(found)} {C}Possible Profiles Found for {Y}{ulist}{W}')  
    except KeyboardInterrupt:
        print(f'{R}[-] {C}Keyboard Interrupt.{W}')
        exit()
    
    return {'USERNAME': set_uname,
            'USERNAME_list': ulist,
            'DNS': set_dns[0],
            'Timeout': set_timeout[0],
            'URLs': found
            }