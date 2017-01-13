import logging
import os

import onedrivesdk.error

from .update_mtime import UpdateTimestampTask as _UpdateTimestampTask
from ..od_api_helper import item_request_call


class UploadFileTask(_UpdateTimestampTask):

    def __init__(self, repo, task_pool, parent_dir_request, parent_relpath, item_name):
        """
        :param onedrived.od_repo.OneDriveLocalRepository repo:
        :param onedrived.od_task.TaskPool task_pool:
        :param onedrivesdk.request.item_request_builder.ItemRequestBuilder parent_dir_request:
        :param str parent_relpath:
        :param str item_name:
        """
        super().__init__(repo, task_pool, parent_relpath, item_name)
        self.parent_dir_request = parent_dir_request

    def __repr__(self):
        return type(self).__name__ + '(%s)' % self.local_abspath

    def handle(self):
        logging.info('Uploading file "%s" to OneDrive.', self.local_abspath)
        try:
            item_stat = os.stat(self.local_abspath)
            returned_item = item_request_call(
                self.repo, self.parent_dir_request.children[self.item_name].upload, self.local_abspath)
            self.update_timestamp_and_record(returned_item, item_stat)
            logging.info('Finished uploading file "%s".', self.local_abspath)
            return True
        except (onedrivesdk.error.OneDriveError, OSError) as e:
            logging.error('Error uploading file "%s": %s.', self.local_abspath, e)
            return False
