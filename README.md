# Track issue 208
Track changes in the body text of matrix-org/matrix-appservice-irc#208

## What is this?
1. The [network wishlist issue] in repository form.
2. Infrastructure to keep (1) up-to-date.

## Why does it exist?
GitHub does not expose edit history for issues. For people working with the
[network wishlist issue] this is a problem in particular, since we can _see_
when it has been edited, but we can't see _what_ changed so we can update the
information in the [wiki], for example.

One could argue that keeping track of all that information in a GitHub issue is
abusing GitHub issues in a way they're not supposed to, and it would be much
better to use something that has first class support for edit history. But why
argue when you can code?

[network wishlist issue]: https://github.com/matrix-org/matrix-appservice-irc/issue/208
[wiki]:                   https://github.com/matrix-org/matrix-appservice-irc/wiki/Bridged-IRC-networks

## Status
**Alpha** This is a single-purpose hack and that's all it needs to be.

## Installation
```
$ cd $SOMEWHERE
$ git clone https://github.com/matrix-org/track-issue-208.git
```
Should the script fail because your Python installation is missing socks
support, you can add it to your project like so:
```
$ wget -P track-issue-208 -requests-adapter https://github.com/Anorov/PySocks/raw/master/socks.py
```
First Run:
```
$ cd track-issue-208
$ python3 trackissue208.py --help
```

## Getting help
If you have questions, contact [@Coffee:matrix.org], or tentatively ask in
[#irc:matrix.org].

[@Coffee:matrix.org]: https://matrix.to/#/@Coffee:matrix.org
[#irc:matrix.org]:    https://matrix.to/#/#irc:matrix.org

## License
* [208.md](208.md): Unspecified
* Everything else: Copyright 2018 [@Coffee:matrix.org]
