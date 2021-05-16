# Auto Almost Everything
# Youtube Channel https://www.youtube.com/c/AutoAlmostEverything
# Please read README.md carefully before use

# Solve captcha by using https://2captcha.com?from=11528745.

import threading, requests, time
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Modules import update, notification, captcha

app = 'FaucetCrypto'
app_path = 'https://faucetcrypto.com'
app_domain = 'faucetcrypto.com'

# Browser config
chromedriver_path = '.\\chromedriver.exe'  # <-- Change to your Chrome WebDriver path, replace "\" with "\\".
opts = Options()
opts.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'  # <-- Change to your Chromium browser path, replace "\" with "\\".
opts.add_experimental_option('excludeSwitches', ['enable-automation'])
opts.add_experimental_option('useAutomationExtension', False)
# opts.headless = True  # <-- Comment this line if you want to show browser.
cap = DesiredCapabilities.CHROME.copy()
cap['platform'] = 'WINDOWS'
cap['version'] = '10'
proxy = 'YourProxy'  # <-- To use proxy, replace 'YourProxy' by proxy string, ex: 18.222.190.66:81
if proxy != '' and proxy != 'YourProxy':
    proxies = Proxy({
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy,
        'proxyType': 'MANUAL',
    })
    proxies.add_to_capabilities(cap)
    opts.add_argument('--ignore-ssl-errors=yes')
    opts.add_argument('--ignore-certificate-errors')

# Account config
faucetcrypto_cookies = [
    {
        # Replace by your remember cookie name -->
        'name': 'remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82',
        # <-- Replace by your remember cookie value
        # Replace by your remember token -->
        'value': 'YourRememberToken',
        # <-- Replace by your remember token
        'domain': 'faucetcrypto.com',
        'path': '/',
    },
]

# Anti captcha config
autoCaptcha = False  # <-- Change to True if you want to use 2captcha to solve the captcha.
if autoCaptcha:
    # Replace by your 2Captcha API Key -->
    hc = captcha.AC_2Captcha('Your2CaptchaAPIKey')
    # <-- Replace by your 2Captcha API Key

sync = True


# Remove fixed elements
def RemoveFixedElements(browser):
    try:
        browser.find_element_by_xpath("//button[contains(text(), 'Skip')]").click()
        time.sleep(1)
    except:
        pass
    try:
        browser.find_element_by_xpath(
            "//button[contains(@class, 'chatbro_header_button chatbro_minimize_button')]").click()
        time.sleep(1)
    except:
        pass
    try:
        browser.execute_script('document.getElementsByClassName("chatbro_minimized_chat")[0].remove();')
    except:
        pass


