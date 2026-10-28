# Mission and principles

## Mission

> **OzarLand is a community-driven space for OpenStack operators to share knowledge, solve operational challenges,
> and make OpenStack operations better together.**

*OzarLand: a shared land for better OpenStack operations.*

OzarLand exists so that the people who run OpenStack platforms can learn from each other. It collects what
operators know from experience: how they deploy, what breaks, how they diagnose it, how they fix it, how they
upgrade, and what they would do differently next time.

## What the name means

OzarLand is a shared land for open source, where OpenStack operators help each other learn, troubleshoot and improve
operations.

| | |
|---|---|
| **Ozar** | The initiative's own name and identity. |
| **Land** | A shared place: everyone can bring their experience, learn from others and help the community grow. |
| **Open source** | Everything is public, under the Apache License 2.0, and improves through the contributions of the people who use it. |

This is the meaning the project gives itself, not a claim about where the word "Ozar" comes from.

## Where it comes from, and where it is going

OzarLand started as a personal initiative by Soufian Zaouam to share practical OpenStack operational knowledge. The
vision is to grow it into a collaborative space where OpenStack operators exchange experience, document solutions and
help one another operate more reliable platforms. Its future should not depend on its original author: it should grow
through the people who use it, improve it, question it and add their own experience. Today it is still small, built by
its maintainer with AI agents ([how OzarLand is built](how-ozarland-is-built.md)), and open to everyone.

## Core principles

| | Principle | What it means in practice |
|:-:|---|---|
| 🤝 | **Community first** | The project belongs to the people who contribute to it, not to one person or one company. |
| 📚 | **Knowledge sharing** | Practical experience is worth more when it is shared. |
| ⚙️ | **Operational excellence** | Real-world operations: troubleshooting, maintenance, upgrades, reliability. |
| 🔓 | **Open collaboration** | Anyone can contribute, whatever their experience. |
| 🛠️ | **Practical knowledge** | Actionable pages, tested procedures and real lessons, with how much each was checked. |
| 🌱 | **Collective improvement** | Every useful contribution can help another operator solve a problem. |

## The problem OzarLand addresses

Running OpenStack is a craft learned mostly on the job. Every operations team builds its own runbooks, its own
checklists and its own hard-won understanding of why a platform behaves the way it does. Most of that knowledge
never leaves the team.

Operational knowledge about OpenStack is abundant but fragmented. It lives in private wikis, chat threads,
personal notes and the heads of a few experienced people. When those people move on, the knowledge goes with them.
Public documentation explains how components are meant to work; it rarely explains what to do at 3 a.m. when an
instance is stuck in `deleting` and the compute node's agent is silent.

Many operators solve the same problems independently, in isolation, with no way to compare their approaches or to
confirm that a fix is sound outside their own environment.

## What OzarLand does

- Gives operators a public place to **ask questions** and get answers from peers who have seen the same thing.
- Captures **problems solved in production** as runbooks others can follow and improve.
- Documents **how operators deploy and operate** OpenStack, with the context and consequences of each choice.
- Pools **upgrade, incident and maintenance experience**, including what went wrong.
- Makes the **validity of each piece of knowledge explicit**: release, deployment method, conditions, and how
  many people have confirmed it.
- **Compares technical approaches** without declaring a single winner.
- Helps **experienced operators and newcomers learn from each other**.
- Turns **individual knowledge into collective knowledge** that anyone can reuse and improve.

OzarLand is a community, not a product. It does not tell operators how they must run OpenStack. It gives them a
place to learn from one another and to build a common body of operational knowledge, one real experience at a time.

## What OzarLand does not do

- It does not define a reference architecture or a recommended way to deploy OpenStack.
- It does not develop, promote or require any tool, distribution or vendor product.
- It does not certify procedures. "Validated by several operators" means exactly that, nothing more.
- It does not replace upstream documentation. It complements it with operational experience and links to it.
- It is not a support channel with response-time commitments. People help each other when they can.

## How the principles apply

1. **Collaboration over authority.** Nobody owns the right answer. Content is improved by comparing experiences.
2. **Openness.** Public discussions, public content, public decisions. Anyone can contribute, review and reuse.
3. **Tool neutrality.** Kolla-Ansible, OpenStack-Ansible, Charmed OpenStack, vendor distributions, custom
   builds: all are legitimate. Content about a specific tool says so, and never implies the others are wrong.
4. **Respect for different approaches.** Two operators can make opposite choices for good reasons. When they
   disagree, the community documents the trade-offs and the context in which each choice makes sense: the goal is to
   understand why, not to decide who is right.
5. **Real experience first.** A page describes something that happened on a real platform, or an approach someone
   actually operates. Theory is welcome when it explains an observation; hypotheses are labelled as such.
6. **Honesty about validity.** Every procedure states the release, the components, the deployment method and the
   conditions under which it was observed, and whether anyone else has confirmed it.
7. **Safety.** Commands that change state are flagged. Destructive commands carry an explicit warning. Secrets,
   hostnames, addresses, unredacted logs and anything that identifies an infrastructure never reach a repository.
8. **Lightweight governance.** Templates and conventions exist to make content findable and trustworthy. They are
   kept as small as possible, and they change when they get in the way.
9. **Knowledge must survive people.** Content is written so that someone who was not there can use it.
10. **Open about AI.** AI agents write, review and lab-test pages. This is said openly, every agent-authored pull
    request names its agent, and only a human operator can make a page `validated`. See
    [how OzarLand is built](how-ozarland-is-built.md).

The [code of conduct](../CODE_OF_CONDUCT.md) applies everywhere in the organisation.

## Who it is for

- Operators who run OpenStack platforms, in production or on their way there.
- Cloud and platform engineers who design and change those platforms.
- SREs and on-call engineers who respond to incidents on them.
- Newcomers who want to learn how OpenStack is actually operated, beyond the installation guides.
- Experienced operators who want to compare their practices with others and give back.
- Anyone responsible for an OpenStack platform who wants to compare notes with peers, from a one-node lab to a
  multi-region production cloud.

You do not need to use a particular deployment tool, distribution, storage backend or network plugin to take part.
Kolla-Ansible, OpenStack-Ansible, Charmed OpenStack, TripleO heritage platforms, vendor distributions, hand-built
clouds: every real-world setup is a valid source of experience.

## Relationship with upstream

OpenStack and Kolla are projects of the OpenInfra Foundation community. OzarLand is an independent community
initiative. It is not affiliated with or endorsed by the OpenInfra
Foundation or any vendor. When a community page uncovers a bug or a documentation gap in an OpenStack project,
contributors are encouraged to report it upstream and to link the upstream bug or change from the page.
