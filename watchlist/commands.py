import click
from watchlist import app, db
from watchlist.models import User, Ariticles


# 自定义initdb
@app.cli.command()
@click.option('--drop', is_flag=True, help='删除之后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo('删除数据库成功')
    db.create_all()
    click.echo('初始化数据库')


# 自定义命令forge，把数据写入数据库
@app.cli.command()
def forge():
    db.create_all()
    articles = [
        {'title': '微信小程序入门讲解',
         'content': 'linux里共有以下几类文件，分别为目录（directory）、（普通）文件（file）、链接文件（link file）、块设备（block）、字符设备（character）、管道文件（pipe）、套接字文件（sockt），灰色标记文件可先忽略。然后文件属性跟windows一样有最新修改时间、文件的大小、所属用户、所属组、文件的操作权限（读入、写入、执行）等，我们可以用下面的命令查看当前目录下的文件的类型及文件属性。',
         'author_id': 1},
        {'title': 'linux下添加环境变量',
         'content': '输出：/home/geeksongs/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/mnt/c/Program Files/WindowsApps/CanonicalGroupLimited.UbuntuonWindows_1804.2019.521.0_x64__79rhkp1fndgsc:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0/:/mnt/c/Windows/System32/OpenSSH/:/mnt/c/Program Files/Intel/WiFi/bin/:/mnt/c/Program Files/Common Files/Intel/WirelessCommon/:/mnt/c/Program Files (x86)/Intel/Intel(R) Management Engine Components/DAL:/mnt/c/Program Files/Intel/Intel(R) Management Engine Components/DAL:/mnt/c/Users/THINK/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Python 3.8:/mnt/c/Users/THINK/AppData/Local/Programs/Python/Python38:/mnt/c/Users/THINK/AppData/Local/Programs/Python/Python38/Scripts:/mnt/c/Users/THINK/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/THINK/AppData/Local/Programs/Microsoft VS Code/bin:/snap/bin里面具有这个环境变量，第一个就是我们刚刚添加的文件夹目录，则环境变量添加成功！！',
         'author_id': 1}
    ]
    name = "陈亚飞"
    username = 'fei'
    user = User(name=name, username=username)
    user.set_password('123123')
    db.session.add(user)
    for m in articles:
        article = Ariticles(title=m['title'], content=m['content'])
        db.session.add(article)
    db.session.commit()
    click.echo('数据导入完成')


# 生成admin账号的函数
@app.cli.command()
@click.option('--username', prompt=True, help="用来登录的用户名")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="用来登录的密码")
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username, name="陈亚飞")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('创建管理员账号完成')
