---
layout: post
title: "The Hidden Challenges of Git: Lessons from Working in Large Projects"
post_series_id: getting-started-with-git
date: 2025-09-08
author: sasadangelo
slug: hidden-challenges-of-git-lessons-from-large-projects
image: /assets/img/hidden-challenges-of-git-lessons-from-large-projects-hero.svg
excerpt: "Git lessons from large projects: a branching strategy, task branches, release candidates, hotfixes, and when small teams can simplify."
categories:
  - "Programming"
  - "DevOps"
---

# The Hidden Challenges of Git: Lessons from Working in Large Projects
_Posted on **{{ page.date | date_to_string }}**_

![The Hidden Challenges of Git: Lessons from Working in Large Projects]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

Git has become the standard tool for version control, powering collaboration and release management from personal projects to large enterprise systems. Yet despite its ubiquity, Git is not easy to master: managing complex merges, feature integrations, and clean histories can be challenging as projects scale. I don't claim to be an expert, but I'd like to share the practices and lessons that have helped me (and my teams) keep large projects organized and under control.

You should read this article if:

- you work on a Git repository shared by several developers and integration has become painful;
- you need a traceable release process with release candidates and hotfixes;
- you want to know when a simpler branching model is enough.

## Branching Strategy for Large-Scale Projects

For large projects with multiple contributors, a clear branching strategy is essential. Keeping the workflow simple but disciplined helps avoid confusion and reduce integration pain. The model below is a simplified variant of the classic [git-flow branching model](https://nvie.com/posts/a-successful-git-branching-model/).

- **Shared branches:** Use three protected branches: `development`, `release-candidate`, and `main`. The `development` branch is where feature branches are merged and tested together. Once enough features are ready, code moves to `release-candidate`. When stable, it's promoted to `main` for production.
- **Feature branches:** You develop each new feature in a separate branch (e.g., `feature-<your feature name>`) created from `development`. After automated tests and code review, you merge it back and delete the branch to keep the repo clean.
- **Hotfix branches:** You fix bugs discovered in `release-candidate` in dedicated branches (e.g., `hotfix-<your hotfix name>`) created from `release-candidate`, then test, review, and merge them back. Multiple cycles may be needed until the release is stable for promotion.

![The three shared branches: main, release-candidate, and development, with a feature branch merged into development]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-1.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Git shared branches*

## Protect Your Shared Branches

Always protect your shared branches (`development`, `release-candidate`, `main`) and avoid direct pushes. Require all changes to go through pull requests (PRs) with code review and passing tests. On GitHub, you configure this with [protected branch rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches). This keeps the branches stable, ensures review, and maintains a clean history. The automated tests that gate each PR are the same ones I describe in [Testing Python Applications with pytest]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/).

## Breaking Down Features into Task Branches

Small features that can be completed in 1–3 days can use a single feature branch: create it from `development`, implement the work, test it, open a PR, and merge. Simple and efficient.

For larger features, long-lived feature branches often cause painful merges, outdated code, and poor visibility. Many teams fail here because they don't spend enough time breaking a feature into autonomous, functional tasks that can be merged directly into `development`. It is the same idea of small, shippable increments behind [Agile methodology]({{ site.baseurl }}/demystifying-agile-unleashing-flexibility-project-management/).

Each task should be developed in its own branch (e.g., `task-<your task name>`), fully functional and testable on its own. Once reviewed and tested, it merges directly into `development`. This ensures incremental progress and continuous integration, and avoids risky end-of-feature merges. The result is a workflow closer to continuous delivery of building blocks than to infrequent large drops.

![A feature split into three independent task branches]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-2.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Breaking a feature into tasks*

## Daily Rebase and Single-Commit PRs

When working on a task or small feature, the developer creates a branch and should rebase it daily onto `development` to stay up to date. Many developers, both junior and experienced, struggle with rebases and conflict management. Once the task is complete, it's important to submit the PR as a single commit (a manual squash could be required), making it easier for reviewers to see exactly what changed.

In practice, the daily routine and the final squash look like this:

```shell
# Daily: replay your task commits on top of the latest development
git fetch origin
git rebase origin/development

# Before opening the PR: squash your task commits into one
git rebase -i origin/development
git push --force-with-lease
```

