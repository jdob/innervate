# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import os
import unittest

from innervate.config import InnervateConfig
from innervate.engine import InnervateEngine


class BaseFunctionalTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()

        self.engine = build_engine()

        # Shortcut variables
        self.config = self.engine.config
        self.user = self.engine.user_manager.user('user1')

        # Sanity check for a clean environment before each test
        self.assert_no_projects()

    def tearDown(self):
        super(BaseFunctionalTestCase, self).tearDown()

        all_projects = self.user.api.projects.list()
        for p in all_projects:
            self.user.api.projects.delete(p.name)

    def scenario(self, name):
        return self.engine.scenario_manager.scenario_by_name(name)

    def assert_no_projects(self):
        self.assert_projects_count(0)

    def assert_projects_count(self, count):
        all_projects = self.user.api.projects.list()
        self.assertEqual(count, len(all_projects))


def build_engine():
    """Creates and initializes an engine.

    This can be used as the basis for functional tests or be imported
    inside of a console and used directly to run scenarios.
    """

    # Load and initialize the configuration based on the example.yaml
    # This may need to be an explicit testing config in the future, but
    # for now it works until it doesn't
    config = InnervateConfig()
    config.load(example_config_filename())

    # Create and initialize an engine but don't start the loop; it
    # will be used to get to the configured pieces we need
    engine = InnervateEngine(config)
    engine.initialize()

    return engine


def example_config_filename():
    x = os.path.dirname(os.path.abspath(__file__))
    ex = os.path.join(os.path.split(x)[0], 'config', 'example.yaml')
    return ex
