from djchoices import DjangoChoices, ChoiceItem


class AWSRegionChoice(DjangoChoices):
    US_East_NV = ChoiceItem('us-east-1', label="US East (N. Virginia)")
    US_East_OH = ChoiceItem('us-east-2', label="US East (Ohio)")
    US_West_NCAL = ChoiceItem('us-west-1', label="US West (N. California)")
    US_West_OR = ChoiceItem('us-west-2', label="US West (Oregon)")
    AP_Mumbai = ChoiceItem('ap-south-1', label="Asia Pacific (Mumbai)")
    AP_Seoul = ChoiceItem('ap-northeast-2', label="Asia Pacific (Seoul)")
    AP_Singapore = ChoiceItem('ap-southeast-1', label="Asia Pacific (Singapore)")
    AP_Sydney = ChoiceItem('ap-southeast-2', label="Asia Pacific (Sydney)")
    AP_Tokyo = ChoiceItem('ap-northeast-1', label="Asia Pacific (Tokyo)")
    EU_Frankfurt = ChoiceItem('eu-central-1', label="EU (Frankfurt)")
    EU_Ireland = ChoiceItem('eu-west-1', label="EU (Ireland)")
    EU_London = ChoiceItem('eu-west-2', label="EU (London)")
    EU_Paris = ChoiceItem('eu-west-3', label="EU (Paris)")
    SA_SaoPaolo = ChoiceItem('sa-east-1', label="Sout America (São Paolo)")


class AWSSecurityGroupRuleType(DjangoChoices):
    INGRESS = ChoiceItem(0, label="ingress")
    EGRESS = ChoiceItem(1, label="egress")


class IPProtocol(DjangoChoices):
    ALL = ChoiceItem('-1', label="all")
    ICMPv4 = ChoiceItem('icmp', label="ICMPv4")
    ICMPv6 = ChoiceItem('icmpv6', label="ICMPv6")
    TCP = ChoiceItem('tcp', label="TCP")
    UDP = ChoiceItem('udp', label="UDP")
