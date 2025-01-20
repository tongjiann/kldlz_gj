import logging


class Logger:
    def __init__(self, name="Logger"):
        # 创建一个日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # 默认设置日志级别为 DEBUG

        # 创建控制台输出处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # 输出级别为 DEBUG

        # 创建日志输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)

        # 添加控制台输出处理器到日志记录器
        self.logger.addHandler(console_handler)

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
