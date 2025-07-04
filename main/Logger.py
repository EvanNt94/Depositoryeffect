import logging 
class Logger:
  def __init__(self, name):
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] [%(module)s.%(funcName)s] [%(lineno)d] %(message)s"
    )
    self.logger = logging.getLogger(__name__)
