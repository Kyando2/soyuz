@enum VoteActionType begin
    va_create_channel = 1
end

struct VoteAction 
    type::VoteActionType
    name::Ekztazy.Optional{String}
    channel_type::Ekztazy.Optional{Int}
    topic::Ekztazy.Optional{String}
    position::Ekztazy.Optional{Int}
    parent::Ekztazy.Optional{Ekztazy.Snowflake}
    nsfw::Ekztazy.Optional{Bool}
end
CreateTextChannelVoteAction(name::String, topic::String, position::Int, parent::Ekztazy.Snowflake, nsfw::Bool) = VoteAction(va_create_channel, name, 0, topic, position, parent, nsfw)
CreateVoiceChannelVoteAction(name::String, position::Int, parent::Ekztazy.Snowflake) = VoteAction(va_create_channel, name, 2, missing, position, parent, missing)

function perform(a::VoteAction)
    if a.type == va_create_channel
        if a.parent != 0 
            Ekztazy.create_guild_channel(c, parse(Int, g), name=a.name, type=a.channel_type, topic=a.topic, position=a.position, parent_id=a.parent, nsfw=a.nsfw)
        else 
            Ekztazy.create_guild_channel(c, parse(Int, g), name=a.name, type=a.channel_type, topic=a.topic, position=a.position, nsfw=a.nsfw)
        end
    end
end

function msg(a::VoteAction)
    if a.type == va_create_channel
        return "Proposal to create channel called $(a.name)."
    end
end