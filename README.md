jira-cli
========

A terminal app for managing JIRA tickets and Github pull requests

## Oh god, why?
I like staying in the terminal vs juggling a conglomerate of JIRA/GitHub tabs in Chrome.

## What does it do?
jira-cli gives you two main screens: one for viewing open GitHub PRs, another for viewing JIRA tickets.

The JIRA overview displays three categories
* in progress
* in TODO
* in Code Review

The GitHub overview displays any open pull requests you have.

## Isn't this _just_ a glorfied shortcut to Chrome?
Yes. The JIRA viewer is still WIP. A Github viewer will follow shortly after (then you'll never need to leave the terminal!)

## But if you want to stay in the terminal, why not use W3M?
No

## Stuff I need to fix before you try this out
* implement JIRA/GitHub caching
* fix the asynchronous JIRA lookups so they don't block UI

## Stuff I'm going to do afterwards
* fix the broken JIRA viewer (lets you view tickets in terminal)
* write a GitHub viewer
* make the command keys a bit more ergonomic
* and much, much more
