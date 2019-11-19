import logging
import re
from crmsh import utils, parallax


def get_online_nodes():
    _, out = utils.get_stdout('crm_node -l')
    if out:
        return re.findall(r'[0-9]+ (.*) member', out)
    else:
        return None


def before_tag(context, tag):
    context.logger = logging.getLogger("test.{}".format(tag))
    # tag @clean means need to stop cluster service
    if tag == "clean":
        online_nodes = get_online_nodes()
        if online_nodes:
            try:
                parallax.parallax_call(online_nodes, 'crm cluster stop')
            except ValueError as err:
                context.logger.error("{}\n".format(err))
                context.failed = True