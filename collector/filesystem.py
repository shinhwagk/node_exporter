import re
import os

from prometheus_client.core import GaugeMetricFamily

from collector.namespace import NAMESPACE
import random

defIgnoredMountPoints = "^/(dev|proc|sys|var/lib/docker/.+)($|/)"
defIgnoredFSTypes = "^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|iso9660|mqueue|nsfs|overlay|proc|procfs|pstore|rpc_pipefs|securityfs|selinuxfs|squashfs|sysfs|tracefs)$"

subsystem = "filesystem"

filesystemMountPath = '/proc/1/mounts'


def filesystemLines(fspath):
    with open(fspath, 'r') as f:
        return f.readlines()


def parseFilesystemLabels(fslines):
    lines = map(lambda l: l.split(' '), fslines)
    lines = filter(lambda l: re.match(
        defIgnoredFSTypes, l[0]) is None, lines)
    lines = filter(lambda l: re.match(
        defIgnoredMountPoints, l[1]) is None, lines)
    return list(map(lambda l: {"device": l[0], "mountPoint": l[1],
                               "fsType": l[2], "options": l[3]}, lines))


class FilesystemCollectorTest(Gauge):
    def __init__(self):
        print(1)


class FilesystemCollector(object):
    def __init__(self):
        self.g1 = GaugeMetricFamily(name='size_bytes', subsystem=subsystem, namespace=NAMESPACE,
                                    documentation='Filesystem size in bytes.', labelnames=["device", "mountpoint", "fstype"])
        self.g2 = GaugeMetricFamily(name='free_bytes', subsystem=subsystem, namespace=NAMESPACE,
                                    documentation='Filesystem size in bytes.', labelnames=["device", "mountpoint", "fstype"])
        self.g3 = GaugeMetricFamily(name='avail_bytes', subsystem=subsystem, namespace=NAMESPACE,
                                    documentation='Filesystem size in bytes.', labelnames=["device", "mountpoint", "fstype"])
        self.g4 = GaugeMetricFamily(name='files', subsystem=subsystem, namespace=NAMESPACE,
                                    documentation='Filesystem size in bytes.', labelnames=["device", "mountpoint", "fstype"])
        self.g5 = GaugeMetricFamily(name='files_free', subsystem=subsystem, namespace=NAMESPACE,
                                    documentation='Filesystem size in bytes.', labelnames=["device", "mountpoint", "fstype"])

    def collect(self):
        for l in parseFilesystemLabels(filesystemLines(filesystemMountPath)):
            st = os.statvfs(l["mountPoint"])
            self.g1.labels(l["device"], l["mountPoint"],
                           l["fsType"]).set(st.f_bsize * st.f_blocks)
            self.g2.labels(l["device"], l["mountPoint"],
                           l["fsType"]).set(st.f_bfree * st.f_blocks)
            self.g4.labels(l["device"], l["mountPoint"],
                           l["fsType"]).set(st.f_files)
            self.g5.labels(l["device"], l["mountPoint"],
                           l["fsType"]).set(random.random())
            self.g5.type = self.g5._type
            self.g5.name = self.g5._name

        yield self.g5
