Give Claude Persistent Memory in 5 Minutes
Subtitle



https://www.youtube.com/watch?v=ryqpGVWRQxA

Claude code is great, but we also know it's only great in the session. Anytime
we pick back up, we've lost everything out of the last session. This is clawed
me. It gives Claude code persistent and compressed memory across sessions while
auto capturing stuff like bug fixes and decisions, then brings that context back
right when we need it. All open source, no API keys. We have videos coming out
all the time. Be sure to subscribe.
The setup here is really quick and you can get all this from the claude mem
repo. I'll assume you already have claude code installed as I do. So adding
claude mem is basically two commands inside claude. First fire up claude.
Then just run this command right here. After that we can install it with the
command right here. Both of these I got off the repo. I'm going to restart
Claude and you're done. That is claude mem right on your system. I didn't have
to play around with any config files or API keys, which is a huge bonus. And
here's the part I really like. It runs locally, so all this data it's capturing
is staying on your machine. All right, let me actually show you all the good
stuff here. It'll be quick so you can get the gist of it cuz that's what
matters. We're inside a fresh project folder, just some fast API I was messing
around with. But for this, we're going to make a super basic Python script just
to cover the point. In the first session, I'm going to ask Claude to
create a recursive Fibonacci PI file, but skip handling negative inputs.
As expected, Claude generates the file and opening it, it all looks good. So
now I'm going to run with this and I'm going to say I'll run it with a negative
number. For obvious reasons, we get an error. So I'll just tell Claude add a
value error when in is negative. Claude updates the code. I rerun it.
Clean error message. The bug's fixed. Okay, now here's the thing. Claude can
do that. That was super easy. While we're doing that though, Claude MEM is
quietly watching in the background. It's logging what just happened. This runs
completely locally on your local host. So, it's always refreshing. We can do
things here like the bug, right? I can view this. I can view the fix, the
reasoning, and the code diff. This is really the whole Claw mem web UI. And
you can see real-time entries that are categorized. And there's our bug fixed.
So now comes the real test cuz the first part is already nice. It was cool,
right, to see this, but basically it's just nice looking logs. I'm going to go
in here and I'm going to end the current session. I'm going to clear out my
terminal and I'm going to fire back up Claude now that I'm in a new session. So
I'm going to ask Claude to pick back up where we left off. Let me just ask it to
recall the Fibonacci bug we fixed last time.
And there it is. It's pulling in that context. Claude pulls the exact fix back
without me explaining the whole story again. And I can go one step further. I
can ask it to search for Fibonacci bug fix.
Now I get the compressed summary. And if I expand it, I get the full context. I
don't have to waste time here copying and pasting or trying to reexlain what
we were doing before. It just remembers. This is huge cuz now we can enter new
sessions, leave these sessions, and claude mem is running in the background
to help us out. There are a lot of things here that I love that are going
to help you out. First, it saves a huge amount of time, so you can stop
reloading context every session. Then, it's actually pretty token efficient.
Claude mem compresses memories by up to 10x, so we aren't hitting our limits as
fast as we once were. Finally, you can actually find stuff. You can search
memories by integrated tags that we have in Cloudme. Type things like bug fix or
decision file path or keywords that pops up in our UI. That's what makes this
really useful to us in these larger projects. And unlike Claude's basic
memory file, this is automatic. Plus, it's open source. So, if you want to
tweak it, you can. Long story short, that's Claude MEM, right? Cloud memory.
Claude MEM saves us time. This is ideally a tool to speed up your workflow
and save you a bunch of tokens. Try it out on your project. I think you'll
immediately feel the difference.

https://github.com/thedotmack/claude-mem.git

Claude Code's Memory System: The Full Guide (Most Developers Miss 90% of This)
Subtitle

https://www.youtube.com/watch?v=FRwZg6VOjvQ

