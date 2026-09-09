# V01 — CLEAN READ SCRIPT (spoken words only)

Ng quotes verified against Whisper (`../ng-quotes-VERBATIM-whisper.txt`).
See `claim-source-map.md` and `VISUAL-MAP.md` before recording.

==== SCENE 01 — COLD OPEN ====

A couple of weeks ago, a man who has taught roughly eight million people how to use artificial intelligence sat down for an interview and said this.
"Frankly, AI models are terrible for learning."
That's Andrew Ng. He co-founded Coursera. He built the founding team at Google Brain. If there is a single person whose career is made of teaching people this technology, it's him. And he flagged the line himself, on camera, as controversial — "I don't know if I've said this publicly, but I think it's true" — and then doubled down on it.
Then he gave an example, and it was about himself.
He said he'd asked a model to help him build the front end and the back end of one of his own projects. It worked. He shipped it. Six months later he needed to build something very close to the same thing again — and he couldn't remember how he'd done it. Not the fine detail. Any of it. So he opened the model back up and started over.
The knowledge of how that thing got built was nowhere in his own head. It had never been there.
And I sat there thinking: I've done this. More than once.
I've built components for my own second-brain system — worked them out, got them running, been pleased with myself. And then months later I've gone back to extend one, or build something close to it, and found I have no idea how I did it the first time. Not a gap. An absence. Whatever understanding was supposed to be left behind after the work, wasn't.
Ng's point was that this isn't a story about him, or about me. He said the same pattern turns up across most of the research on using AI to get work done. And then he said five words that are the reason this video exists:
"The data is very clear."
He's right that it's clear. He just never said which data.
No paper, no name, no number. Just: the data is clear. > So I went and read it. All of it. Because this stopped being an academic question a while ago — it's a thing most of us now do every day, without thinking about it at all.
And what I found was not what I expected, in a way I'll get to. But the first thing worth saying is that the research splits clean down the middle — and almost nobody talks about the line it splits on.

==== SCENE 02 — THE LINE NOBODY DRAWS ====

Here's the thing that gets lost when this gets argued about online.
There are two completely different activities happening, and we use one word for both of them.
The first is using AI to teach you something. A tutor. A system built by people who think about how learning works, whose job is to get you to understand the thing.
And the evidence there is good. Genuinely good. Researchers have pooled dozens of proper trials of AI tutoring, and across all of them it comes out ahead of the alternative. Not miraculous — a modest, real improvement, showing up consistently across ages and subjects. When somebody sits down and engineers AI to teach, it teaches.
If that's the video you came for, that's the honest answer: it works, and I'd expect it to keep getting better. There's a lot to say about what that changes about school, and about who gets access to a tutor that never gets tired — and I'll make that video.
This isn't that video.
Because that is not what you and I do with it.
The second thing — the thing almost everybody is actually doing — is using AI to get a task finished. Not to be taught. To be done. The essay, the config, the analysis, the code, the deck by Thursday.
And here's why that difference matters more than it sounds.
Think about how you normally learn a hard thing. You don't learn it by being told. You learn it by struggling through it — the wrong turns, the thing that wouldn't work, the fix you found at eleven at night. And when you come out the other side, you keep something. Next time you meet that problem, or one that rhymes with it, you know your way around.
The struggle isn't the price of the learning. The struggle is where the learning happens.
So the question this video is about is simple, and nobody was really asking it until recently:
What happens to that — when something else does the struggling for you?
There are five things the research says. The first one is the one that explains why nobody noticed.

==== SCENE 03 — FINDING ONE: the two lines move in opposite directions ====

The first thing the research says is the strangest, and everything else follows from it.
What you produce gets better. You get worse. And both happen at the same time, from the same tool.
Those two things sound like they can't both be true. They are, and it's been measured now more than once, in different countries, on different people, doing different work.
Here's the cleanest version of it.
A team went into a high school in Turkey and did the obvious experiment, which — remarkably — almost nobody had bothered to do. Some students practiced math the way students always have. Some had GPT-4 sitting open beside them while they worked.
With the AI there, the second group was transformed. Their scores on the practice problems went up by nearly half. If you sell this software, that is the number on your slide, and it isn't a lie.
Then the researchers closed the laptops and gave everybody an exam.
The students who'd practiced with AI didn't merely lose their advantage. They finished below the students who never had it at all. They would have been better off if it had never been in the room.
Four sessions. That's how long it took to end up behind where they started — and the reason is that the practice never became learning. It stayed practice, done by something else.
The researchers have a word for what the students were doing. They call it a crutch — and a crutch works perfectly, right up until somebody takes it away and you discover what happened to the leg underneath.
Now hold that next to what happened in China, because the scale is different enough to matter. Researchers there followed twenty-six thousand students for two and a half years. Homework scores went up. Exam scores went down. Same students, same subjects, same time.
And in a lab, people asked to write an essay with AI wrote better essays — and, tested afterward, had learned no more from writing them than people who'd had no help at all. The essay improved. The understanding didn't move.
Three different setups. Same fingerprint every time. The work improves and the worker doesn't.
Which raises an obvious question, and it's the one that kept me reading.
If this is happening at that scale — how has nobody noticed?

