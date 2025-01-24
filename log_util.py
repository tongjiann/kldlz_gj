import logging
import os


class Logger:
    def __init__(self, name="Logger", log_level=logging.DEBUG, log_file="app.log"):
        """
        初始化日志记录器。

        :param name: 日志记录器名称
        :param log_level: 日志级别（默认为 DEBUG）
        :param log_file: 日志文件路径（如果为 None，则不输出到文件）
        """
        # 创建一个日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)  # 设置日志级别

        # 创建日志输出格式
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 创建控制台输出处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 如果指定了日志文件，则创建文件输出处理器
        if log_file:
            # 确保日志文件目录存在
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """输出DEBUG级别的日志"""
        self.logger.debug(message)

    def info(self, message):
        """输出INFO级别的日志"""
        self.logger.info(message)

    def warn(self, message):
        """输出WARN级别的日志"""
        self.logger.warning(message)

    def error(self, message):
        """输出ERROR级别的日志"""
        self.logger.error(message)


# 全局单例日志对象
log = None


def get_logger(log_file=None, log_level=logging.INFO):
    """
    获取全局单例日志对象。

    :param log_file: 日志文件路径（如果为 None，则不输出到文件）
    :param log_level: 日志级别（默认为 DEBUG）
    :return: Logger 实例
    """
    global log
    if log is None:
        log = Logger(log_level=log_level)
    return log


# 示例用法
if __name__ == "__main__":
    logger = get_logger(log_file="app.log", log_level=logging.INFO)
    logger.debug("这是一条DEBUG日志")  # 不会输出，因为日志级别是 INFO
    logger.info("这是一条INFO日志")
    logger.warn("这是一条WARN日志")
    logger.error("这是一条ERROR日志")
