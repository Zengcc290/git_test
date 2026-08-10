# 从 CLI 模块导入真正的命令行处理函数。
from .cli import main


# 只有使用 ``python -m knowledge_search`` 运行包时，才执行 CLI。
if __name__ == "__main__":
    # 将 main 返回的状态码交给操作系统，方便脚本判断命令是否成功。
    raise SystemExit(main())