==== SCENE 04 — FINDING TWO: you can't feel it happening ====

The answer is that everything you can see says it's working.
You cannot feel this happening. Not because you're careless — because every signal available to you in the moment is positive.
Think about what you actually observe when you finish something with AI. The task is done. It's done faster. It looks at least as good as what you'd have produced alone, often better. You were less frustrated. Nothing about that experience carries a warning.
In the Chinese study, that was true right down the line. Homework scores rose. Homework took less time. Kids were less miserable about it. Every measure a parent or a teacher actually looks at said this was going well.
The exam results were already sliding underneath, and nobody could see it, because nobody grades you on what you learned. They grade you on what you handed in. Those are different things, and only one of them shows up on the day.
And here's the detail from that study that genuinely unsettled me.
The full damage took about two years to show up.
Two years. That's not a feedback loop — that's no feedback at all. Whatever you did in the spring of one year surfaces as a worse result in a completely different context two years later, by which time you have no reason on earth to connect the two. You'd blame the test. You'd blame the teacher. You'd blame yourself for not being as sharp as you used to be.
You would never blame a tool that, at the time, made everything easier. You'd just quietly conclude you were worse at this than you used to be — which, in the only sense that matters, you would be.
And this is the right moment to be straight with you about the evidence, once, so I'm not interrupting the rest of this to hedge.
Some of this is early. The Turkish study and the lab work are properly controlled experiments, published and reviewed. The big Chinese one is an economics working paper — the numbers are real and the method is serious, but it hasn't been through peer review yet, and I'd rather you knew that from me than found it out later. None of these studies ran longer than a few years, because the technology isn't older than that. What we don't have is anyone's whole career.
So: not settled science. But four independent groups, on two continents, looking at different people doing different work, and finding the same shape. That's worth taking seriously, and it's the last time I'll qualify it.
Because there's a second thing hiding in this, and it's the part I think people would object to hardest — if they knew.

==== SCENE 05 — FINDING THREE: you don't get the time back ====

Everybody who defends this makes the same argument, and I think it's a reasonable one.
Fine. I learned less. But I got it done in half the time, and I'm an adult with a job — not every task in my life has to be an education. I'll trade the depth for the speed.
That's a real trade and there's nothing wrong with making it.
The problem is that it isn't the trade on offer.
Some researchers put this to the test on people who were not students. Working software developers — professionals, paid for the job — asked to learn a tool they'd never used. Half with AI, half without.
The ones with AI came out knowing less about the tool afterward. That part, by now, you can predict.
Here's what I didn't predict. They didn't finish any faster.
Not "slightly faster." Not "faster but not significantly." There was no time saving to speak of at all. They gave up the understanding and got nothing in exchange for it.
And when the researchers went back and watched the screen recordings to work out where the time went, the answer is almost funny. It went into talking to the AI. Some people asked it fifteen separate questions. Some spent more than a third of the whole task just composing what to ask.
Every minute saved by not writing the thing was spent asking for the thing.
So the bargain most of us think we're striking — I'll be a bit shallower, but I'll be quicker — was, at least here, not a bargain. It was just a loss with a good story attached.
Which brings me to the part that made me want to make this video in the first place. Because so far this is a story about one task, and one thing you didn't learn. It doesn't stay that way.

==== SCENE 06 — FINDING FOUR: so you ask again ====

Go back to where we started. Andrew Ng needed to rebuild something, couldn't remember how he'd done it, and opened the model back up.
Read that again as a sequence rather than an anecdote, because it's a loop, and the loop is the whole problem.
You use it to finish something. Because you finished it that way, you don't learn it. Because you didn't learn it, the next time you meet that problem you can't do it either. So you use it again. And that time you learn even less, because now you're not even starting from partial understanding — you're starting from nothing.
Every pass through that loop, there's less of you in the work.
That's the de-skilling. Not a dramatic collapse — a slow narrowing of what you can do unaided, happening at exactly the speed you'd never notice.
And the loop has a nasty property: it feels like competence the whole way round. You're shipping. You're solving things. Your output is fine. The only thing that changed is that none of it is load-bearing on you any more.
In the developer study, the people who handed the whole task over were the fastest in the entire experiment — and came out knowing the least. Speed and ignorance, arriving together, from the same behavior.
The Chinese researchers could actually pick these people out of the data, without ever meeting them. There's a signature: work finished faster than the quickest student who wasn't using AI, and scored just as high. Fast and correct and hollow.
Eighty-one percent of the AI users in that study left that fingerprint.
Eighty-one percent. That isn't a minority abusing the tool. That's what ordinary use looks like.
Which is where I expected to end this video. Something like: it's worse than you think, be careful out there, thanks for watching.
Except that when I got to the last part of the evidence, it turned the whole thing over.

