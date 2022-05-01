module Soyuz

using Ekztazy
using JSON3
using StructTypes

c = Client()

g = ENV["GUILD_ID"]

include("votes/actions.jl")

mutable struct Vote 
    alr_vo::Vector{Ekztazy.Snowflake}
    value::Int
    threshold::Int
    action::VoteAction
    closed::Bool
    orgmsg::Union{Ekztazy.Snowflake, Missing}
end

StructTypes.StructType(::Type{Vote}) = StructTypes.Struct()
StructTypes.StructType(::Type{VoteAction}) = StructTypes.Struct()

already_voted(v::Vote, u::Ekztazy.Snowflake) = u in v.alr_vo

const VOTECHID = 970108683746951178

votemap = JSON3.read(read("votemap.json", String), Dict{String, Vote})

current = sort([parse(Int, k) for k in keys(votemap)])[end]+1

function update_votemap()
    global votemap
    open("votemap.json", "w") do io
        write(io, JSON3.write(votemap))
    end
end

function create_vote(action::VoteAction) 
    global c, current, votemap
    local voteid = string(current)
    current += 1
    votemap[voteid] = Vote(Vector(), 0, 0, action, false, missing)
    byes = component!(c, "$(voteid)_FOR"; type=2, style=1, label="FOR") do ctx
        local vote = votemap[voteid]
        local id = ctx.interaction.member.user.id
        if !(already_voted(vote, id)) && !(vote.closed)
            push!(vote.alr_vo, id)
            vote.value+=1
            Ekztazy.reply(c, ctx, content="Successfully voted.", flags=64)
        elseif vote.closed 
            Ekztazy.reply(c, ctx, content="This vote has ended.", flags=64)
        elseif (already_voted(vote, id))
            Ekztazy.reply(c, ctx, content="Already voted.", flags=64)
        end
        if vote.value>vote.threshold && !(vote.closed)
            perform(action)
            orgmsg = Ekztazy.MessageReference(message_id=vote.orgmsg)
            if ismissing(orgmsg)
                create_message(c, VOTECHID, content="Vote #$(voteid) passed.")
            else 
                create_message(c, VOTECHID, content="Vote passed.", message_reference=orgmsg)
            end
            vote.closed = true
        end
        update_votemap()
    end
    bno = component!(c, "$(voteid)_AGAINST"; type=2, style=4, label="AGAINST") do ctx
        local vote = votemap[voteid]
        local id = ctx.interaction.member.user.id
        if !(already_voted(vote, id)) && !(vote.closed)
            push!(vote.alr_vo, id)
            vote.value-=1
            Ekztazy.reply(c, ctx, content="Successfully voted.", flags=64)
        elseif vote.closed 
            Ekztazy.reply(c, ctx, content="This vote has ended.", flags=64)
        elseif already_voted(vote, id)
            Ekztazy.reply(c, ctx, content="Already voted.", flags=64)
        end
        update_votemap()
    end
    local msgid = fetch(create_message(c, VOTECHID, content=msg(action), components=[Component(type=1, components=[byes, bno])])).val.id
    votemap[voteid].orgmsg = msgid
    update_votemap()
end

include("votes/channel.jl")

on_ready!(c) do ctx
    print("Logged in!")
end

start(c)

end
