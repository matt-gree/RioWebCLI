# RioWeb Community Manager
## Use
Download the code, rename [TEMPLATE_rio_key.json](TEMPLATE_rio_key.json) to just rio_key.json and input your Rio Key to the field. Run the functions you want to in main.py

## Known RioWeb Limitations

There is currently no way to see all of the communites a user sponsors

Email invites are not active, thus atm I don't think its possible to add users to communities

Community members returned only have IDs, not usernames

## Definition of Tags 
Tags can be of four types: Community, Competition, Component, or Gecko Code. All tags, gecko code or not, are tied to a community, with the intention of tracking who created it. Originally, Gecko Code Tags were only intended to be added under the ProjectRio community ("comm_ID": 1) to restrict who could add them so we could be sure they worked and avoid issues for bad tag codes. However, now ProjectRio allows people to add custom gecko code tags to their own communities with the understanding that they won't help debug non official gecko code tags. Tags from one community can be used in any TagSet to, for example, allow someone to watch a stream and make their own TagSets with the same rules without remaking tags for the same rules.