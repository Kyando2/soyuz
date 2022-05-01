command!(c, g, "create_channel", "propose to create a channel", legacy=false, options=Options(
    [String, "name", "the name of the channel"]
)) do ctx, name::String 
    global c, votemap
    create_vote(CreateChannelVoteAction(name))
    Ekztazy.reply(c, ctx, content="Succesfully created vote proposal.")
end