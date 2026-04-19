TarDAL-Poss 项目说明
========================================

一、本项目在解决什么痛点
------------------------
1. 红外与可见光图像融合（TarDAL 等算法）多在命令行或脚本环境运行，评委现场往往不便配置 Python、CUDA、依赖库与前后端分离部署，难以快速、一致地体验效果。
2. 教学与竞赛评审需要「可演示、可复现、可比对」的交付物：同一套源码应能编译出与约定一致的 Windows 可运行目录，避免因环境差异导致「能跑 / 不能跑」争议。
3. 本仓库将 TarDAL 融合流水线封装为 Flask API，并用 Vue（Vite）提供网页上传与结果查看；通过 PyInstaller 将算法、配置、前端静态资源打进单一后端可执行程序目录，实现「编译完成后在 dist 目录直接运行」，运行机无需单独安装 Node.js 或配置前后端两个服务。

二、主要创新点 / 工程亮点（概要）
------------------------------
1. 算法层：基于 TarDAL 融合管线（config / pipeline / module 等），在本地或打包环境中加载权重完成红外–可见光融合及关联流程。
2. 交付形态：PyInstaller 规格文件 tardal_backend.spec 将 backend、算法模块、frontend/dist 静态资源一并收集；运行时可由同一 Flask 进程托管前端（/TarDAL-Poss/）与 API，适合「单 exe + 浏览器」演示。
3. 构建自动化：提供 scripts 下的 bat 与 PowerShell 脚本，串联前端构建（按需）、PyInstaller、以及将 readme.txt、评委说明、RUN.bat、示例图等复制到 dist\TarDAL-Poss-Backend，编译结果即最终可运行目录。

三、评委老师如何根据文档编译并运行？（Windows）
----------------------------------------------------
在已安装必要开发工具的 Windows 电脑上，于**项目根目录**完成构建后，**直接在本机 dist\TarDAL-Poss-Backend\** 中运行程序即可（无需再执行任何打 zip 脚本）。

【环境前提】
- 已安装 Python 3（建议与团队开发版本一致），并将 python / pip 加入 PATH。
- 构建时需能执行 pip install -r requirements.txt；PyInstaller 由脚本按需安装。
- 若仓库中尚无 frontend\dist\index.html，需安装 Node.js（含 npm），以便脚本执行 npm install 与 npm run build。若已有构建好的 frontend\dist，脚本默认跳过 npm（除非设置强制重建，见下）。
- 磁盘空间充足；首次 PyInstaller 打包耗时较长属正常现象。
- 离线运行：构建前必须在 weights\v1\ 下放置 tardal-dt.pth 与 mask-u2.pth（与 TarDAL 官方 Release 一致）；构建脚本与 tardal_backend.spec 会校验；生成后的 exe 运行时不再联网下载模型。

【推荐命令（项目根目录）】

  双击或在命令行执行其一即可：
    scripts\build_backend_exe.bat
    或 PowerShell：.\scripts\Build-BackendExe.ps1

  脚本将依次：按需 npm install / npm run build；安装依赖与 PyInstaller；执行 pyinstaller tardal_backend.spec；再调用 scripts\Copy-PictureExampleToDist.ps1，把根目录 readme.txt、packaging\judge 下的 RUN.bat 与 评委说明.txt、以及合并后的 Picture-Example 复制到 dist\TarDAL-Poss-Backend\。

【编译完成后如何运行】
- 进入目录：**项目根目录\dist\TarDAL-Poss-Backend\**
- 双击 **TarDAL-Poss-Backend.exe**，或 **RUN.bat**（效果相同）。
- 浏览器访问：**http://127.0.0.1:5000/TarDAL-Poss/**（详见同目录 **评委说明.txt**）。
- 同目录下 **Picture-Example** 为示例图，可拖入网页测试。

【与脚本相关的其他 bat（开发调试用）】
- scripts\start-backend.bat：从源码启动 Flask 后端。
- scripts\start-frontend.bat：启动 Vite 前端开发服务器（需先有 frontend\node_modules）。
- scripts\clean_cache.bat：清理缓存与中间产物。逻辑在 scripts\clean_cache.ps1，也可执行 .\scripts\clean_cache.ps1 或 -Full。

【清理后如何重新编译】
清理不会改变 requirements.txt 与 tardal_backend.spec。重新执行上文构建脚本即可；若缺少 frontend\dist，会自动 npm install / build 后再 PyInstaller。

四、文档与目录索引
------------------
- 根目录 readme.txt：本说明；构建时复制到 dist\TarDAL-Poss-Backend\readme.txt。
- packaging\judge\评委说明.txt：运行步骤与浏览器地址；构建时复制到 dist 内。
- packaging\judge\readme.txt：packaging\judge 目录说明。
- packaging\judge\Picture-Example\readme.txt：示例图模板与合并逻辑说明。
- Picture-Example\readme.txt：项目根目录示例图像（案例 1～4）说明。
- weights\v1\readme.txt：离线构建所需权重文件名说明。
