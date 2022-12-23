"""
Helper functions to launch the benchmark and the optimizer from the command line.
"""

import logging
import argparse

from mlos_bench.environment import LocalExecService, ConfigPersistenceService

_LOG_LEVEL = logging.INFO
_LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d %(funcName)s %(levelname)s %(message)s'
logging.basicConfig(level=_LOG_LEVEL, format=_LOG_FORMAT)

_LOG = logging.getLogger(__name__)


class Launcher:
    """
    Common parts of the OS Autotune command line launcher.
    """

    def __init__(self, description='OS Autotune launcher'):

        _LOG.info("Launch: %s", description)

        self._config_loader = None
        self._env_config_file = None
        self._global_config = {}
        self._parser = argparse.ArgumentParser(description=description)

        self._parser.add_argument(
            '--log', required=False, dest='log_file',
            help='Path to the log file. Use stdout if omitted.')

        self._parser.add_argument(
            '--log-level', required=False, type=int, default=_LOG_LEVEL,
            help=f'Logging level. Default is {_LOG_LEVEL} ({logging.getLevelName(_LOG_LEVEL)}).' +
                 f' Set to {logging.DEBUG} for debug, {logging.WARNING} for warnings only.')

        self._parser.add_argument(
            '--config', required=True,
            help='Path to JSON file with the configuration'
                 ' of the benchmarking environment')

        self._parser.add_argument(
            '--config-path', nargs="+", required=False,
            help='Locations of JSON config files.')

        self._parser.add_argument(
            '--global', required=False, dest='global_config',
            help='Path to JSON file that contains additional (sensitive)'
                 ' parameters of the benchmarking environment')

    @property
    def parser(self):
        """
        Get the command line parser (so we can add more arguments to it).
        """
        return self._parser

    def parse_args(self):
        """
        Parse command line arguments and load global config parameters.
        """
        (args, args_rest) = self._parser.parse_known_args()

        logging.root.setLevel(args.log_level)
        if args.log_file:
            log_handler = logging.FileHandler(args.log_file)
            log_handler.setLevel(args.log_level)
            log_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
            logging.root.addHandler(log_handler)

        self._env_config_file = args.config
        self._config_loader = ConfigPersistenceService({"config_path": args.config_path})

        if args.global_config is not None:
            self._global_config = self._config_loader.load_config(args.global_config)

        self._global_config.update(Launcher._try_parse_extra_args(args_rest))
        if args.config_path:
            self._global_config["config_path"] = args.config_path

        return args

    @staticmethod
    def _try_parse_extra_args(cmdline):
        """
        Helper function to parse global key/value pairs from the command line.
        """
        _LOG.debug("Extra args: %s", cmdline)

        config = {}
        key = None
        for elem in cmdline:
            if elem.startswith("--"):
                if key is not None:
                    raise ValueError("Command line argument has no value: " + key)
                key = elem[2:]
                kv_split = key.split("=", 1)
                if len(kv_split) == 2:
                    config[kv_split[0].strip()] = kv_split[1]
                    key = None
            else:
                if key is None:
                    raise ValueError("Command line argument has no key: " + elem)
                config[key.strip()] = elem
                key = None

        if key is not None:
            raise ValueError("Command line argument has no value: " + key)

        _LOG.debug("Parsed config: %s", config)
        return config

    def load_config(self, json_file_name: str) -> dict:
        """
        Load JSON config file. Use path relative to `config_path` if required.
        """
        assert self._config_loader is not None, "Call after invoking .parse_args()"
        return self._config_loader.load_config(json_file_name)

    def load_env(self):
        """
        Create a new benchmarking environment from the configs and command line parameters.
        Inject the persistence service so that the environment can load other configs.
        """
        return self._config_loader.load_environment(
            self._env_config_file, self._global_config,
            service=LocalExecService(parent=self._config_loader))