# Claim Challenges
def ClaimChallenges(faucetcrypto_cookies):
    func = 'Claim Challenges'
    func_path = '/challenge/list'

    while True:
        global sync
        if sync:
            sync = False
            browser = webdriver.Chrome(desired_capabilities=cap, options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(app_path)
                for cookie in faucetcrypto_cookies:
                    browser.add_cookie(cookie)
                browser.get(app_path + func_path)
                time.sleep(1)
                RemoveFixedElements(browser)
                buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Claim Challenge')]")
                claimed = 0
                if len(buttons) > 0:
                    for button in buttons:
                        if 'cursor-pointer' in button.get_attribute('class'):
                            try:
                                button.click()
                                time.sleep(0.5)
                                claimed += 1
                            except:
                                pass
                if claimed:
                    notification.notify(app, 'Claimed %d challenges!' % claimed)
                else:
                    notification.notify(app, 'No challenge to claim!')
                time.sleep(1)
            except Exception as ex:
                print('%s has exception:\n%s!' % (app + ' ' + func, ex))
                notification.notify(app, '%s has exception:\n%s!' % (func, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(1800)
        else:
            time.sleep(1)


# Claim Faucet
def ClaimFaucet(faucetcrypto_cookies):
    func = 'Claim Faucet'
    func_path = '/task/faucet-claim'

    while True:
        global sync
        if sync:
            sync = False
            browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(app_path)
                for cookie in faucetcrypto_cookies:
                    browser.add_cookie(cookie)
                browser.get(app_path + func_path)
                time.sleep(1)
                RemoveFixedElements(browser)
                if 'Ready To Claim!' in browser.page_source:
                    time_start = time.time()
                    while True:
                        if 'Ready To Claim!' not in browser.page_source:
                            notification.notify(app, 'Claimed faucet!')
                            break
                        elif 'You have failed to complete the captcha many times' in browser.page_source:
                            notification.notify(app, 'Failed to complete the captcha many times!')
                            break
                        elif 'Please click on the similar buttons in the following order' in browser.page_source:
                            notification.sound()
                            notification.notify(app, 'Please solve captcha!')
                            time.sleep(60)
                            if 'Get Reward' in browser.page_source:
                                break
                        elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                            if autoCaptcha:
                                hcaptcha = browser.find_element_by_xpath(
                                    "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                sitekey = ''
                                for fragment in urlparse.urlparse(hcaptcha.get_attribute('src')).fragment.split(
                                        '&'):
                                    if 'sitekey=' in fragment:
                                        sitekey = fragment.split('=')[1]
                                        break
                                token = hc.HCaptcha(sitekey, browser.current_url)
                                task_id = None
                                xsrf_token = browser.get_cookie('XSRF-TOKEN')['value']
                                faucet_crypto_session = browser.get_cookie('faucet_crypto_session')['value']
                                link = 'https://faucetcrypto.com/task/generate-link'
                                cookies = {
                                    'XSRF-TOKEN': xsrf_token,
                                    'faucet_crypto_session': faucet_crypto_session,
                                }
                                headers = {
                                    'x-xsrf-token': xsrf_token.replace('%3D', '='),
                                }
                                data = {
                                    'type': 'faucet_claim',
                                    'task_id': task_id,
                                    'captcha': token,
                                }
                                res = requests.post(link, cookies=cookies, headers=headers, data=data, timeout=30)
                                browser.execute_script('window.location.href = arguments[0];', res.url)
                            else:
                                notification.sound()
                                notification.notify(app, 'Please solve captcha!')
                                time.sleep(60)
                                if 'Get Reward' in browser.page_source:
                                    break
                        elif 'Page Expired' in browser.page_source:
                            browser.refresh()
                        elif 'Get Reward' in browser.page_source:
                            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                            buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Get Reward')]")
                            if len(buttons) > 0:
                                for button in buttons:
                                    try:
                                        button.click()
                                    except:
                                        pass
                        if time.time() - time_start > 360:
                            notification.notify(app, 'Timeout.')
                            break
                    time.sleep(1)
                else:
                    notification.notify(app, 'Not ready to claim!')
            except Exception as ex:
                print('%s has exception:\n%s!' % (app + ' ' + func, ex))
                notification.notify(app, '%s has exception:\n%s!' % (func, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(1500)
        else:
            time.sleep(1)


# Do Ptc Ads
def DoPtcAds(faucetcrypto_cookies):
    func = 'Do Ptc Ads'
    func_path = '/ptc/list'

    while True:
        global sync
        if sync:
            sync = False
            delay_time = 60
            browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(app_path)
                for cookie in faucetcrypto_cookies:
                    browser.add_cookie(cookie)
                browser.get(app_path + func_path)
                time.sleep(1)
                RemoveFixedElements(browser)
                havePtcAds = True
                try:
                    a = browser.find_element_by_xpath(
                        "//a[contains(@href, 'https://faucetcrypto.com/task/ptc-advertisement/')]")
                    a_href = a.get_attribute('href')
                    browser.get(a_href)
                    time.sleep(1)
                except:
                    havePtcAds = False
                    delay_time = 3600
                    notification.notify(app, 'No Ptc Ads to click!')
                if havePtcAds:
                    time_start = time.time()
                    while True:
                        try:
                            if len(browser.window_handles) > 1:
                                target_tag = None
                                for handle in browser.window_handles:
                                    browser.switch_to.window(handle)
                                    if app_domain not in browser.current_url:
                                        browser.close()
                                    else:
                                        target_tag = handle
                                browser.switch_to.window(target_tag)
                            else:
                                browser.switch_to.window(browser.current_window_handle)
                        except:
                            pass
                        if 'You have failed to complete the captcha many times' in browser.page_source:
                            delay_time = 1500
                            notification.notify(app, 'Failed to complete the captcha many times!')
                            break
                        elif 'Please click on the similar buttons in the following order' in browser.page_source:
                            notification.sound()
                            notification.notify(app, 'Please solve captcha!')
                            time.sleep(60)
                            if 'Get Reward' in browser.page_source:
                                break
                        elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                            if autoCaptcha:
                                hcaptcha = browser.find_element_by_xpath(
                                    "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                sitekey = ''
                                for fragment in urlparse.urlparse(hcaptcha.get_attribute('src')).fragment.split('&'):
                                    if 'sitekey=' in fragment:
                                        sitekey = fragment.split('=')[1]
                                        break
                                token = hc.HCaptcha(sitekey, browser.current_url)
                                task_id = str(browser.current_url).split('/').pop()
                                xsrf_token = browser.get_cookie('XSRF-TOKEN')['value']
                                faucet_crypto_session = browser.get_cookie('faucet_crypto_session')['value']
                                link = 'https://faucetcrypto.com/task/generate-link'
                                cookies = {
                                    'XSRF-TOKEN': xsrf_token,
                                    'faucet_crypto_session': faucet_crypto_session,
                                }
                                headers = {
                                    'x-xsrf-token': xsrf_token.replace('%3D', '='),
                                }
                                data = {
                                    'type': 'ptc_advertisement',
                                    'task_id': task_id,
                                    'captcha': token,
                                }
                                res = requests.post(link, cookies=cookies, headers=headers, data=data, timeout=30)
                                browser.execute_script('window.location.href = arguments[0];', res.url)
                            else:
                                notification.sound()
                                notification.notify(app, 'Please solve captcha!')
                                time.sleep(60)
                                if 'Get Reward' in browser.page_source:
                                    break
                        elif 'Page Expired' in browser.page_source:
                            browser.refresh()
                        elif 'Get Reward' in browser.page_source:
                            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                            buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Get Reward')]")
                            if len(buttons) > 0:
                                for button in buttons:
                                    try:
                                        button.click()
                                    except:
                                        pass
                        elif 'Continue' in browser.page_source:
                            try:
                                browser.find_element_by_xpath("//a[contains(text(), 'Continue')]").click()
                                notification.notify(app, 'Completed task!')
                                break
                            except:
                                pass
                        if time.time() - time_start > 360:
                            notification.notify(app, 'Timeout.')
                            break
                        time.sleep(1)
            except Exception as ex:
                print('%s has exception:\n%s!' % (app + ' ' + func, ex))
                notification.notify(app, '%s has exception:\n%s!' % (func, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(delay_time)
        else:
            time.sleep(1)


# Do Short link
def DoShortlink(faucetcrypto_cookies):
    func = 'Do Shortlink'
    func_path = '/shortlink/list'
    func_domain = 'faucetcrypto.com/claim/step/'

    while True:
        global sync
        if sync:
            sync = False
            delay_time = 60
            browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(app_path)
                for cookie in faucetcrypto_cookies:
                    browser.add_cookie(cookie)
                browser.get(app_path + func_path)
                time.sleep(1)
                RemoveFixedElements(browser)
                haveShortlink = True
                while True:
                    try:
                        windows_count = len(browser.window_handles)
                        if windows_count > 1:
                            target_tag = None
                            for handle in browser.window_handles:
                                browser.switch_to.window(handle)
                                if app_domain not in browser.current_url:
                                    if windows_count > 1:
                                        browser.close()
                                    else:
                                        browser.get(app_path + func_path)
                                        target_tag = handle
                                else:
                                    target_tag = handle
                            browser.switch_to.window(target_tag)
                        else:
                            browser.switch_to.window(browser.current_window_handle)
                        browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                        if 'https://faucetcrypto.com/task/shortlink/short-fc' in browser.page_source:
                            browser.get('https://faucetcrypto.com/task/shortlink/short-fc')
                        elif 'https://faucetcrypto.com/task/shortlink/short-fg' in browser.page_source:
                            browser.get('https://faucetcrypto.com/task/shortlink/short-fg')
                        else:
                            haveShortlink = False
                            delay_time = 3600
                            notification.notify(app, 'No Shortlink to click!')
                        time.sleep(1)
                    except:
                        haveShortlink = False
                        delay_time = 3600
                        notification.notify(app, 'No Shortlink to click!')
                    finally:
                        break
                if haveShortlink:
                    time_start = time.time()
                    is_shortlink_page = False
                    step_count = 0
                    while True:
                        try:
                            if len(browser.window_handles) > 1:
                                target_tag = None
                                for handle in browser.window_handles:
                                    browser.switch_to.window(handle)
                                    if (app_domain not in browser.current_url and not is_shortlink_page) or (
                                            func_domain not in browser.current_url and is_shortlink_page):
                                        browser.close()
                                    else:
                                        target_tag = handle
                                browser.switch_to.window(target_tag)
                            else:
                                browser.switch_to.window(browser.current_window_handle)
                        except:
                            pass
                        if 'You have failed to complete the captcha many times' in browser.page_source:
                            delay_time = 1500
                            notification.notify(app, 'Failed to complete the captcha many times!')
                            break
                        elif 'Please click on the similar buttons in the following order' in browser.page_source:
                            notification.sound()
                            notification.notify(app, 'Please solve captcha!')
                            time.sleep(60)
                            if 'Get Reward' in browser.page_source:
                                break
                        elif 'widget containing checkbox for hCaptcha security challenge' in browser.page_source:
                            if autoCaptcha:
                                hcaptcha = browser.find_element_by_xpath(
                                    "//iframe[contains(@title, 'widget containing checkbox for hCaptcha security challenge')]")
                                sitekey = ''
                                for fragment in urlparse.urlparse(hcaptcha.get_attribute('src')).fragment.split('&'):
                                    if 'sitekey=' in fragment:
                                        sitekey = fragment.split('=')[1]
                                        break
                                token = hc.HCaptcha(sitekey, browser.current_url)
                                task_id = str(browser.current_url).split('/').pop()
                                xsrf_token = browser.get_cookie('XSRF-TOKEN')['value']
                                faucet_crypto_session = browser.get_cookie('faucet_crypto_session')['value']
                                link = 'https://faucetcrypto.com/task/generate-link'
                                cookies = {
                                    'XSRF-TOKEN': xsrf_token,
                                    'faucet_crypto_session': faucet_crypto_session,
                                }
                                headers = {
                                    'x-xsrf-token': xsrf_token.replace('%3D', '='),
                                }
                                data = {
                                    'type': 'shortlink',
                                    'task_id': task_id,
                                    'captcha': token,
                                }
                                res = requests.post(link, cookies=cookies, headers=headers, data=data, timeout=30)
                                browser.execute_script('window.location.href = arguments[0];',
                                                       res.headers['X-Inertia-Location'])
                            else:
                                notification.sound()
                                notification.notify(app, 'Please solve captcha!')
                                time.sleep(60)
                                if 'Get Reward' in browser.page_source:
                                    break
                        elif 'Page Expired' in browser.page_source:
                            browser.refresh()
                        elif 'Get Reward' in browser.page_source:
                            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                            buttons = browser.find_elements_by_xpath("//button[contains(text(), 'Get Reward')]")
                            if len(buttons) > 0:
                                for button in buttons:
                                    try:
                                        button.click()
                                    except:
                                        pass
                        elif '<span class="text-primary" id="timer">?</span>' in browser.page_source:
                            try:
                                browser.find_element_by_xpath(
                                    "//button[contains(text(), 'Show Timer / Click Here')]").click()
                                is_shortlink_page = True
                            except:
                                pass
                        elif '<span class="text-primary" id="timer">0</span>' in browser.page_source:
                            try:
                                browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
                                step_count += 1
                                if step_count == 3:
                                    notification.notify(app, 'Complete Shortlink task!')
                                    break
                            except:
                                pass
                        if time.time() - time_start > 360:
                            notification.notify(app, 'Timeout.')
                            break
                        time.sleep(1)
            except Exception as ex:
                print('%s has exception:\n%s!' % (app + ' ' + func, ex))
                notification.notify(app, '%s has exception:\n%s!' % (func, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(delay_time)
        else:
            time.sleep(1)


# Do Offerwalls
def DoOfferwalls_AsiaMag(faucetcrypto_cookies):
    func = 'Do Offerwalls - Asia Mag'
    func_path = 'http://asia-mag.com'
    func_domain = 'asia-mag.com'

    # Account config
    # Replace by your ASIA Mag visit code -->
    asiamag_visit_code = 'YourVisitCode'
    # <-- Replace by your ASIA Mag visit code

    while True:
        global sync
        if sync:
            sync = False
            delay_time = 60
            browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(func_path)
                time.sleep(1)
                # Step 0
                browser.find_element_by_xpath("//input[@name='Sid']").send_keys(asiamag_visit_code)
                browser.find_element_by_xpath("//input[@name='VIPAccess']").click()
                time.sleep(1)
                # Step 1,2,3,4
                time_start = time.time()
                while True:
                    try:
                        if len(browser.window_handles) > 1:
                            target_tag = None
                            for handle in browser.window_handles:
                                browser.switch_to.window(handle)
                                if func_domain not in browser.current_url:
                                    browser.close()
                                else:
                                    target_tag = handle
                            browser.switch_to.window(target_tag)
                        else:
                            browser.switch_to.window(browser.current_window_handle)
                    except:
                        pass
                    try:
                        browser.execute_script('''
                            var elements = document.getElementsByTagName("a");
                            for (var i = 0; i < elements.length; i++) {
                                if (elements[i].href.includes("asia-mag.com" != true)) {
                                    document.getElementsByTagName("a")[i].parentNode.removeChild(elements[i])
                                }
                            }
                        ''')
                    except:
                        pass
                    if 'This IP/User reached daily maximum sessions !' in browser.page_source:
                        delay_time = 43200
                        notification.notify(app, 'IP/Use reached daily maximum sessions.')
                        break
                    elif 'Thanks for your participation !</h1>' in browser.page_source:
                        notification.notify(app, "Completed offer!")
                        break
                    elif 'to continue...</h5>' in browser.page_source:
                        try:
                            browser.find_element_by_xpath("//div[@class='single-article']").click()
                        except:
                            pass
                    elif '/4 : Watch video <span' in browser.page_source:
                        try:
                            browser.execute_script('document.getElementsByTagName("video")[0].play();')
                        except:
                            pass
                    elif '/4 : Click to start !</button>' in browser.page_source:
                        try:
                            browser.find_element_by_xpath("//button[contains(text(), '/4 : Click to start !')]").click()
                        except:
                            pass
                    elif '/4 : Click on the top sidebar button !</h5>' in browser.page_source:
                        try:
                            browser.execute_script('window.scrollTo(0,0);')
                            browser.find_element_by_xpath("//button[contains(text(), 'Click & wait...')]").click()
                        except:
                            pass
                        try:
                            browser.execute_script('window.scrollTo(0,0);')
                            browser.find_element_by_xpath("//button[contains(text(), 'Final Step')]").click()
                        except:
                            pass
                    elif '/4 : Click on the bottom sidebar button !</h5>' in browser.page_source:
                        try:
                            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                            browser.find_element_by_xpath("//button[contains(text(), 'Click & wait 3s !')]").click()
                        except:
                            pass
                        try:
                            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                            browser.find_element_by_xpath("//button[contains(text(), 'Final Step')]").click()
                        except:
                            pass
                    elif '/4 : Complete captcha on bottom page !</h5>' in browser.page_source:
                        notification.sound()
                        notification.notify(app, 'Please solve captcha!')
                        time.sleep(90)
                        break
                    if time.time() - time_start > 360:
                        break
                    time.sleep(1)
            except Exception as ex:
                print('%s has exception:\n%s!' % (app + ' ' + func, ex))
                notification.notify(app, '%s has exception:\n%s!' % (func, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(delay_time)
        else:
            time.sleep(1)


if update.check():
    notification.notify(app, 'New version is released. Please download it! Thank you.')
else:
    try:
        threads = []
        threads.append(threading.Thread(target=ClaimChallenges, args=(faucetcrypto_cookies,)))
        threads.append(threading.Thread(target=ClaimFaucet, args=(faucetcrypto_cookies,)))
        threads.append(threading.Thread(target=DoPtcAds, args=(faucetcrypto_cookies,)))
        threads.append(threading.Thread(target=DoShortlink, args=(faucetcrypto_cookies,)))
        # threads.append(threading.Thread(target=DoOfferwalls_AsiaMag, args=()))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except Exception as ex:
        print('%s has exception:\n%s!' % (app, ex))
        notification.notify(app, '%s has exception:\n%s!' % (app, ex))
