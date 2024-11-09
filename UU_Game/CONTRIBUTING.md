# UU Game Project Guidelines

<hr>

- [Git](#git)
  - [Some Git rules](#some-git-rules)
  - [Git workflow](#git-workflow)
  - [Writing good commit messages](#writing-good-commit-messages)
- [Documentation](#documentation)
- [Environments](#environments)
- [Dependencies](#dependencies)
- [Testing](#testing)
- [Structure and Naming](#structure-and-naming)
- [Code style](#code-style)


<a name="git"></a>

## 1. Git

<a name="some-git-rules"></a>

### 1.1 Some Git rules

There are a set of rules to keep in mind:

- Perform work in a feature branch.

  _Why:_

  > Because this way all work is done in isolation on a dedicated branch rather than the main branch. It allows you to submit multiple pull requests without confusion. You can iterate without polluting the main branch with potentially unstable, unfinished code. [read more...](https://www.atlassian.com/git/tutorials/comparing-workflows#feature-branch-workflow)

- Branch out from `dev`

  _Why:_

  > This way, you can make sure that code in main will almost always build without problems, and can be mostly used directly for releases (this might be overkill for some projects).


- Update your local `dev` branch and do an interactive rebase before pushing your feature and making a Pull Request.

  _Why:_

  > Rebasing will merge in the requested branch (`main` or `dev`) and apply the commits that you have made locally to the top of the history without creating a merge commit (assuming there were no conflicts). Resulting in a nice and clean history. [read more ...](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

- Resolve potential conflicts while rebasing and before making a Pull Request.
- Delete local and remote feature branches after merging.

  _Why:_

  > It will clutter up your list of branches with dead branches. It ensures you only ever merge the branch back into (`main` or `dev`) once. Feature branches should only exist while the work is still in progress.

- Before making a Pull Request, make sure your feature branch builds successfully and passes all tests.

  _Why:_

  > You are about to add your code to a stable branch. If your feature-branch tests fail, there is a high chance that your destination branch build will fail too.

- Protect your `dev` and `main` branch.

  _Why:_

  > It protects your production-ready branches from receiving unexpected and irreversible changes. read more... [GitHub](https://help.github.com/articles/about-protected-branches/), [Bitbucket](https://confluence.atlassian.com/bitbucketserver/using-branch-permissions-776639807.html) and [GitLab](https://docs.gitlab.com/ee/user/project/protected_branches.html)

<a name="git-workflow"></a>

### 1.2 Git workflow

Since this is a smaller project, we will use a simplified version of a [Feature-branch-workflow](https://nvie.com/posts/a-successful-git-branching-model/).
We will use x.y.z to represent what version we are currently using, where x is the major version, y is the minor version and z is the patch.

- We have two main branches, `main` and `dev`.
- We do not work directly in the `main` or `dev` branches!
- We also have one type of support branch type, "feature".
- When implementing a new feature, we branch from the `dev` branch and give the new branch a descriptive but short name. I.e. `move_validator`.
- When the feature is completed, merge `dev` into your branch to avoid conflicts in the `dev` branch. Then increment the minor version and merge your branch into `dev` (This will be in the code at a later decided location).
- Bugfixes/Hotfixes are implemented as a feature type, before merging the fix, increment the patch (z). Bugfixes are allowed to be merged into `main` if the bug can break the system.
- Update the versions.txt located in the root folder with a short description of what the feature/fix does.

<a name="writing-good-commit-messages"></a>

### 1.3 Writing good commit messages

Having a good guideline for creating commits and sticking to it makes working with Git and collaborating with others a lot easier. Here are some rules of thumb ([source](https://chris.beams.io/posts/git-commit/#seven-rules)):

- Limit the subject line to 50 characters.

  _why_

  > Commits should be as fine-grained and focused as possible, it is not the place to be verbose. [read more...](https://medium.com/@preslavrachev/what-s-with-the-50-72-rule-8a906f61f09c)

- Capitalize the subject line.
- Do not end the subject line with a period.
- Use imperative mood in the subject line i.e. "Add ability to toggle game token".

  _Why:_

  > Rather than writing messages that say what a committer has done. It's better to consider these messages as the instructions for what is going to be done after the commit is applied on the repository. [read more...](https://news.ycombinator.com/item?id=2079612)

- Use the body to explain **what** and **why** as opposed to **how**. [read more...](https://cbea.ms/git-commit/#why-not-how)


<a name="documentation"></a>

## 2. Documentation

- Keep `README.md` updated as a project evolves.
- Comment your code. Try to make it as clear as possible what you are intending with each major section.
- If there is an open discussion on GitHub or stackoverflow about the code or approach you're using, include the link in your comment.
- Don't use clean code as an excuse to not comment at all.
- Keep comments relevant as your code evolves.

<a name="environments"></a>

## 3. Environments

### TODO...

<a name="dependencies"></a>

## 4. Dependencies

### TODO...

<a name="testing"></a>

## 5. Testing

### TODO...

<a name="structure-and-naming"></a>

## 6. Structure and Naming

Since this is a very small project, there is no specific standard for structure and naming.
The source files goes in the src folder located at root.

<a name="code-style"></a>

## 7. Code style

No code style is needed for this project. 
It could be wise to follow the code style in the prototype to make the code more consistent.
This is not a requirement, more of a recommendation.

Sources:
[RisingStack Engineering](https://blog.risingstack.com/),
[Mozilla dever Network](https://dever.mozilla.org/),
[Heroku Dev Center](https://devcenter.heroku.com),
[Airbnb/javascript](https://github.com/airbnb/javascript),
[Atlassian Git tutorials](https://www.atlassian.com/git/tutorials),
[Apigee](https://apigee.com/about/blog),
[Wishtack](https://blog.wishtack.com),
[A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/),
[How to Write a Git Commit Message](https://cbea.ms/git-commit/)
