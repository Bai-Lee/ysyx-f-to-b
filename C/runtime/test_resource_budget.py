"""Small real-child controls; never allocate GiBs merely to test a policy."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import budget_exec
from resource_policy import generation_environment, load_policy


class ResourceBudgetTests(unittest.TestCase):
    def test_active_policy_and_heap_override(self):
        policy = load_policy()
        self.assertEqual(policy['process_group_limit_mib'], 6144)
        original = {'MILL_JVM_OPTS': '-Xmx2g -XX:ActiveProcessorCount=2',
                    'JAVA_TOOL_OPTIONS': '-Xmx2g -Djavax.net.ssl.trustStore=kept'}
        result = generation_environment(original)
        self.assertEqual(result['MILL_JVM_OPTS'], '-Xmx4096m -XX:ActiveProcessorCount=2')
        self.assertIn('trustStore=kept', result['JAVA_TOOL_OPTIONS'])
        self.assertIn('-Xmx2g', original['MILL_JVM_OPTS'])

    def test_startup_headroom_blocks_child(self):
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / 'budget.json'
            args = ['budget_exec', '--report', str(report), '--', sys.executable, '-c', 'pass']
            with patch.object(sys, 'argv', args), patch.object(budget_exec, 'windows_available_bytes', return_value=1024**3), patch.object(budget_exec.subprocess, 'Popen') as spawn:
                self.assertEqual(budget_exec.main(), 125)
                spawn.assert_not_called()
            self.assertEqual(json.loads(report.read_text())['reason'], 'WINDOWS_START_HEADROOM')

    def test_positive_and_over_budget_real_child(self):
        with tempfile.TemporaryDirectory() as temp:
            for name, limit, size, expected in [('positive', 128, 32, 0), ('over-budget', 32, 80, 125)]:
                report = Path(temp) / (name + '.json')
                command = [sys.executable, str(Path(budget_exec.__file__)), '--rss-mib', str(limit),
                           '--report', str(report), '--', sys.executable, '-c',
                           f'import time; a=bytearray({size}*1024**2); time.sleep(2.5)']
                result = subprocess.run(command, timeout=30, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                data = json.loads(report.read_text())
                self.assertEqual(data['policy']['process_group_limit_mib'], 6144)
                self.assertGreater(data['peak_group_pss_bytes'], size * 1024**2)
                self.assertEqual(data['status'], 'PASS' if expected == 0 else 'RESOURCE_LIMIT')
                if expected:
                    self.assertEqual(data['reason'], 'PROCESS_GROUP_MEMORY')


if __name__ == '__main__':
    unittest.main(verbosity=2)
