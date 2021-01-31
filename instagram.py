from instapy_cli import client

username = 'tik_your_toks'
password = '***********'
video = './dg0z0cs86de61.mp4'
cookie_file = 'COOKIE_FOR_USER.json'
text = 'This will be the caption of your video.' + '\r\n' + 'You can also use hashtags! #hash #tag #now'

with client(username, password, cookie_file=cookie_file, write_cookie_file=True) as cli:
    # get string cookies
    cookies = cli.get_cookie()
    # print(type(cookies)) # == str
    # print(cookies)
    cli.upload(video, text)
    #This doesnt work anymore :(