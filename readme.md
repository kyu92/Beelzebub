# 关于Beelzebub
> Beelzebub是用python编写的一键填报台州科技职业学院企业微信健康数据表格的脚本，填写完基本信息后仅需运行脚本即可实现每日的数据申报

* 申报数据的时间：
  * 默认是当前程序运行的时间戳

* 使用方式：
  * 修改resources/data.json文件的xh和mobile两项即可，分别对应学号和手机号
  * 若需要放到服务器上自动运行，请将circulate项设置为true,并修改submit_on为指定提交时间  
  *如果使用循环提交模式，submit_on必须设置时间格式，13:00表示下午1点整提交*

# 文件结构
> root  
>> resources: 资源相关文件  
>>> data.json 用户数据即相关配置文件  

>> dist: 打包完成的exe文件  
>> logical.py python脚本  


# 更新日志：
* 2020.6.21: 修改主逻辑代码，重置标记方式改为隔日清除，修复运行当天重复提交的问题，reset_flag函数改用线程调用
* 2020.6.23: 修改主逻辑代码，将UUID的生成放到主逻辑函数中，修复隔日提交失败的问题  
* 2020.6.23: 修改主逻辑代码，提交的数据改为可自定义内容  
    **循环模式修改完数据需要重启程序*  
    **需要修改数据请自行抓取对应的表单内容填到data选项里*
* 2020.6.23: 修改循环逻辑，循环检查提交时间改为可自定义