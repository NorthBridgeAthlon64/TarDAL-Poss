本文件夹作用
----------
存放随 **dist\TarDAL-Poss-Backend** 一起交付的辅助文件：启动脚本、评委简明说明、示例图目录模板。构建脚本在完成 PyInstaller 后会通过 **scripts\Copy-PictureExampleToDist.ps1** 将本目录中的 **RUN.bat**、**评委说明.txt** 复制到 dist 内，并与根目录 readme.txt、Picture-Example 合并结果放在 **exe 同目录**。

各文件说明
----------
评委说明.txt
  编译完成后在 dist 目录中运行程序的简明步骤（浏览器地址、拖图测试、杀毒提示等）；模型已内置，无需联网下载。

RUN.bat
  切换到当前目录并启动 TarDAL-Poss-Backend.exe。

Picture-Example\
  示例图模板目录；与项目根目录 Picture-Example 合并后进入 dist。

readme.txt
  本文件，说明 packaging\judge 目录用途。