==== SCENE 07 — FINDING FIVE: it isn't the tool ====

There was a third group in that Turkish experiment. I didn't tell you about it.
Same school. Same students. Same four sessions. Same model — the identical technology.
One difference: the researchers set it up so that it would not hand over answers. It gave hints, written by the teachers, and it made the student do the step.
That group performed the best of anybody during practice. Better than the ones who could ask it anything.
And when the laptops were taken away and the exam came round — they were fine. No penalty. They had kept what they learned. They came out level with the students who'd never used AI at all.
Same technology. Same room. Same week. One group ended up behind people who never touched it, and one group paid nothing at all. The only thing that differed was whether the thing would do the work for you when you asked it to.
So it isn't the tool. It was never the tool.
And then there's the finding I keep thinking about, which comes from watching those developers work.
The researchers didn't stop at "with AI" and "without AI." They sat and watched recordings of how each person actually used it, and found six distinct habits. Six ways of doing the same job with the same assistant.
Three of those habits destroyed the learning. Three of them protected it almost entirely.
The worst outcomes came from handing the whole thing over, or from bouncing errors back at it until something worked — people who finished the task and learned nothing from it. The best came from people who let it generate the answer, and then made themselves understand what it had written before they moved on. Same tool, same task; one group kept the knowledge and one group didn't.
That last group scored more than twice what the delegators did. Eighty-six against thirty-nine.
Now here's the number that I think is the only genuinely actionable thing in this entire video.
The difference in how long those two groups took?
Four and a half minutes.
Four and a half minutes, on a task of about twenty-five. For more than double the understanding retained.
And every one of those six habits is a person using AI. Nobody in that comparison refused the tool. Nobody went back to doing it the hard way. The gap between the best and the worst outcome had nothing to do with the technology and everything to do with whether, at any point, the person made themselves understand the thing in front of them.

==== SCENE 08 — THE VERDICT ====

So. Is AI terrible for learning?
No. But using AI to get your work done is — and that's how nearly all of us use it.
Built to teach you, it teaches. Set up to refuse the answer, it does no harm at all. Used the way you and I use it at four in the afternoon with something due — it hands you a finished thing and takes the understanding as payment, and it doesn't tell you that's the price.
Andrew Ng was right. He was also more precise than the sentence that got quoted. What he actually said was that we should stop thinking of AI as helpful for learning — in the vast majority of ways that the vast majority of people are using it today. That qualifier is the entire argument, and it's the first thing that falls off when a sentence travels.
I'm not going to tell you to stop using it. I use it constantly and I'm not going to pretend otherwise, and the evidence doesn't support that advice anyway — every single one of the people who came out of that study with their skills intact was using AI too.
What the evidence supports is much smaller, and much more annoying, which is usually how you know something is true.
Before you close the thing you just finished — make yourself understand what it did.
Not all of it. Not perfectly. Just enough that you could rebuild it without asking again.
That's four and a half minutes of actually understanding it. And the difference between spending them and not spending them is whether, two years from now, you're the person who knows how that works — or the person opening the model back up, starting over, wondering where it all went.
Ng couldn't rebuild his own project. I couldn't rebuild mine. Neither of us ever learned the thing we thought we'd done.
And neither of us noticed at the time. That's the part I'd want you to take away — not that the tool is dangerous, but that the moment it costs you something is a moment that feels completely fine.

==== SCENE 09 — CTA ====

One last thing, and then I'll get out of your way.
Every number in this video came from a paper I opened and read. All six of them are on screen right now — who wrote it, when, where it was published, and the reference you'd need to pull it yourself.
If you think I've got one of them wrong, go and check. That is not a rhetorical flourish. That is the entire point of what I'm trying to do here.
Because this is what this channel is going to be. Somebody makes a confident claim about AI — a claim with money riding on the answer — and I go and learn enough to do the arithmetic on it.
And sometimes the claim is going to hold up. When it does, I'll make that video too. Otherwise the ones where it doesn't aren't worth anything.
So if that's useful to you — subscribe. It's free and it's the only thing that decides whether this reaches anybody.
Hit the like button on your way out. I know. Everyone says it. It genuinely does change who gets shown this.
If you know somebody who's been arguing about this at work, or at home, or with a teenager — send it to them.
And ring the notification bell, because these take weeks to research and understand properly, and they don't come out on a schedule. The bell is the only way you'll know when the next one lands.
I'm Terry Byrd.
Go check my numbers.
