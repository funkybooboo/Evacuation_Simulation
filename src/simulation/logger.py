import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger


"""
    def logging(self, person):
        log_directory = f'../../../logs/run{self.simulation_count}/people/person'
        os.makedirs(log_directory, exist_ok=True)

        self.logger.setLevel(logging.INFO)

        log_file = f'{log_directory}/{self.pk}.log'
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)

        self.logger.addHandler(f_handler)

        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(formatter)
        self.logger.addHandler(c_handler)

    def log_person_statistics(self, person, message):
        self.logger.info(message)

    sim_logger = Person(simulation_count=1, pk=123)
    sim_logger.log_person_statistics("This is a test log message.")

        # logging.basicConfig(filename=f'../../../logs/run{simulation_count}/people/person{pk}.log', level=logging.INFO,
                           # format='%(asctime)s - %(levelname)s - %(message)s')
    """