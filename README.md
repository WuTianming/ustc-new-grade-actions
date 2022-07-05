20220705可用。

# ustc-new-grade-actions
USTC 新成绩自动通知脚本，使用 GitHub Actions 实现云端自动运行。

# 参考
查分的 Python 代码实现基于 [ustc-new-grade-auto-notification by Sinon02](https://github.com/Sinon02/ustc-new-grade-auto-notification)。

# 说明 & privacy
默认使用qq邮箱和科大邮箱收信，若使用其他邮箱可自行修改。

# fork 自用方法
[@Alpha-Girl](https://github.com/Alpha-Girl) 同学做了一个视频来具体讲解以下步骤，[传送门](https://www.bilibili.com/video/BV1Zf4y1G7C6)

假如您想 fork 本仓库以便自己使用，请确保您 fork 后完成以下步骤：

- 修改 `config.py`，把邮件收信人改掉（最后一行）
- 在仓库设置中，加入以下 Secrets：`CAS_USERNAME`, `CAS_PASSWD`, `MAIL_HOST`, `MAIL_SENDER`, `MAIL_PASSWD`, `MAIL_QQ`, `MAIL_USTC`。其中`CAS`开头的是统一认证系统的账号密码，`MAIL`开头的是发送邮件的若干配置。
- 确保 Actions 被启用
- 将仓库 clone 到本地，执行`git commit -m 'sync' --allow-empty`来创建一个空的 commit，然后 push 回去。这会触发脚本进行**sync**操作，登录教务系统进行一次信息同步。
- 观察 Actions 执行记录，看是否能够运行成功。经过第一次**sync**之后，以后会自动根据 crontab 的设置定时运行。

注：由于某些众所周知的原因，QQ邮箱不能直接用密码登陆，而需单独生成授权码；觉得太麻烦就直接用科大邮箱比较好。
