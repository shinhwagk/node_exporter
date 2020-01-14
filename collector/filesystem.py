import re
import os

from prometheus_client.core import GaugeMetricFamily

from collector.namespace import NAMESPACE
from collector.collector import Collector


defIgnoredMountPoints = "^/(dev|proc|sys|var/lib/docker/.+)($|/)"
defIgnoredFSTypes = "^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|iso9660|mqueue|nsfs|overlay|proc|procfs|pstore|rpc_pipefs|securityfs|selinuxfs|squashfs|sysfs|tracefs)$"


def parseFilesystemLabels(fslines):
    lines = map(lambda l: l.split(' '), fslines)
    lines = filter(lambda l: re.match(
        defIgnoredFSTypes, l[0]) is None, lines)
    lines = filter(lambda l: re.match(
        defIgnoredMountPoints, l[1]) is None, lines)
    return list(map(lambda l: {"device": l[0], "mountPoint": l[1],
                               "fsType": l[2], "options": l[3]}, lines))


def generateFilesystemMetic(name, subsystem, documentation, labels, value):
    g = GaugeMetricFamily(name="{}_{}_{}".format(NAMESPACE, name, subsystem),
                          documentation=documentation, labels=["device", "mountpoint", "fstype"])
    g.add_metric([labels["device"], labels["mountPoint"],
                  labels["fsType"]], float(value))
    return g


class FilesystemCollector(Collector):
    name = 'filesystem'

    def collect(self):
        with open('/proc/1/mounts', 'r') as f:
            for l in parseFilesystemLabels(f.readlines()):
                st = os.statvfs(l["mountPoint"])
                yield generateFilesystemMetic('size_bytes', self.name, '',
                                              l, st.f_bsize * st.f_blocks)
                yield generateFilesystemMetic('free_bytes', self.name, '',
                                              l, st.f_bfree * st.f_blocks)
                yield generateFilesystemMetic('avail_bytes', self.name, '',
                                              l, st.f_bsize * st.f_blocks)
                yield generateFilesystemMetic('files', self.name, '',
                                              l, st.f_files)
                yield generateFilesystemMetic('files_free', self.name, '',
                                              l,  st.f_files * st.f_ffree)
