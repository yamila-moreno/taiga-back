# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This makes all code that import services works and
# is not the baddest practice ;)

from .bulk_update_order import bulk_update_severity_order
from .bulk_update_order import bulk_update_priority_order
from .bulk_update_order import bulk_update_issue_type_order
from .bulk_update_order import bulk_update_issue_status_order
from .bulk_update_order import bulk_update_task_status_order
from .bulk_update_order import bulk_update_points_order
from .bulk_update_order import bulk_update_userstory_status_order

from .filters import get_all_tags
from .filters import get_issues_filters_data

from .stats import get_stats_for_project_issues
from .stats import get_stats_for_project
