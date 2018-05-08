from enumfields import Enum


class ClusterType(Enum):
    ESX = 1
    JUNIPER = 2
    SOLR = 3
    KAFKA = 4
    ELASTICSEARCH = 5
    MONGODB = 6
    CASSANDRA = 7
    PRISM = 8
    SQL = 9

    class Labels:
        ESX = 'VMWare ESXi'
        JUNIPER = 'JunOS'
        SOLR = 'SolrCloud'
        KAFKA = 'Kafka'
        ELASTICSEARCH = 'elasticsearch'
        MONGODB = 'MongoDB'
        CASSANDRA = 'Cassandra'
        PRISM = 'Nutanix PRISM'
        SQL = 'SQL'


class OperatingSystem(Enum):
    UBUNTU = 1
    CENTOS = 2
    WINDOWS = 3
    MAC_OS = 4
    JUNOS = 5
    ESX = 6
    OTHER = 7

    class Labels:
        UBUNTU = 'ubuntu'
        CENTOS = 'CentOS'
        WINDOWS = 'Windows'
        MAC_OS = 'Mac OS'
        JUNOS = 'JunOS'
        ESX = 'VMWare ESXi'
        OTHER = 'other'
