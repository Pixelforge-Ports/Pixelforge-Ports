import unittest
from game_requirements import game_requirements


class Requirements(unittest.TestCase):
    def test_game_version_is_distinct_from_port_release(self):
        result = game_requirements('# Release 1.0.1\n## Get ashworld.dat from GOG\nDownload the supported build (1.8.1b).\n## Controls\nA: jump')
        self.assertEqual(result['windows_version'], '1.8.1b')
        self.assertNotIn('Controls', result['instructions'])

    def test_undocumented_version_is_not_guessed(self):
        result = game_requirements('# Release 1.0.1\n## Get gunslugs2.jar from GOG\nUse the supported build (fingerprint listed below).')
        self.assertIsNone(result['windows_version'])

    def test_windows_line_endings_and_game_edition(self):
        result = game_requirements('## Get meganoid.dat from GOG\r\nUse the supported build (2.2.3, 2017 game).\r\n')
        self.assertEqual(result['windows_version'], '2.2.3')

    def test_missing_section(self):
        self.assertEqual(game_requirements('# Release 1.0.1')['instructions'], '')

    def test_residual_installer_version(self):
        result = game_requirements('## Get residual.jar from GOG\nDownload the **Windows offline backup installer for version 1.4.1**.')
        self.assertEqual(result['windows_version'], '1.4.1')

    def test_android_is_not_a_windows_installer(self):
        result = game_requirements('## Get the APK\nThis port requires **Gunslugs 3.2.4**.')
        self.assertEqual(result['platform'], 'Android')
        self.assertEqual(result['game_version'], '3.2.4')
        self.assertIsNone(result['windows_version'])