- `git rebase origin/development` replays your commits on top of the remote `development`, so conflicts surface early and in small pieces.
- `git rebase -i` opens an editor where you mark every commit except the first as `squash` (or `s`). See the [git-rebase documentation](https://git-scm.com/docs/git-rebase) for all options.
- `--force-with-lease` updates your remote task branch after the rewrite, but refuses to overwrite commits someone else pushed in the meantime.

During review, you may push additional commits to address feedback. GitHub's "Squash and merge" or "Rebase and merge" buttons collapse or replay them cleanly; see [About merge methods on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github). Always rebase your task branch instead of merging `development` into it, to avoid extra merge commits on `development`. After merging, delete the branch to prevent conflicts and a diverging commit history.

This approach keeps the history clean, ensures smooth reviews, and allows small tasks to integrate safely and incrementally into the main development flow.

## Release Candidate and Hotfix Workflows

Once a sufficient number of features are ready for production, the release candidate (RC) cycle begins. Often, multiple release candidates may be required before the final release. The process starts by promoting the code from `development` to `release-candidate` via a PR. I recommend using "Create a merge commit" and naming it clearly, e.g., `Release Candidate: <version>-rcX`. This makes it easy to track what each release candidate contains by looking at the commit history in both `release-candidate` and `main`.

![GitHub commit history showing the merge commit for release candidate 0.0.1-rc1 on top of three task commits]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-3.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Release candidates tracked with merge commits*

The code is then deployed to a staging environment, where end-to-end tests run. If you find defects, you fix them in a hotfix branch created directly from `release-candidate` and merge it back via PR. Each hotfix effectively generates a new release candidate, while `development` continues its next development cycle independently.

Once the release candidate passes all tests and is stable, the code is ready to be promoted to `main` and deployed to production. This workflow ensures a clear, traceable, and controlled path from development to production, reducing risks and making each release auditable. It is the Git side of the delivery pipeline I discuss in [DevOps in Software Development]({{ site.baseurl }}/bridging-gap-devops-software-development/).

![A hotfix branch created from release-candidate and merged back, while a feature continues on development]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-4.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Release candidate and hotfix workflow*

## Promote Code to Production

When a release candidate is ready for production, open a PR to merge `release-candidate` into `main`. I recommend using "Create a merge commit" and naming it clearly, e.g., `Release: <version>`. This not only shows all task commits included in the release but also documents the release candidates that preceded it.

Once the code is deployed to production, merge any hotfixes applied to the release candidate back into `development` to keep it up to date and aligned with production.

![GitHub commit history showing Release 0.0.1 on top of two release candidates and a hotfix]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-5.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Releases tracked with merge commits*

## Keep Development in Sync with Hotfixes

After merging a hotfix into `release-candidate` (or `main`), always bring those changes back into `development` through a PR with a merge commit. Since `development` is a protected shared branch, never rebase it: that would rewrite history everyone else has already pulled. This ensures `development` stays up to date with production fixes and avoids regressions in future releases.

![GitHub commit history of development showing a "Realign Release 0.0.1 hotfixes" merge commit]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-6.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Keeping development in sync with hotfixes*

## Simplifying for Small Teams or Rarely Updated Repositories

Not all projects need a complex set of shared branches. For very small teams (2–3 people) or repositories that are updated infrequently, for example metadata repositories, maintaining three protected branches (`development`, `release-candidate`, `main`) may be overkill.

In these situations, consider simplifications:

- **Single `main` branch:** If changes are rare and the risk of conflicts or regressions is low, a single branch may suffice. Developers can test locally before merging directly into `main`. This is close to [trunk-based development](https://trunkbaseddevelopment.com/).
- **Skipping `release-candidate`:** With fewer contributors, there may be less need for long release cycles, making a separate `release-candidate` branch unnecessary. Features and fixes can be integrated and tested directly in `main`.

This approach keeps the workflow simple while still maintaining control and traceability for small-scale projects.

![The branch model with release-candidate removed: features merge into development and then directly into main]({{ site.baseurl }}/assets/img/hidden-challenges-of-git-lessons-from-large-projects-fig-7.webp){:width="760" height="400" loading="lazy" .responsive_img}
*Simplified shared branches*

The table below summarizes which setup fits which kind of project:

| Project type | Shared branches | Release candidates | Hotfix flow |
|---|---|---|---|
| Large team, frequent releases | `development`, `release-candidate`, `main` | Yes, tracked with merge commits | `hotfix-*` from `release-candidate`, merged back into `development` |
| Small team (2–3 people) | `development`, `main` | Optional | Fixes integrated and tested directly in `main` |
| Rarely updated repository | `main` only | No | Fix directly on `main` via PR |

## Conclusion

A disciplined branching strategy and incremental, task-focused development keep Git histories clean and integration smooth. Release candidates and hotfix workflows provide a controlled path to production, but small teams or rarely updated repositories can simplify with fewer branches. Clear conventions help teams collaborate efficiently, regardless of project size.

In this article we covered:

- three protected shared branches (`development`, `release-candidate`, `main`) and why nobody pushes to them directly;
- breaking large features into small task branches that merge independently;
- daily rebasing and single-commit PRs to keep history readable;
- the release candidate and hotfix cycle, tracked with named merge commits;
- when a small team or a rarely updated repository can drop branches.

In the next article of this series, [Beyond Push and Pull]({{ site.baseurl }}/beyond-push-and-pull-understanding-git-core-concepts/), I step back to the core concepts underneath this workflow: where your changes live and how each Git command moves them.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