In this video, Claude Code has a memory system most developers never use. Six
layers deep, self-writing notes, and a hidden feature that's rolling out right
now. You open a new Claude Code session. You explain your project, your stack,
your conventions, your team's weird naming patterns. Tomorrow, you do it all
again. But here's the thing. Clot code isn't actually amnesiac. It has a full
memory system. Most developers are using 10% of it. There are two completely
different memory systems at play. Number one, claude.md files, instructions you
write for claude to follow, like a file for AI behavior. Number two, automemory.
Claude's own nodes, things it figures out and saves for itself. Think of it as
Claude's private journal about your codebase. The cloud system goes six
layers deep. At the top, managed policy. Your IT team deploys this orwide. Every
developer, every machine, same clot behavior. Below that, project memory,
your claw.md in the repo shared with the team via git. Then project rules,
modular files include odd rules for fine grain control. Then user memory in your
home directory. Your personal preferences for every project. Then
project local claude.local.md personal overrides automatically get
ignored. And at the bottom, automemory cla's own nodes unique per repository.
Automemory is the hidden gem here. It lives at tilda.claude.
projects certainly your repo memory. A directory Claude writes to itself during
your sessions. It saves things like the commands to build your project, your
code start preferences, recurring bugs it solved, the architecture of your key
modules. The entry point is memory.mmd. And here's the critical constraint. Only
the first 200 lines load into Claude system prompt automatically. So Claude
keeps memory.md tight. Detailed nodes go into topic files. Debugging.md
patents.mmd which load on demand when you need them. Automemory is in gradual
rollout. To force it on, set claude_code disabled_memory
to zero. Claude MD files can import other files using the at sign syntax
like this. at sign readme and claude loads your readme as context. You can
import package.json for available commands, docs, architecture files, any
markdown. Both relative and absolute paths work. Recursive imports go up to
five hops deep. One important note, imports inside code spans and code
blocks are intentionally ignored, so you won't accidentally trigger imports in
documentation examples. For larger projects, one massive cla MD becomes a
nightmare to maintain. Entert rules tois a directory of focused topic specific
markdown files. Create code style.md for formatting rules. Testing.md for your
test conventions. Security.md for what claude should never do. The power move
part specific rules using yl front matter. Add a parts field with clock
patterns. And those rules only activate when claude works with matching files.
API rules only fire for TypeScript files under src API. React rules only for TSX
components. Security rules for everything. Surgical precision. Two
commands every CLA code user should know. /init bootstraps at clot.md for
your existing codebase. Clot analyzes your project and generates a starter
memory file. Run it once then refine /memory opens a file selector during any
session. Edit your clot.md your automemory or any imported file in your
system editor right now. You can also just tell cloud directly. Remember that
we use PNPM not mpm. It saves it. Enterprise teams can deploy
organizationwide zilot.md files through their configuration management systems.
MDM group policy ensible whatever you use. This managed policy file sits at a
system level path above any project or user settings. It loads first. It takes
the lowest priority and poss more specific instructions override it. One
file consistent AI behavior across every developer in your org. Three rules for
effective cloud memory. Be specific. Use two space indentation
beats format code properly. Use structure. Bullet points under
descriptive headings, not walls of text. Review periodically.
Memory goes stale. Your cloud.md from 6 months ago might be fighting your
current architecture. Update it. Your cloud code is as smart as the memory you
give it. Set up your cloud.md today. Enable automemory. Build the modular
rules your team actually needs. The link to the full docs is in the description.
If this helped, subscribe. We cover cloud code and aentic AI every week. Now
go make Claude remember things.



How Beads Fixes Claude Code's Memory Loss

https://www.youtube.com/watch?v=Ky_hfrn-sTw

