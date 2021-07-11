# !!! still in development

# ustc-new-grade-actions
USTC 新成绩自动通知脚本，使用 GitHub Actions 实现云端自动运行。

# 参考
查分的 Python 代码实现基于 [ustc-new-grade-auto-notification by Sinon02](https://github.com/Sinon02/ustc-new-grade-auto-notification)。

# 说明 & privacy
本仓库尚未准备向外发布（主要自用）。repo 内含有与用户信息相关的数据文件，假如 fork 请留意。

# fork 自用方法
假如您想 fork 本仓库以便自己使用，请确保您 fork 后完成以下步骤：

- 修改 `config.py`，把邮件收信人改掉（最后一行）
- 在仓库设置中，加入以下 Secrets：`CAS_USERNAME`, `CAS_PASSWD`, `MAIL_HOST`, `MAIL_SENDER`, `MAIL_PASSWD`。其中`CAS`开头的是统一认证系统的账号密码，`MAIL`开头的是发送邮件的若干配置。
- 确保 Actions 被启用
- 将仓库 clone 到本地，执行`git commit -m 'sync' --allow-empty`来创建一个空的 commit，然后 push 回去。这会触发脚本进行**sync**操作，登录教务系统进行一次信息同步。
- 观察 Actions 执行记录，看是否能够运行成功
