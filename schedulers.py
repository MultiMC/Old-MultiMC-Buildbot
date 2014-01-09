####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.

from buildbot.schedulers.basic import SingleBranchScheduler, AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes import filter

# If true, automatically build every commit.
buildOnCommit = True

def rc_branch_filter(branch):
    return branch.startswith("release-")

def get_schedulers(builder_names):
    schedulers = []

    schedulers.append(ForceScheduler(
        name="force",
        builderNames=[name for key, blist in builder_names.iteritems() for name in blist]))

    if buildOnCommit:
        schedulers.append(SingleBranchScheduler(
            name="stable",
            change_filter=filter.ChangeFilter(branch='master'),
            treeStableTimer=30,
            builderNames=builder_names["stable"]))

        schedulers.append(SingleBranchScheduler(
            name="develop",
            change_filter=filter.ChangeFilter(branch='develop'),
            treeStableTimer=30,
            builderNames=builder_names["develop"]))

        schedulers.append(AnyBranchScheduler(
            name="release-candidate",
            change_filter=filter.ChangeFilter(branch_fn=rc_branch_filter),
            treeStableTimer=30,
            builderNames=builder_names["rc"]))

        return schedulers