Subtitle
I have been extensively doing AI pair programming for various clients and
absolutely love Anthropics Claude except for one brutal problem amnesia. Claude
code is an AI coding assistant that works directly in your terminal helping
you build features, debug issues, and architect systems. But here is the
catch. Every time you start a new session or hit context compaction,
Claude forgets everything, all the bugs it discovered, architectural decisions
you made and fix this later notes. Everything gone. You spend half your
time reexplaining what you were working on instead of actually building it. This
is where beads enter into the picture. Beads is an issue tracker built
specifically for AI agents. Instead of you maintaining stale to-do lists,
Claude automatically creates issues as it works. Tracks dependencies between
tasks and updates detailed notes at milestones.
When you start fresh after context complexion, Claude reads its own nodes
from beads and instantly knows what you were building, what decisions were made
and what's next. It's a persistent memory for your AI pair programmer. In
this video, we'll walk through real code examples showing how the amnesia problem
destroys productivity and then I will also show you how beads solves it with
automatic issue tracking, smart dependencies and persistent memory that
survives across sessions. First I thought I will do a hands-on one but I
think there is lot of uh screen slop which really really muddies the water.
So I have just built some slides but I can assure you you will learn more this
way and let me know in the comments what do you think about this new format. By
the way this is Fad Miraa and I welcome you to the channel. Please like the
video and subscribe and do me a favor become a member as that keeps the lights
on uh on the channel. Also if you're looking for AI updates without any hype
please follow me on X as I regularly post there now. Okay. And of course, if
you're looking to build an AI project for any enterprise, for any use case,
please reach out at vadmiraza.com and you can find the link in video
description. So, let's get started with the example.
Now, what we are going to do, we just first see what exactly is this uh
forgetful problem with AI agent especially with clot. So, let's get
started. Now if you look at this screen, Claude discovering three important
issues while working on this repo of mine. Rate limiting, email validation
and slug uniqueness. These discoveries happen naturally during implementation
while I am having a chat with claude in a session. So this is my day one. It has
done these discoveries. Everything looks good. I have spent the whole day
explaining all the context. Then comes the second day. Now
I have started a new session but all the context is gone. The discovered issues,
completed work and all the decisions evaporated. Now I have to spend the time
reconstructing what was already figured out.
This is where beats come into play. All you need to do in order to set it up
just download it with the kernel command and I will drop the link in video
description and just go to your repo and simply just do BD in it and initialize
it. So this one commands create a local SQLite database and a get synced backup
and this is only one manual setup. Everything else happens automatically
with some um magic by Stevia G. It just gets integrated with the cloud. So what
has just happened? Look um what happened here is that under
the hood it the beads stores everything in two places. A fast local database for
cloud to query and a get version file that syncs across your machine. So if
you have multiple people working on it, they can just simply pull and push from
the the repo commit to it and then everyone would be using the same stuff
and then you can simply import it in your SQLite database if you have a
multierson team there. Okay. Now how exactly be solves it? So look at this.
There is another new day. Whatever you are talking with the claude claude now
files issues automatically as it discovers them. No manual to-do list.
Each discovered issue is linked to the work that uncovered it. So you have been
talking with it. You are filing it. CL is storing it in the memory with the
help of beat. You are not doing anything. You are just carrying on with
your session as is. So at the end of the day what happens is that um at key
milestones claude has enriched the notes with what was completed decision made
and what's next. This becomes future claude's memory.
Now when the you know this is what day one was and this was the end of day one.
Now let's say day two comes in claude already has everything. It reads its own
notes and reconstructs full context instantly. No re-explaining needed. It
knows what was done. It's a new session, new conversation. And Claude already
knows what was done yesterday, what's pending, and what was discovered. How
good is that? And if you notice here, you're not doing anything different. Be
is taking care of everything here. So claude is automatically doing the BD
ready BD list show. You're not doing it. So this is the beauty of claude here.
Now there are lot of other features in it.
For example um you can also see that claude is creating a hard blocker
relationship. So the dashboard for example in this case the dashboard
cannot start until authentication is done and this prevents working on things
in the wrong order. So there are different you know uh dependencies in
your code. You don't want claude or any agent to start working in parallel or
build something which is dependent on another feature. So this is another
beauty of it. So the dependency system really ensures clot only sees work
that's actually ready to start. Blocked items stay hidden until their
dependencies are resolved. And as I said you know there are a lot of other chains
like it has discovery chain. every discovered issue is linked to the work
that found it. You get a complete audit trail of while building X we discovered
Y Z and W and it just files it away. And then you know if you want more fancy
stuff there is also some parent chart relationship which let Claude break down
large features into track trackable pieces. Each subtask is automat
automatically linked to the parent epic and then you know if you want to view
the hierarchy you just use a show command and for with that you can see
the entire feature hierarchy at a glance what's done what's in progress and
overall completion percentage and then these are some of the commands
where you can get a bird's eye view of your project status like how many issues
are open in progress or done plus how many clawed discovered automatically.
And then you know there are a lot of other things like for example you can
instantly see what's stuck and why and primarily this helps you prioritize
unblocking work or decide what to tackle and you can also use something as git
sync across machines like you are using your desktop or laptop or phone you can
simply use it you know uh inter machine sort of workflow if you please like
you're working something on your desktop in your office and then you and also
just move it to your home. So if you just look at the whole workflow, this is
how it works. So the entire workflow is in one you know you can see that where
cloud is managing everything automatically after you initialize this
and then accessible memory anywhere you work. This is the beauty of this tool.
Really really love it. Um so key takeaway you know beads transformed
claude from an amnesiac assistant into a persistent pair programmer who never
forgets what you are building. Saves a lot of trouble trust me.
So that's it. This is what I have been actually using in production environment
with real clients, real use cases because AI is awesome and great. But
when you actually implement in the real world then only then you realize the
problems like these and then I think the tools like beads are really really very
helpful. Entropic might really you know put it [clears throat] uh inside
Claude's next version who knows but for now beads is really really awesome.
So please like the video and subscribe and become a member as that helps a lot.

https://github.com/gastownhall/beads.git