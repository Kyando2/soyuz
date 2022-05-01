command!(c, g, "create_text_channel", "propose to create a text channel", legacy=false, options=Options(
    [String, "name", "the name of the channel"],
    [String, "topic", "the topic of the channel"],
    [Int, "position", "the sorting position of the channel"],
    [Int, "parent", "the category for this channel, 0 if none"],
    [Bool, "nsfw", "whether the channel is nsfw"]
)) do ctx, name::String, topic::String, position::Int, parent::Int, nsfw::Bool
    global c, votemap
    create_vote(CreateTextChannelVoteAction(name, topic, position, Ekztazy.Snowflake(parent), nsfw))
    Ekztazy.reply(c, ctx, content="Succesfully created vote proposal.")
end

command!(c, g, "create_voice_channel", "propose to create a voice channel", legacy=false, options=Options(
    [String, "name", "the name of the channel"],
    [Int, "position", "the sorting position of the channel"],
    [Int, "parent", "the category for this channel, 0 if none"],
)) do ctx, name::String, position::Int, parent::Int
    global c, votemap
    create_vote(CreateVoiceChannelVoteAction(name, position, Ekztazy.Snowflake(parent)))
    Ekztazy.reply(c, ctx, content="Succesfully created vote proposal.")
end