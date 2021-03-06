import logging
import json
import humanize

from wpamod.plugins.base.analysis_plugin import AnalysisPlugin


class PSUtilSummary(AnalysisPlugin):
    def analyze(self):
        """
        Show a summary of memory usage for python processes
        """
        output = []

        input_files = self.get_input_files('*.psutil')
        if len(input_files) == 0:
            return []

        for i, input_file in enumerate(input_files):
            try:
                psutil_data = json.loads(file(input_file).read())
            except:
                logging.debug('Failed to load JSON from %s' % input_file)
            else:
                self._process_psutil_memory_data(i, psutil_data, output)

        return output

    def _process_psutil_memory_data(self, count, psutil_data, output):
        """
        :param psutil_data: A dict containing the data
        :param output: A list with our parsed output
        :return: None
        """
        processes = psutil_data['Processes']
        memory_usage = []

        for pid, data in processes.iteritems():
            if self._is_w3af(data):
                target = self._get_process_target(pid)
                pid_target = '%s - %s' % (pid, target)

                usage = float(data['memory_percent'])
                usage = '%0.2f %%' % usage

                shared = humanize.naturalsize(data['memory_info_ex']['shared'])
                rss = humanize.naturalsize(data['memory_info_ex']['rss'])

                process_data = [('rss', rss),
                                ('shared', shared),
                                ('Percent OS used', usage)]

                memory_usage.append((pid_target, process_data))

        for key, value in psutil_data['ps_mem'][0].items():
            try:
                psutil_data['ps_mem'][0][key] = humanize.naturalsize(value * 1024)
            except:
                continue

        memory_usage.append(('Program memory by psmem',
                             psutil_data['ps_mem'][0].items()))

        output.append(('Measurement #%s' % count, memory_usage))

    def _get_process_target(self, pid):
        input_files = self.get_input_files('*.processes')
        for input_file in input_files:
            try:
                process_data = json.loads(file(input_file).read())
            except:
                logging.debug('Failed to load JSON from %s' % input_file)
            else:
                if pid in process_data:
                    return process_data[pid]['name'] + '.' + process_data[pid]['target']

        return '(unknown)'

    def _is_w3af(self, data):
        if data['exe'] is None:
            return False

        return 'python' in data['exe']

    def get_output_name(self):
        return 'PSUtils memory usage summary'
