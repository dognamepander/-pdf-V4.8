# -扫描版pdf空白定位器-V4.8

扫描版pdf空白定位器，扫描版pdf和原非扫描pdf建立一一对应的关系，然后检查方框中和横线上方是否是空白，还有括号是否是空白。如果存在这种情况，需用例执行人员重新核对。

其试用于如下情况检测：
![1](https://github.com/dognamepander/-pdf-V4.8/assets/119275007/0a001358-1107-442d-abf0-a8c9d15f051a)
![2](https://github.com/dognamepander/-pdf-V4.8/assets/119275007/9808ac82-6c35-4eea-a013-e8c5eb6382c9)

软件设计思路，建立扫描版pdf和原非扫描pdf建立一一对应的关系，然后检查方框中部和横线上方是否是空白，还有括号是否是空白。

![QQ浏览器截图20240528151934](https://github.com/dognamepander/-pdf-V4.8/assets/119275007/9a3195ed-6d60-4393-8f74-3cc3e4ea20e3)

软件设计思路补充，平移和旋转在校正扫描pdf时太慢，推键使用过仿射变化，其关键在于找到合适的四角边框，可以使用到轮廓检测和膨胀腐蚀等操作。

![QQ浏览器截图20240528153414](https://github.com/dognamepander/-pdf-V4.8/assets/119275007/53349537-9ee3-4a75-be1e-692b066b6c29)
